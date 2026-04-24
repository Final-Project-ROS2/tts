from setuptools import find_packages, setup

import os
from glob import glob

package_name = 'tts'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
    ],
    install_requires=[
        'setuptools',
        'pyttsx3',
        'coqui-tts',
        'simpleaudio',
    ],
    zip_safe=True,
    maintainer='final-project',
    maintainer_email='karamahati@gmail.com',
    description='Text-to-Speech subscriber node for ROS 2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tts_service = tts.tts_service:main',
            'tts_node = tts.tts_node:main',
        ],
    },
)
