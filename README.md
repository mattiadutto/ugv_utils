## UGV UTILS
This repository contains a set of launch files that are useful for the robot or simulation usage:
- **box_filter_scout_mini.launch.py**: it remove the laser point inside the footprint of the robot from the scan topic and publish on scan_filtered topic.
- **bunker_real.launch.py**: it creates the static transform for the GPS and the IMU sensors, it launch the twist_mux for the cmd_vel
- **scout_mini_real.launch.py**: it launch the twist_mux for the cmd_vel

Configuration files:
- **laser_filter_scout_mini.yaml**: configuration file for the box_filter_scout_mini.launch.py
- **twist_mux_real.yaml**: configuration file for the twist_mux node used on the bunker_real and scout_mini_real launch files.
