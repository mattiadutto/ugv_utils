###
### It launches main robot components and utility nodes for the Bunker Pro robot in the feeding operation.
### Mattia Dutto
###

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition, LaunchConfigurationEquals
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_name = "ugv_utils"

    ekf_params_file = LaunchConfiguration(
        "ekf_params_file", default="ekf_localization_with_gps.yaml"
    )
    lidar_3d = LaunchConfiguration("lidar_3d", default="true")
    map_name = LaunchConfiguration("map_name", default="workshop_big.yaml")
    nav2_params_file = LaunchConfiguration(
        "nav2_params_file", default="nav2_params_bunker.yaml"
    )
    use_camera = LaunchConfiguration("use_camera", default="false")
    use_gps = LaunchConfiguration("use_gps", default="false")

    declare_ekf_params_file_arg = DeclareLaunchArgument(
        "ekf_params_file",
        default_value=ekf_params_file,
        description="ekf parameter configuration saved in src/scout_navigation/config",
    )
    declare_lidar_3d_arg = DeclareLaunchArgument(
        "lidar_3d",
        default_value=lidar_3d,
        description="true if you want to use Velodyne otherwise RPLidar A3",
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
    declare_use_camera_arg = DeclareLaunchArgument(
        "use_camera", default_value=use_camera, description="usage of the camera"
    )
    declare_use_gps_arg = DeclareLaunchArgument(
        "use_gps", default_value=use_gps, description="usage of the gps"
    )

    ### STATIC TF
    ### This TF are calculated using the ITEM sensor castle mounted with the shovel on the robot.
    ### For the IMU we don't need any TF the IMU node is already creating the TF.
    transform_camera_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "0.019",
            "-0.125",
            "0.205",
            "-1.57",
            "0",
            "0",
            "base_link",
            "camera_link",
        ],
        condition=LaunchConfigurationEquals("use_camera", "true"),
    )

    transform_gps_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["0.139", "0.209", "0.313", "0", "0", "0", "base_link", "gps"],
        condition=LaunchConfigurationEquals("use_gps", "true"),
    )

    transform_lidar_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "0.019",
            "0",
            "0.384" if lidar_3d else "0.381",
            "0",
            "0",
            "0",
            "base_link",
            "velodyne" if lidar_3d else "laser",
        ],
    )

    ### TWIST MUX
    # File with twist_mux params
    twist_mux_params = os.path.join(
        get_package_share_directory(package_name), "config", "twist_mux_real.yaml"
    )

    twist_mux_node = Node(
        package="twist_mux",
        executable="twist_mux",
        output="screen",
        remappings={("/cmd_vel_out", "/cmd_vel")},
        parameters=[twist_mux_params],
    )

    ### STATE PUBLISHER
    # For using this you need the ugv_gazebo_sim packege installed.
    # pkg_bunker_publisher = get_package_share_directory("bunker_gazebo_sim")

    # robot_state_publisher_cmd = IncludeLaunchDescription(
    #     os.path.join(pkg_bunker_publisher, "launch", "bunker_robot_state_publisher.launch.py"),
    #     launch_arguments={
    #         "use_sim_time": LaunchConfiguration('use_sim_time'),
    #         "namespace": namespace
    #     }.items(),
    # )

    ### BUNKER BASE
    pkg_bunker_base = get_package_share_directory("bunker_base")

    bunker_base_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_bunker_base, "launch", "bunker_base.launch.py")
        ),
        launch_arguments={}.items(),
    )

    ### CAMERA
    pkg_camera = get_package_share_directory("realsense2_camera")

    camera_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_camera, "launch", "rs_launch.py")
        ),
        condition=LaunchConfigurationEquals("use_camera", "true"),
        launch_arguments={
            "rgb_camera.color_profile": "1920x1080x30",
            "depth_module.depth_profile": "1280x720x30",
            "depth_module.infra_profile": "1280x720x30",
            "align_depth.enable": "true",
            "pointcloud.enable": "true",
        }.items(),
    )

    ### GPS
    pkg_gps = get_package_share_directory("nmea_navsat_driver")

    gps_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gps, "launch", "nmea_serial_driver.launch.py")
        ),
        condition=LaunchConfigurationEquals("use_gps", "true"),
    )

    ### IMU
    pkg_imu = get_package_share_directory("microstrain_inertial_driver")

    imu_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_imu, "launch", "microstrain_launch.py")
        ),
        launch_arguments={}.items(),
    )

    ### LIDAR
    pkg_lidar = get_package_share_directory("velodyne")

    velodyne_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_lidar, "launch", "velodyne-all-nodes-VLP16-launch.py")
        ),
        condition=LaunchConfigurationEquals("lidar_3d", "true"),
    )

    pkg_lidar = get_package_share_directory("rplidar_ros2")

    rplidar_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_lidar, "launch", "view_rplidar_a3_launch.py")
        ),
        condition=LaunchConfigurationEquals("lidar_3d", "false"),
        launch_arguments={"use_rviz": "false"}.items(),
    )

    ### NAV2 Stack
    pkg_nav2 = get_package_share_directory("scout_navigation")

    nav2_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2, "launch", "nav2.launch.py")
        ),
        launch_arguments={
            "use_sim_time": "false",
            "use_rviz": "false",
            "map_name": map_name,
            "namespace": "",
            "ekf_params_file": ekf_params_file,
            "nav2_params_file": nav2_params_file,
            "rviz_params_file": "",
        }.items(),
    )

    ld = LaunchDescription()
    # Launch options
    ld.add_action(declare_ekf_params_file_arg)
    ld.add_action(declare_lidar_3d_arg)
    ld.add_action(declare_map_name_arg)
    ld.add_action(declare_nav2_params_file_arg)
    ld.add_action(declare_use_camera_arg)
    ld.add_action(declare_use_gps_arg)
    # TFs
    ld.add_action(transform_camera_node)
    # ld.add_action(transform_gps_node)
    ld.add_action(transform_lidar_node)
    # Utily nodes
    ld.add_action(twist_mux_node)
    # ld.add_action(robot_state_publisher_cmd)
    # Driver nodes
    ld.add_action(bunker_base_cmd)
    ld.add_action(camera_cmd)
    # ld.add_action(gps_cmd)
    ld.add_action(imu_cmd)
    ld.add_action(rplidar_cmd)
    ld.add_action(velodyne_cmd)
    # Nav2
    ld.add_action(nav2_cmd)

    return ld
