import sys
import types
import pytest
from types import SimpleNamespace


def test_tts_topic_node_calls_coqui_tts_and_aplay(monkeypatch):
    # Prevent importing the real Coqui TTS package during tests.
    fake_api = types.ModuleType("TTS.api")
    class DummyCoquiTTS:
        def __init__(self, *args, **kwargs):
            self.calls = []

        def tts_to_file(self, text, file_path):
            self.calls.append((text, file_path))
    fake_api.TTS = DummyCoquiTTS
    fake_TTS = types.ModuleType("TTS")
    fake_TTS.api = fake_api
    sys.modules["TTS"] = fake_TTS
    sys.modules["TTS.api"] = fake_api

    import tts.tts_node as tts_node

    # Replace Node initialization and logging so we can instantiate without a ROS context.
    monkeypatch.setattr(tts_node.Node, "__init__", lambda self, *args, **kwargs: None)
    monkeypatch.setattr(tts_node.Node, "get_logger", lambda self: SimpleNamespace(info=lambda *a, **k: None, warn=lambda *a, **k: None, error=lambda *a, **k: None))

    # Capture subscription creation and verify the topic name.
    subscription_args = {}

    def fake_create_subscription(self, msg_type, topic, callback, qos):
        subscription_args["msg_type"] = msg_type
        subscription_args["topic"] = topic
        subscription_args["callback"] = callback
        subscription_args["qos"] = qos
        return "subscription"

    monkeypatch.setattr(tts_node.Node, "create_subscription", fake_create_subscription)

    # Replace CoquiTTS with a dummy object that records the invoked method.
    class DummyCoquiTTS:
        def __init__(self, *args, **kwargs):
            self.calls = []

        def tts_to_file(self, text, file_path):
            self.calls.append((text, file_path))

    monkeypatch.setattr(tts_node, "CoquiTTS", DummyCoquiTTS)

    commands = []
    monkeypatch.setattr(tts_node.os, "system", lambda cmd: commands.append(cmd) or 0)

    node = tts_node.TTSTopicNode()

    assert node.subscription == "subscription"
    assert subscription_args["topic"] == "/tts"
    assert subscription_args["qos"] == 10

    message = SimpleNamespace(data="hello world")
    node.listener_callback(message)

    assert node.tts.calls == [("hello world", "/tmp/output.wav")]
    assert commands == ["aplay /tmp/output.wav"]
