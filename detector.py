import os
import cv2
import time
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from ultralytics import YOLO
from config import (
    CAMERAS, NO_PERSON_START, NO_PERSON_END,
    DETECTION_confidence, DETECTION_imgsz,
    ALERT_cooldown_seconds, ALERT_email_from, ALERT_email_to,
    ALERT_smtp_server, ALERT_smtp_port, ALERT_app_password,
    SNAPSHOT_frames_to_capture, SNAPSHOT_output_dir
)

os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
cv2.setNumThreads(1)

model = YOLO("yolov8n.pt").to("cpu")
os.makedirs(SNAPSHOT_output_dir, exist_ok=True)

class CameraMonitor:
    def __init__(self, cam_id, stream_url):
        self.cam_id = cam_id
        self.stream_url = stream_url
        self.cap = None
        self.last_alert = 0
        self.last_seen = time.time()
        self.alert_triggered = False
    
    def connect(self):
        self.cap = cv2.VideoCapture(self.stream_url)
        return self.cap.isOpened()
    
    def release(self):
        if self.cap:
            self.cap.release()
            self.cap = None

def is_no_person_hours():
    hour = datetime.now().hour
    if NO_PERSON_START > NO_PERSON_END:
        return hour >= NO_PERSON_START or hour < NO_PERSON_END
    return NO_PERSON_START <= hour < NO_PERSON_END

def send_alert_email(cam_id, snapshot_path=None):
    def _send():
        try:
            msg = MIMEMultipart()
            msg['From'] = ALERT_email_from
            msg['To'] = ALERT_email_to
            msg['Subject'] = f'[HYDRA ALERT] Person Detected - Camera {cam_id}'
            
            body = f'''
<b>⚠️ SECURITY ALERT</b><br><br>
<b>Camera:</b> {cam_id}<br>
<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
<b>Location:</b> Restricted Area<br><br>
Person detected during no-person hours (10 PM - 6 AM).
'''
            msg.attach(MIMEText(body, 'html'))
            
            if snapshot_path and os.path.exists(snapshot_path):
                with open(snapshot_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(snapshot_path))
                    msg.attach(img)
            
            server = smtplib.SMTP(ALERT_smtp_server, ALERT_smtp_port)
            server.starttls()
            server.login(ALERT_email_from, ALERT_app_PASSWORD)
            server.sendmail(ALERT_email_from, ALERT_email_to, msg.as_string())
            server.quit()
            print(f'[ALERT] Email sent for Camera {cam_id}')
        except Exception as e:
            print(f'[ALERT ERROR] Failed to send email: {e}')
    
    threading.Thread(target=_send, daemon=True).start()

def capture_snapshot(cam_id, stream_url):
    def _capture():
        try:
            cap = cv2.VideoCapture(stream_url)
            if not cap.isOpened():
                print(f'[SNAPSHOT] Cannot open stream for camera {cam_id}')
                return
            
            best_frame = None
            max_area = 0
            
            for _ in range(SNAPSHOT_frames_to_capture):
                ret, frame = cap.read()
                if not ret:
                    break
                
                results = model(frame, classes=[0], imgsz=DETECTION_imgsz, conf=DETECTION_confidence, verbose=False)
                boxes = results[0].boxes
                
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    area = (x2 - x1) * (y2 - y1)
                    conf = float(box.conf[0])
                    
                    if conf > 0.3 and area > max_area:
                        max_area = area
                        best_frame = frame[y1:y2, x1:x2]
            
            cap.release()
            
            if best_frame is not None:
                save_path = os.path.join(SNAPSHOT_output_dir, f'cam{cam_id}_{int(time.time())}.jpg')
                cv2.imwrite(save_path, best_frame)
                print(f'[SNAPSHOT] Captured for Camera {cam_id}: {save_path}')
                return save_path
            else:
                print(f'[SNAPSHOT] No person found for camera {cam_id}')
                return None
        except Exception as e:
            print(f'[SNAPSHOT ERROR] {e}')
            return None
    
    threading.Thread(target=_capture, daemon=True).start()

def run_surveillance():
    print('[HYDRA] Starting HydraSurveillance System...')
    print(f'[HYDRA] No-person hours: {NO_PERSON_START}:00 - {NO_PERSON_END}:00')
    print(f'[HYDRA] Monitoring {len(CAMERAS)} cameras')
    
    monitors = {}
    for cam_id, url in CAMERAS.items():
        monitor = CameraMonitor(cam_id, url)
        if monitor.connect():
            monitors[cam_id] = monitor
            print(f'[HYDRA] Camera {cam_id} connected')
        else:
            print(f'[HYDRA] Camera {cam_id} failed to connect')
    
    if not monitors:
        print('[HYDRA] No cameras connected. Exiting.')
        return
    
    quit_flag = False
    
    while not quit_flag and monitors:
        if not is_no_person_hours():
            time.sleep(30)
            continue
        
        for cam_id, monitor in list(monitors.items()):
            ret, frame = monitor.cap.read()
            if not ret:
                monitor.connect()
                continue
            
            results = model(frame, classes=[0], imgsz=DETECTION_imgsz, conf=DETECTION_confidence, verbose=False)
            now = time.time()
            
            if results[0].boxes:
                monitor.last_seen = now
                
                if now - monitor.last_alert >= ALERT_cooldown_seconds:
                    print(f'[ALERT] Person detected @ Camera {cam_id}')
                    monitor.last_alert = now
                    monitor.alert_triggered = True
                    
                    capture_snapshot(cam_id, monitor.stream_url)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                quit_flag = True
                break
    
    for monitor in monitors.values():
        monitor.release()
    cv2.destroyAllWindows()
    print('[HYDRA] Shutdown complete.')

if __name__ == '__main__':
    run_surveillance()