import sys
import os
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from TTS.api import TTS as CoquiTTS

try:
    import simpleaudio as sa
    SIMPLEAUDIO_AVAILABLE = True
except ImportError:
    SIMPLEAUDIO_AVAILABLE = False

class TTSTopicNode(Node):
    def __init__(self):
        super().__init__('tts_topic_node')

        # Subscribe to '/tts' topic
        self.subscription = self.create_subscription(
            String,
            '/tts',
            self.listener_callback,
            10)

        self.get_logger().info('Loading Coqui TTS model...')
        # Initializing the model
        self.tts = CoquiTTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False)
        self.get_logger().info('TTS Topic Node Ready. Listening on /tts')

    def listener_callback(self, msg):
        self.get_logger().info(f'Processing speech for: "{msg.data}"')
        try:
            output_path = "/tmp/output.wav"
            self.tts.tts_to_file(text=msg.data, file_path=output_path)
            # give the system a brief moment before playback to avoid missing the first word
            time.sleep(1.0)
            if SIMPLEAUDIO_AVAILABLE:
                try:
                    wave_obj = sa.WaveObject.from_wave_file(output_path)
                    play_obj = wave_obj.play()
                    play_obj.wait_done()
                except Exception as inner_exc:
                    self.get_logger().warn(f'simpleaudio playback failed: {inner_exc} — falling back to aplay')
                    os.system(f"aplay {output_path}")
            else:
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
