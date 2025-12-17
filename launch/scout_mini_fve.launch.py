###
### It launches utility nodes for the scout mini robot with realsense camera and robosense lidar.
### Mattia Dutto  
###

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = "ugv_utils"
    
    ### STATIC TF
    transform_camera_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "0",
            "-0.125",
            "0.36",
            "-1.57",
            "0",
            "0",
            "base_link",
            "camera_link",
        ],
    )
    
    transform_lidar_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "0",
            "0",
            "0.435",
            "0",
            "0",
            "0",
            "base_link",
            "rslidar",
        ],
    )
    
    ### SCOUT BASE
    pkg_scout_base = get_package_share_directory("scout_base")

    scout_base_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_scout_base, "launch", "scout_mini_base.launch.py")
        ),
        launch_arguments={}.items(),
    )
    
    ### CAMERA
    pkg_camera = get_package_share_directory("realsense2_camera")

    camera_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_camera, "launch", "rs_launch.py")
        ),
        launch_arguments={
            "rgb_camera.color_profile": "1280x720x15",
            "depth_module.depth_profile": "1280x720x15",
            # "depth_module.infra_profile": "1280x720x15",
            "align_depth.enable": "true",
            "pointcloud.enable": "true",
            "pointcloud.ordered_pc": "true"
        }.items(),
    )
    
    # ros2 launch realsense2_camera rs_launch.py align_depth.enable:=True pointcloud.enable:=True depth_module.depth_profile:=1280x720x30 pointcloud.ordered_pc:=true
    
    pkg_lidar = get_package_share_directory("rslidar_sdk")

    rplidar_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_lidar, "launch", "start.py")
        )
    )
    
    ld = LaunchDescription()
    
    # Launch options
    # TFs
    ld.add_action(transform_camera_node)
    ld.add_action(transform_lidar_node)
    # Utility nodes 
    # Driver nodes
    ld.add_action(scout_base_cmd)
    ld.add_action(camera_cmd)
    ld.add_action(rplidar_cmd)
    # Nav2
    
    return ld