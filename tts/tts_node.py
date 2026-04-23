import sys
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from TTS.api import TTS as CoquiTTS

# --- PORTABLE PATH LOGIC ---
# This finds the home directory of whoever is running the code
home_dir = os.path.expanduser('~')

# Instead of hardcoding "/home/ppoohkt", we build the path dynamically
install_path = os.path.join(home_dir, 'ros2_ws/install/tts_interfaces/lib/python3.10/site-packages')
local_path = os.path.join(home_dir, '.local/lib/python3.10/site-packages')

sys.path.append(install_path)
sys.path.append(local_path)


class TTSTopicNode(Node):
    def __init__(self):
        super().__init__('tts_topic_node')

        # Subscribe to 'speech_text' topic
        self.subscription = self.create_subscription(
            String,
            'speech_text',
            self.listener_callback,
            10)

        self.get_logger().info('Loading Coqui TTS model...')
        # Initializing the model
        self.tts = CoquiTTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False)
        self.get_logger().info('TTS Topic Node Ready. Listening on /speech_text')

    def listener_callback(self, msg):
        self.get_logger().info(f'Processing speech for: "{msg.data}"')
        try:
            output_path = "/tmp/output.wav"
            self.tts.tts_to_file(text=msg.data, file_path=output_path)
            # aplay is standard on most Ubuntu systems
            os.system(f"aplay {output_path}")
        except Exception as e:
            self.get_logger().error(f"TTS Error: {e}")


def main():
    rclpy.init()
    node = TTSTopicNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
