###
### It launches utility nodes for the bunker robot.
### Mattia Dutto  
###

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = "ugv_utils"
    
    ### STATIC TF
    ### TF based on the main castle of sensors.
    transform_gps_node = Node(
        package = "tf2_ros", 
        executable = "static_transform_publisher",
        arguments = ["0.12", "0.209", "0.313", "0", "0", "0", "base_link", "gps"]
    ) 
    
    transform_imu_node = Node(
        package = "tf2_ros", 
        executable = "static_transform_publisher",
        arguments = ["0","0","0","0","0","0", "base_link", "imu"]
    )
    
    ### TWIST MUX
    # File with twist_mux params
    twist_mux_params = os.path.join(
        get_package_share_directory(pkg_name), "config", "twist_mux_real.yaml"
    )
    
    twist_mux_node = Node(
        package="twist_mux",
        executable="twist_mux",
        output="screen",
        remappings={("/cmd_vel_out", "/cmd_vel")},
        parameters=[twist_mux_params],
    )
    
    ld = LaunchDescription()
    
    ld.add_action(transform_gps_node)
    ld.add_action(transform_imu_node)
    
    ld.add_action(twist_mux_node)
    
    return ld