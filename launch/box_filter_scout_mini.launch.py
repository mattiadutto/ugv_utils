###
### Laser filter on the scout mini shape.
### This node can be used both on simulation and on the real robot, we just have to 
### adjust the namespace value.
### Mattia Dutto  
###

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = "ugv_utils"
    
    namespace = LaunchConfiguration("namespace", default="")
    
    declare_namespace_arg = DeclareLaunchArgument(
        "namespace", 
        default_value=namespace,
        description="Namespace of the robot for simulation usage."
    )
    
    laser_filter_params_file_path = PathJoinSubstitution(
        [get_package_share_directory(pkg_name), "config", "laser_filter_scout_mini.yaml"]
    )
    
    laser_filer_node = Node(
        package="laser_filters",
        executable="scan_to_scan_filter_chain",
        name="scan_to_scan_filter_chain",
        parameters=laser_filter_params_file_path,
        remappings=[("/tf", f"{namespace}/tf"), 
                    ("/tf_static", f"{namespace}/tf_static"),
                    ("/scan", f"{namespace}/scan"),
                    ("/scan_filtered", f"{namespace}/scan_filtered")
                    ]
        )
    
    ld = LaunchDescription()
    
    ld.add_action(declare_namespace_arg)
    
    ld.add_action(laser_filter_node)
    
    return ld