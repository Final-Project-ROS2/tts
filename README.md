# tts

A ROS 2 Python package that subscribes to the `/tts` topic and speaks incoming text using [Coqui TTS](https://github.com/coqui-ai/TTS) and [sounddevice](https://python-sounddevice.readthedocs.io/).

## Requirements

| Dependency | Notes |
|---|---|
| ROS 2 (Humble or later) | `rclpy`, `std_msgs`, `launch_ros` |
| Python ≥ 3.8 | |
| Coqui TTS | `pip install coqui-tts[codec]` |
| sounddevice | `pip install sounddevice` |
| PortAudio | system library required by sounddevice (`brew install portaudio` / `sudo apt install libportaudio2`) |

## Installation

```bash
# 1. Clone into your ROS 2 workspace src/
cd ~/ros2_ws/src
git clone <repo-url> tts

# 2. Install Python dependencies
pip install -r tts/requirements.txt

# 3. Build
cd ~/ros2_ws
colcon build --packages-select tts
source install/setup.bash
```

> **Note:** The first run downloads the `tts_models/en/ljspeech/tacotron2-DDC` model (~100 MB) and requires internet access.

## Usage

### Launch the node

```bash
ros2 launch tts tts.launch.py
```

### Publish a message

```bash
ros2 topic pub --once /tts std_msgs/msg/String "data: 'Hello from ROS 2'"
```

### Run the node directly

```bash
ros2 run tts tts_service
```

## Architecture

```
/tts  (std_msgs/String)
       │
       ▼
  tts_service node
       │  Coqui TTS  →  wav samples
       ▼
  sounddevice.play()
```

Concurrent messages are serialised with a threading lock — the node will finish speaking the current utterance before starting the next one.

## Limitations

- English-only (hardcoded `tts_models/en/ljspeech/tacotron2-DDC` model).
- Requires a working audio output device. Check `python3 -c "import sounddevice; print(sounddevice.query_devices())"` if no audio is heard.

## License

Apache-2.0
