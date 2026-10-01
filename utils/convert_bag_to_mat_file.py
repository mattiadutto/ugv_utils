import sys
import rosbag2_py

from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
from tf_transformations import euler_from_quaternion
from scipy.io import savemat

from sensor_msgs.msg import LaserScan

# Variables
bag_time = []
laser_data = []

# Matlab dictionary
matlab_dic = {}

# Open the bag
storage_options = rosbag2_py.StorageOptions(uri=sys.argv[1], storage_id="sqlite3")
converter_options= rosbag2_py.ConverterOptions(input_serialization_format="cdr", output_serialization_format="cdr")

reader = rosbag2_py.SequentialReader()
reader.open(storage_options, converter_options)

topic_types = reader.get_all_topics_and_types()

type_map = {t.name: t.type for t in topic_types}

t0 = -1

while reader.has_next():
    (topic, data, t) = reader.read_next()
    msg_type = get_message(type_map[topic])
    msg = deserialize_message(data, msg_type)
    
    if t0 < 0:
        t0 = t
        
    if isinstance(msg, LaserScan) and topic == "/scout_mini/scan_edited":
        bag_time.append((t-t0) * 1e-9)
        
        laser_data.append(msg.ranges)
        
        matlab_dic.update({"laser_data": laser_data, "bag_time": bag_time})
        
savemat(sys.argv[1][:-4]+".mat", matlab_dic)
