from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'robot_commander'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='huawei',
    maintainer_email='huawei@example.com',
    description='NLP Robot Commander using Qwen and ROS 2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
    'command_listener = robot_commander.command_listener:main',
    'robot_controller = robot_commander.robot_controller:main',
    'command_interface = robot_commander.command_interface:main',
],
    },
)
