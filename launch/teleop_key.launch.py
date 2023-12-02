from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    ld = LaunchDescription()
    
    test_node = Node(
        package="igvc_sim",
        executable="teleop_key.py",
        output='screen'
    )
    
    ld.add_action(test_node)
    
    return ld