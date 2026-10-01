###
### It launches utility nodes for the scout mini robot.
### Mattia Dutto  
###

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = "ugv_utils"
    
    ### STATIC TF
    
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
    
    ld.add_action(twist_mux_node)
    
    return ld