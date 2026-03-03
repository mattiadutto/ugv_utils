import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = "ugv_utils"
    
    # Robot
    pkg_bunker_base = get_package_share_directory("bunker_base")
    
    bunker_base_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_bunker_base, "launch", "bunker_base.launch.py")
        ),
    )
    
    # Robot IMU
    pkg_imu = get_package_share_directory("microstrain_inertial_driver")

    imu_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_imu, "launch", "microstrain_launch.py")
        ),
        launch_arguments={}.items(),
    )
    
    # Robot camera
    pkg_camera = get_package_share_directory("realsense2_camera")

    camera_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_camera, "launch", "rs_launch.py")
        ),
        launch_arguments={
            "rgb_camera.color_profile": "848x480x5",
            "depth_module.depth_profile": "848x480x5",
            # "depth_module.infra_profile": "1280x720x15",
            "align_depth.enable": "true",
            "pointcloud.enable": "true",
            "pointcloud.ordered_pc": "true"
        }.items(),
    )
    
    # Static TF
    transform_imu_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "base_link",
            "imu_link",
        ]    
    )
    
    transform_camera_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "base_link",
            "camera_link",
        ]    
    )
    
    
    
    # Polar H10 - 1
    pkg_polar = get_package_share_directory("polar_h10")

    polar_one = "00000000"

    polar_one_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_polar, "launch", "polar_multisensor_launch.py")
        ),
        launch_arguments={"sensor_address": polar_one}.items(),
    )
    
    polar_two = "00000000"

    polar_two_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_polar, "launch", "polar_multisensor_launch.py")
        ),
        launch_arguments={"sensor_address": polar_two}.items(),
    )
    
    polar_three = "00000000"

    polar_three_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_polar, "launch", "polar_multisensor_launch.py")
        ),
        launch_arguments={"sensor_address": polar_three}.items(),
    )
    
    polar_four = "00000000"

    polar_four_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_polar, "launch", "polar_multisensor_launch.py")
        ),
        launch_arguments={"sensor_address": polar_four}.items(),
    )
    
    ld = LaunchDescription()
    
    ld.add_action(bunker_base_cmd)
    ld.add_action(imu_cmd)
    ld.add_action(camera_cmd)
    
    ld.add_action(transform_imu_node)
    ld.add_action(transform_camera_node)
    
    ld.add_action(polar_one_cmd)
    ld.add_action(polar_two_cmd)
    ld.add_action(polar_three_cmd)
    ld.add_action(polar_four_cmd)
    
    return ld