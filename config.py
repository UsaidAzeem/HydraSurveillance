# HydraSurveillance Configuration
# Camera streams (RTSP URLs) - add your 20+ cameras here
CAMERAS = {
    1: "rtsp://username:password@192.168.1.101:554/stream1",
    2: "rtsp://username:password@192.168.1.102:554/stream1",
    3: "rtsp://username:password@192.168.1.103:554/stream1",
    4: "rtsp://username:password@192.168.1.104:554/stream1",
    5: "rtsp://username:password@192.168.1.105:554/stream1",
    6: "rtsp://username:password@192.168.1.106:554/stream1",
    7: "rtsp://username:password@192.168.1.107:554/stream1",
    8: "rtsp://username:password@192.168.1.108:554/stream1",
    9: "rtsp://username:password@192.168.1.109:554/stream1",
    10: "rtsp://username:password@192.168.1.110:554/stream1",
    11: "rtsp://username:password@192.168.1.111:554/stream1",
    12: "rtsp://username:password@192.168.1.112:554/stream1",
    13: "rtsp://username:password@192.168.1.113:554/stream1",
    14: "rtsp://username:password@192.168.1.114:554/stream1",
    15: "rtsp://username:password@192.168.1.115:554/stream1",
    16: "rtsp://username:password@192.168.1.116:554/stream1",
    17: "rtsp://username:password@192.168.1.117:554/stream1",
    18: "rtsp://username:password@192.168.1.118:554/stream1",
    19: "rtsp://username:password@192.168.1.119:554/stream1",
    20: "rtsp://username:password@192.168.1.120:554/stream1",
}

# Time window for detection (24-hour format)
# Only detect persons between NO_PERSON_START and NO_PERSON_END
NO_PERSON_START = 22  # 10 PM
NO_PERSON_END = 6     # 6 AM

# Detection settings
DETECTION_confidence = 0.25
DETECTION_imgsz = 480

# Alert settings
ALERT_cooldown_seconds = 20
ALERT_email_from = "usaidazeem880@gmail.com"
ALERT_email_to = "usaidazeem880@gmail.com"
ALERT_smtp_server = "smtp.gmail.com"
ALERT_smtp_port = 587
ALERT_app_password = "YOUR_APP_PASSWORD"  # Generate from Gmail

# Snapshot settings
SNAPSHOT_frames_to_capture = 150
SNAPSHOT_output_dir = "captures"