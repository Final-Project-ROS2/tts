# TTS (Text-to-Speech) ROS 2 Node

This package lets your robot **speak text out loud**. Publish a string to the `/tts` ROS 2 topic and the node synthesizes speech and plays it through your speakers.

It uses **Coqui TTS** (`tts_models/en/ljspeech/vits`) — a high-quality neural TTS engine that runs completely **offline**. No internet, no API key, no account needed.

> This guide assumes you are running **Ubuntu 22.04** with **ROS 2 Humble** already installed.

---

## How It Works

```
ros2 topic pub /tts  →  tts_topic_node  →  Coqui TTS  →  aplay  →  speakers
```

Publish `"Hello world"` to `/tts` and your speakers say it.

---

## Step 1 — Prerequisites

**Check ROS 2 is installed:**
```bash
ros2 --version
```

**Check your ROS 2 workspace exists:**
```bash
ls ~/final_project_ws/src
```
If it does not exist:
```bash
mkdir -p ~/final_project_ws/src
```

---

## Step 2 — Install System Dependencies

Install `aplay` (ALSA audio player) used to play the synthesized WAV file:

```bash
sudo apt update
sudo apt install alsa-utils
```

**Test it works:**
```bash
aplay --version
```

---

## Step 3 — Get the Package

Clone this repository into your ROS 2 workspace:

```bash
cd ~/final_project_ws/src
git clone https://github.com/Final-Project-ROS2/tts.git
```

---

## Step 4 — Install Python Dependencies

Install Coqui TTS. On Ubuntu 22.04+ with a managed Python environment, use:

```bash
pip install coqui-tts --break-system-packages
```

If you are inside an active virtual environment (`tts_venv` or similar), use the venv's pip directly to avoid the system restriction:

```bash
~/tts_venv/bin/pip install coqui-tts
```

> The first time the node starts, Coqui TTS will automatically download the `tts_models/en/ljspeech/vits` model (~100 MB). This only happens once; subsequent runs load from cache.

---

## Step 5 — Build the Package

**Important:** Run `colcon build` from the **workspace root** (`~/final_project_ws`), not from inside the package directory.

```bash
cd ~/final_project_ws
colcon build --packages-select tts
```

You should see:

```
Starting >>> tts
Finished <<< tts
```

Load the package into your terminal session:

```bash
source ~/final_project_ws/install/setup.bash
```

> Add this line to `~/.bashrc` to avoid running it every time:
> ```bash
> echo "source ~/final_project_ws/install/setup.bash" >> ~/.bashrc
> ```

---

## Step 6 — Run the Node

```bash
ros2 run tts tts_node
```

You should see:

```
[tts_topic_node]: Loading Coqui TTS model...
[tts_topic_node]: TTS Topic Node Ready. Listening on /tts
```

The node is now running and waiting for text to speak.

---

## Step 7 — Send It Some Text

Open a **second terminal** and publish a message:

```bash
ros2 topic pub --once /tts std_msgs/msg/String "data: 'Hello from ROS 2'"
```

Your speakers should say the words out loud. Change the text inside the single quotes to anything you want.

---

## Topic Reference

| Topic | Type | Direction | Description |
|---|---|---|---|
| `/tts` | `std_msgs/msg/String` | Subscribe | Text to be spoken aloud |

---

## Troubleshooting

### No audio output

Check that `aplay` can play audio:
```bash
aplay /usr/share/sounds/alsa/Front_Left.wav
```
If you hear nothing, check your system's audio output device.

---

### `aplay: command not found`

```bash
sudo apt install alsa-utils
```

---

### `ModuleNotFoundError: No module named 'TTS'`

```bash
pip install coqui-tts
```

---

### The node starts but nothing is spoken

Check the node is receiving messages. In a second terminal:
```bash
ros2 topic echo /tts
```
Then publish in a third terminal. You should see the message appear. If not, the topic name may be wrong.

---

### `source install/setup.bash` — command not found

Make sure you are in the right folder:
```bash
cd ~/final_project_ws
source install/setup.bash
```

---

## Quick Reference

| Task | Command |
|---|---|
| Install audio player | `sudo apt install alsa-utils` |
| Install Coqui TTS | `pip install coqui-tts --break-system-packages` |
| Build | `cd ~/final_project_ws && colcon build --packages-select tts` |
| Load into terminal | `source ~/final_project_ws/install/setup.bash` |
| Start the node | `ros2 run tts tts_node` |
| Send text to speak | `ros2 topic pub --once /tts std_msgs/msg/String "data: 'your text here'"` |

---

## License

Apache-2.0
