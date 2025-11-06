###
### It launches main robot components and utility nodes for the Bunker Pro robot for recording the data at CERZOO facility during the study of robot-animal interaction.
### Mattia Dutto
###

### Instructions:
### - Add the references to your heart rate monitor node here.
### - Configure the right parameters for the RealSense camera.
### - If you want add ros2 bag node here.
### - Compile (colcon build && . install/setub.bash).
### - Launch the node of the camera on the pole, this will be just rgb no depth / no stereo / no pointcloud, so should be easy to send and receive the data. An alternative can be the usage of an IP cam and connecting via ROS to that camera. If we want to do everything in the easiest way, we can connect the camera to the laptop and record on the local SSD the data. In the worst case after each day you copy the data from the laptop to the SSD.
### - Launch this node.
### - If you didn't add ros2 bag, lauch the bag recording. For saving the data directly to the SSD, you should pass to the node -o /path/to/the/ssd. You should also test this for avoid that the system will overload and you will have issue with the topics.


import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_name = "ugv_utils"

    ### STATIC TF
    ### This TF are calculated using the ITEM sensor castle mounted with the shovel on the robot.
    ### For the IMU we don't need any TF the IMU node is already creating the TF.
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
        launch_arguments={
            "rgb_camera.color_profile": "1920x1080x30",
            "depth_module.depth_profile": "1280x720x30",
            "depth_module.infra_profile": "1280x720x30",
            "pointcloud.enable": "true",
        }.items(),
    )

    ### IMU
    pkg_imu = get_package_share_directory("microstrain_inertial_driver")

    imu_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_imu, "launch", "microstrain_launch.py")
        ),
        launch_arguments={}.items(),
    )

    ### POLAR SENSORS

    ld = LaunchDescription()
    # Launch options
    # TFs
    ld.add_action(transform_camera_node)
    # Utily nodes
    ld.add_action(twist_mux_node)
    # Driver nodes
    ld.add_action(bunker_base_cmd)
    ld.add_action(camera_cmd)
    ld.add_action(imu_cmd)
    # Custom nodes

    return ld
