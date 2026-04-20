from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tts',
            executable='tts_service',
            name='tts_service',
            output='screen',
            emulate_tty=True,
        ),
    ])
