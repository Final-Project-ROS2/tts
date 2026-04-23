# TTS (Text-to-Speech) ROS 2 Node

This package lets your robot **speak text out loud**. You send it a text message over ROS 2, and it reads it aloud through your speakers.

It uses `espeak-ng` — a free, lightweight speech engine that runs completely **offline** on your computer. No internet, no API key, no account needed.

> This guide assumes you are running **Ubuntu 22.04** inside **VMware** on a Mac, with **ROS 2 Humble** already installed.

---

## How It Works (Simple Version)

```
You publish a message  →  /tts topic  →  tts_service node  →  speaks out loud
```

For example, you publish `"Hello world"` to the `/tts` topic, and your VM's speakers say it.

---

## Step 1 — Prerequisites

Before starting, make sure you have these ready.

**Check ROS 2 is installed:**
```bash
ros2 --version
```
You should see something like `ros2 cli version: 0.18.x`. If you get `command not found`, install ROS 2 Humble first.

**Check your ROS 2 workspace exists:**
```bash
ls ~/ros2_ws/src
```
If the folder does not exist, create it:
```bash
mkdir -p ~/ros2_ws/src
```

---

## Step 2 — Install System Dependencies

Install `espeak-ng` (the speech engine) from Ubuntu's package manager:

```bash
sudo apt update
sudo apt install espeak-ng
```

**Test it works:**
```bash
espeak-ng "hello"
```
You should hear your VM say "hello" through your speakers. If you hear nothing, see the [Troubleshooting](#troubleshooting) section below.

---

## Step 3 — Get the Package

Clone this repository into your ROS 2 workspace:

```bash
cd ~/ros2_ws/src
git clone <repo-url> tts
```

Replace `<repo-url>` with the actual URL of this repository.

---

## Step 4 — Install Python Dependencies

```bash
pip install -r ~/ros2_ws/src/tts/requirements.txt
```

This installs `pyttsx3`, the Python library that talks to `espeak-ng`.

---

## Step 5 — Build the Package

```bash
cd ~/ros2_ws
colcon build --packages-select tts
```

Wait for it to finish. You should see:

```
Starting >>> tts
Finished <<< tts
```

Then load the package into your terminal session:

```bash
source ~/ros2_ws/install/setup.bash
```

> You need to run `source ~/ros2_ws/install/setup.bash` every time you open a new terminal. To avoid this, add it to your `.bashrc`:
> ```bash
> echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
> ```

---

## Step 6 — Run the Node

Open a terminal and start the TTS node:

```bash
ros2 launch tts tts.launch.py
```

You should see output like:
```
[tts_service]: TTS ready (espeak-ng). Voice: ...
```

The node is now running and waiting for text to speak.

---

## Step 7 — Send It Some Text

Open a **second terminal** and publish a message:

```bash
ros2 topic pub --once /tts std_msgs/msg/String "data: 'Hello from ROS 2'"
```

Your VM should speak the words out loud. You can change the text inside the single quotes to anything you want.

---

## Running Without the Launch File (Alternative)

If you prefer, you can run the node directly instead of using the launch file:

```bash
ros2 run tts tts_service
```

Both methods do the same thing. The launch file is the recommended way.

---

## Troubleshooting

### I hear nothing when I run `espeak-ng "hello"`

VMware needs audio output enabled. Check these steps:

1. **In VMware settings** — go to your VM settings and make sure "Sound Card" is added and enabled.

2. **Check PulseAudio is running inside Ubuntu:**
   ```bash
   pulseaudio --check -v
   ```
   If it is not running, start it:
   ```bash
   pulseaudio --start
   ```

3. **Test audio with a simple tone:**
   ```bash
   speaker-test -t sine -f 440 -l 1
   ```

---

### `espeak-ng: command not found`

Run the install again:
```bash
sudo apt install espeak-ng libespeak-ng-dev
```

---

### `ModuleNotFoundError: No module named 'pyttsx3'`

Run:
```bash
pip install pyttsx3
```

---

### The node starts but nothing is spoken

Check the node is actually receiving your message. In a second terminal:
```bash
ros2 topic echo /tts
```
Then publish your message in a third terminal. You should see the message appear in the `echo` terminal. If you do not, the topic name may be wrong.

---

### `source install/setup.bash` — command not found

Make sure you are in the right folder:
```bash
cd ~/ros2_ws
source install/setup.bash
```

---

## Quick Reference

| Task | Command |
|---|---|
| Install dependencies | `sudo apt install espeak-ng && pip install pyttsx3` |
| Build | `cd ~/ros2_ws && colcon build --packages-select tts` |
| Load into terminal | `source ~/ros2_ws/install/setup.bash` |
| Start the node | `ros2 launch tts tts.launch.py` |
| Send text to speak | `ros2 topic pub --once /tts std_msgs/msg/String "data: 'your text here'"` |
| Test espeak directly | `espeak-ng "hello"` |

---

## License

Apache-2.0
