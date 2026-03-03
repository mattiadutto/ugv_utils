###
### It launches utility nodes for the scout mini robot.
### Mattia Dutto
###

import os
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    pkg_name = "ugv_utils"
    namespace = "scout_mini"
    use_sim_time = "true"

    map_name = LaunchConfiguration("map_name", default="warehouse.yaml")
    nav2_params_file = LaunchConfiguration(
        "nav2_params_file", default="nav2_params.yaml"
    )
    nav2_rviz_file = LaunchConfiguration(
        "nav2_rviz_file", default="scout_mini_navigation.rviz"
    )

    declare_map_name_arg = DeclareLaunchArgument(
        "map_name",
        default_value=map_name,
        description="name of the map saved in src/scout_navigation/maps",
    )

    declare_nav2_params_file_arg = DeclareLaunchArgument(
        "nav2_params_file",
        default_value=nav2_params_file,
        description="nav2 parameter configuration saved in src/scout_navigation/config",
    )

    declare_nav2_rviz_file_arg = DeclareLaunchArgument(
        "nav2_rviz_file",
        default_value=nav2_rviz_file,
        description="nav2 parameter configuration saved in src/scout_navigation/rviz",
    )

    ### Scout Mini
    scout_gazebo_sim_cmd = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("scout_gazebo_sim"),
            "launch",
            "scout_mini_empty_world.launch.py",
        ),
        launch_arguments={"use_rviz": "false", "yaw_pose": "0.0"}.items(),
    )

    ### NAV2 Stack
    pkg_nav2 = get_package_share_directory("scout_navigation")

    nav2_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2, "launch", "nav2.launch.py")
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "use_rviz": "true",
            "map_name": map_name,
            "namespace": namespace,
            "nav2_params_file": nav2_params_file,
            "rviz_params_file": nav2_rviz_file,
        }.items(),
    )


    ld = LaunchDescription()
    # Lauch options
    ld.add_action(declare_map_name_arg)
    ld.add_action(declare_nav2_params_file_arg)
    ld.add_action(declare_nav2_rviz_file_arg)
    # Sim
    ld.add_action(scout_gazebo_sim_cmd)
    # Nav2
    # ld.add_action(nav2_cmd)

    return ld
