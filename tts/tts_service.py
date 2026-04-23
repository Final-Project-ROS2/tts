#!/usr/bin/env python3

import queue
import threading

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String

import pyttsx3


class TTSService(Node):
    def __init__(self):
        super().__init__('tts_service')

        self._speech_queue = queue.Queue()
        self._engine = None
        self._engine_ready = threading.Event()

        # /tts_busy  — True while speaking, False when idle
        # /tts_done  — True on success, False on error (once per utterance)
        self._busy_pub = self.create_publisher(Bool, '/tts_busy', 10)
        self._done_pub = self.create_publisher(Bool, '/tts_done', 10)

        self.subscription = self.create_subscription(
            String,
            '/tts',
            self.tts_callback,
            10
        )

        # Init engine and worker in background so the node starts spinning immediately
        threading.Thread(target=self._init_engine, daemon=True).start()
        threading.Thread(target=self._speech_worker, daemon=True).start()

    def _init_engine(self):
        try:
            self._engine = pyttsx3.init()
            voices = self._engine.getProperty('voices')
            voice_id = voices[0].id if voices else 'default'
            self.get_logger().info(f'TTS ready (espeak-ng). Voice: {voice_id}')
        except Exception as e:
            self.get_logger().error(
                f'Failed to init TTS engine: {e}\n'
                'Make sure espeak-ng is installed: sudo apt install espeak-ng'
            )
        finally:
            self._engine_ready.set()

    def tts_callback(self, msg: String):
        text = msg.data.strip()
        if not text:
            return
        if not self._engine_ready.is_set():
            self.get_logger().warn('TTS engine still initialising — message queued.')
        self.get_logger().info(f'Queued: "{text}"')
        self._speech_queue.put(text)

    def _speech_worker(self):
        self._engine_ready.wait()
        if self._engine is None:
            self.get_logger().error('TTS engine unavailable — speech worker exiting.')
            return
        while rclpy.ok():
            try:
                text = self._speech_queue.get(timeout=1.0)
            except queue.Empty:
                continue
            success = False
            try:
                self.get_logger().info(f'Speaking: "{text}"')
                self._publish_busy(True)
                self._engine.say(text)
                self._engine.runAndWait()
                success = True
            except Exception as e:
                self.get_logger().error(f'TTS playback failed: {e}')
            finally:
                self._publish_busy(False)
                done_msg = Bool()
                done_msg.data = success
                self._done_pub.publish(done_msg)
                self._speech_queue.task_done()

    def _publish_busy(self, state: bool):
        msg = Bool()
        msg.data = state
        self._busy_pub.publish(msg)


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
