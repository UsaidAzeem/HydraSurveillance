# HydraSurveillance : Multiple Cameras at once

A production-grade industrial surveillance system designed for round-the-clock security monitoring. HydraSurveillance processes 20+ RTSP camera streams simultaneously, detecting unauthorized intrusions during restricted hours and delivering real-time alerts with photographic evidence.

**Key Capabilities**
- Real-time person detection across 20+ camera feeds using YOLOv8n
- Intelligent time-window filtering (10 PM - 6 AM active monitoring)
- Automated snapshot capture with best-frame selection
- Non-blocking alert pipeline (~45 second end-to-end)

**Performance Summary**
- Single camera: 4-9 FPS @ ~15% CPU
- 20 cameras: 0.5-1 FPS @ ~95% CPU
- Memory footprint: ~306 MB baseline
- Network: 20-80 Mbps aggregate bandwidth

---

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores @ 2.0 GHz | 8 cores @ 3.0 GHz+ |
| RAM | 4 GB | 8 GB |
| Storage | 10 GB free | 50 GB SSD |
| Network | 100 Mbps | 1 Gbps |
| Cameras | 20 | 20-50 |

## Compute & Time Analysis

### Per-Camera Processing

```
Frame capture (RTSP):    ~30-100ms   (network dependent)
YOLOv8n inference:       ~80-150ms  (CPU, imgsz=480)
Detection parsing:       ~1-5ms
Total per frame:         ~111-255ms
```

### Throughput Calculations

| Camera Count | Frames/sec | CPU Load | RAM Usage |
|-------------|------------|---------|-----------|
| 1 | ~4-9 | ~15% | 1.2 GB |
| 5 | ~2-4 | ~50% | 1.8 GB |
| 10 | ~1-2 | ~80% | 2.5 GB |
| 20 | ~0.5-1 | ~95%+ | 4.0 GB |

### Alert Pipeline

```
Detection trigger:      0ms       (in main loop)
Snapshot thread start:  0ms       (async)
Capture 150 frames:      ~30sec    (background)
Model inference ×150:  ~15sec    (CPU)
Best selection:         0ms
Email send:              ~2-5sec   (SMTP)
Total alert time:        ~45sec    (non-blocking)
```

### Time Window Check

```
datetime.now():        <1ms
Hour comparison:       <1ms
Sleep interval:        30sec
```

## Memory Usage

| Component | Memory |
|-----------|--------|
| YOLOv8n model | ~6 MB |
| 20 video buffers | ~100 MB |
| Python overhead | ~200 MB |
| **Total** | **~306 MB** |

## Network Bandwidth

```
20 cameras × 4 Mbps stream = 80 Mbps (typical)
20 cameras × 1 Mbps stream = 20 Mbps (substream)
```

## Performance Optimization

1. **OMP_NUM_THREADS=4** - Limits OpenMP threads per process
2. **MKL_NUM_THREADS=4** - Limits Intel MKL threads
3. **cv2.setNumThreads(1)** - Limits OpenCV threads
4. **imgsz=480** - Reduces inference resolution
5. **Async alerts** - Non-blocking snapshot capture

## Bottlenecks

1. **CPU** - YOLOv8n inference is CPU-bound
2. **Network** - RTSP streams at scale
3. **RAM** - Video frame buffers

## Scaling Formula

```
Max cameras = (CPU cores × 0.8) / 1.5
```

For 20+ cameras at acceptable framerate, consider:
- Multi-process architecture (separate detector per camera)
- GPU acceleration (YOLOv8n with CUDA)
- Edge devices per camera
