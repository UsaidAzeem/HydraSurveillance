# HydraSurveillance

Industrial security surveillance system for monitoring 20+ cameras simultaneously. Detects unauthorized persons during no-person hours (10 PM - 6 AM) and sends email alerts with snapshots.

## Features

- **Multi-camera support**: Monitor 20+ RTSP camera streams simultaneously
- **Time-based detection**: Only active during no-person hours (10 PM - 6 AM)
- **Person detection**: Uses YOLOv8n for real-time person detection
- **Email alerts**: Sends SMTP email alerts when person detected
- **Snapshot capture**: Automatically captures clear photos of detected persons

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure cameras in `config.py`:
```python
CAMERAS = {
    1: "rtsp://username:password@192.168.1.101:554/stream1",
    # Add your 20+ cameras here
}
```

3. Configure email alerts in `config.py`:
```python
ALERT_email_from = "your-email@gmail.com"
ALERT_email_to = "your-email@gmail.com"
ALERT_app_PASSWORD = "your-gmail-app-password"  # Generate from Google Account settings
```

4. Run the system:
```bash
python detector.py
```

## Configuration

Edit `config.py` to customize:
- `CAMERAS`: Dictionary of camera ID to RTSP URL
- `NO_PERSON_START/END`: Detection hours (default 22-6 = 10PM-6AM)
- `ALERT_cooldown_seconds`: Time between alerts
- `DETECTION_confidence`: YOLO confidence threshold

## Usage

- Press `q` to quit the program
- Alerts are sent asynchronously (non-blocking)
- Snapshots saved to `captures/` directory