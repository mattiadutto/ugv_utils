import os
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    package_name = "ugv_utils"

    topic_status = LaunchConfiguration("topic_status", default="/system_status")

    system_monitor_params = LaunchConfiguration(
        "system_monitor_params_file", default="params_system_monitor.yaml"
    )

    declare_topic_status_arg = DeclareLaunchArgument(
        "topic_status",
        default_value=topic_status,
        description="Name of the topic where the robot status [CPU, RAM and BATTERY] will be publish",
    )

    declare_system_monitor_params_arg = DeclareLaunchArgument(
        "system_monitor_params_file",
        default_value=system_monitor_params,
        description="Name of the file of system monitor parameters",
    )

    node_rosbridge_server = Node(
        package="rosbridge_server", executable="rosbridge_websocket", output="screen"
    )

    system_monitor_params = PathJoinSubstitution(
        [
            get_package_share_directory("system_monitor"),
            "config",
            system_monitor_params,
        ]
    )

    node_system_monitor = Node(
        package="system_monitor",
        executable="system_monitor_exe",
        output="screen",
        parameters=[system_monitor_params],
    )

    node_web_video_server = Node(
        package="web_video_server", executable="web_video_server", output="screen"
    )

    ld = LaunchDescription()

    ld.add_action(declare_topic_status_arg)
    ld.add_action(declare_system_monitor_params_arg)

    ld.add_action(node_rosbridge_server)
    ld.add_action(node_system_monitor)
    ld.add_action(node_web_video_server)

    return ld
