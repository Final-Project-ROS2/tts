#!/usr/bin/env python3

import threading

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from TTS.api import TTS
import sounddevice as sd


class TTSService(Node):
    def __init__(self):
        super().__init__('tts_service')

        self.get_logger().info('Loading Coqui TTS model...')
        self.tts = TTS('tts_models/en/ljspeech/tacotron2-DDC')
        # output_sample_rate moved in newer Coqui TTS builds; fall back gracefully
        syn = self.tts.synthesizer
        self.sample_rate = (
            getattr(syn, 'output_sample_rate', None)
            or getattr(getattr(syn, 'tts_config', None), 'audio', {}).get('sample_rate', None)
            or 22050
        )
        self.get_logger().info(f'TTS ready. sample_rate={self.sample_rate}')

        self._speak_lock = threading.Lock()

        self.subscription = self.create_subscription(
            String,
            '/tts',
            self.tts_callback,
            10
        )

    def tts_callback(self, msg: String):
        text = msg.data.strip()
        if not text:
            return
        self.get_logger().info(f'Speaking: "{text}"')
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()

    def _speak(self, text: str):
        with self._speak_lock:
            try:
                wav = self.tts.tts(text=text)
                sd.stop()
                sd.play(wav, samplerate=self.sample_rate)
                sd.wait()
            except Exception as e:
                self.get_logger().error(f'TTS playback failed: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = TTSService()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
