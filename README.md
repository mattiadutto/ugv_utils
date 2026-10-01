## UGV UTILS

| File | Description | Distribution |
| -- | -- | -- |
| config/laser_filter_scout_mini.yaml | Configuration file for box_filter_scout_mini.launch.py | Humble |
| config/twist_mux_real.yaml | Configuration file for the twist_mux node used on teh bunker_real and scout_mini_real launch files | Humble |
| launch/bunker_real_cerzoo.launch.py | Launch the nodes for the Agilex Bunker Pro, IMU, Realsense camera and twist mux. | Jazzy |
| launch/bunker_real.launch.py | Launch the nodes for the Agilex Bunker Pro, IMU, Realsense camera, GPS, LiDAR (RPLidar A3 or Velodyne VLP-16), twist mux and nav2. | Humble |
| launch/scout_mini_real_box_filter.launch.py | Launch file for launching box filter that is basically removing all the points around the LiDAR | Humble |
| launch/scout_mini_fve.launch.py | Launch the nodes Agilex Scout Mini, Realsese Camera, Robosense LiDAR for food volume estimation (*this project was interropted so we can consider to remove this file*) | Humble |
| launch/scout_mini.launch.py | Launch the simulation for the Agilex Scout Mini with Nav2 and feeding nodes | Humble |
| launch/twist_mux.launch.py | Launch the twist_mux node | Humble |
| utils/convert_bag_to_mat.py | Example on the /scan topic for converting a bag file to matlab file | - |
