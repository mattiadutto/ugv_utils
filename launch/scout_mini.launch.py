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

    map_name = LaunchConfiguration("map_name", default="workshop_big_empty_slam.yaml")
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
            "scout_mini_workshop_world.launch.py",
        ),
        launch_arguments={"use_rviz": "true", "yaw_pose": "0.0"}.items(),
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

    # nav2_cmd = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(pkg_nav2, "launch", "nav2_speed_limit.launch.py")
    #     ),
    #     launch_arguments={
    #         "use_sim_time": use_sim_time,
    #         "use_rviz": "true",
    #         "map_name": map_name,
    #         "namespace": namespace,
    #         "nav2_params_file": nav2_params_file,
    #         "rviz_params_file": nav2_rviz_file,
    #         "speed_map_name": "workshop_big_empty_slam_speed_limit.yaml",
    #     }.items(),
    # )

    ### Feeding nodes.
    lidar_distance_node = Node(
        package="lidar_distance",
        executable="lidar_distance",
        name="lidar_distance",
        parameters=[
            PathJoinSubstitution(
                [
                    get_package_share_directory("lidar_distance"),
                    "config",
                    "params_lidar_distance.yaml",
                ]
            )
        ],
        remappings=[
            ("/tf", f"{namespace}/tf"),
            ("/tf_static", f"{namespace}/tf_static"),
        ],
        output="screen",
    )

    follow_waypoints_params = os.path.join(
        get_package_share_directory("follow_waypoints"),
        "config",
        "params_follow_line.yaml",
    )

    file = open(follow_waypoints_params)

    data = yaml.safe_load(file)["follow_line"]["ros__parameters"]

    follow_waypoints_node = Node(
        package="follow_waypoints",
        executable="follow_line_exe",
        output="screen",
        parameters=[data],
    )

    ld = LaunchDescription()
    # Lauch options
    ld.add_action(declare_map_name_arg)
    ld.add_action(declare_nav2_params_file_arg)
    ld.add_action(declare_nav2_rviz_file_arg)
    # Sim
    ld.add_action(scout_gazebo_sim_cmd)
    # Nav2
    ld.add_action(nav2_cmd)
    # Feeding
    # ld.add_action(lidar_distance_node)
    # ld.add_action(follow_waypoints_node)
    return ld
