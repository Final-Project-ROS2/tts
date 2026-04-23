import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from TTS.api import TTS as CoquiTTS

class TTSTopicNode(Node):
    def __init__(self):
        super().__init__('tts_topic_node')
        self.subscription = self.create_subscription(String, 'speech_text', self.listener_callback, 10)
        self.get_logger().info('Loading Coqui TTS model...')
        self.tts = CoquiTTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False)
        self.get_logger().info('TTS Topic Node Ready. Publish to /speech_text to talk.')

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')
        try:
            output_path = "/tmp/output.wav"
            self.tts.tts_to_file(text=msg.data, file_path=output_path)
            os.system(f"aplay {output_path}")
        except Exception as e:
            self.get_logger().error(f"Failed to play: {e}")

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