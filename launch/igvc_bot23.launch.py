import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import RegisterEventHandler
from launch.events.process import ProcessStarted
from launch.event_handlers.on_process_start import OnProcessStart
from launch import LaunchContext

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_file_name = 'urdf/vikram_igvc.urdf'
    urdf = os.path.join(
        get_package_share_directory('igvc_sim'),
        urdf_file_name)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    position = [0.0,0.0,0.2]
    orientation = [0.0,0.0,0.0]


    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf]),
        
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity','igvc_bot',
                       '-x',str(position[0]),
                       '-y',str(position[1]),
                       '-z',str(position[2]),
                       '-R',str(orientation[0]),
                       '-P',str(orientation[1]),
                       '-Y',str(orientation[2]),
                       '-topic','/robot_description'],
            output='screen'
        ),
        Node(package = "tf2_ros",
            name="map_tf_broadcaster", 
            executable = "static_transform_publisher",
            arguments = ["1", "0", "0", "0", "0", "0", "1", "map", "odom"]),
        Node(package = "tf2_ros",
            name="base_footprint_tf_broadcaster", 
            executable = "static_transform_publisher",
            arguments = ["0", "0", "0", "0", "0", "0", "1", "base_footprint", "base_link"]),
        Node(package = "tf2_ros", 
            name="castor_cylinder_tf_broadcaster",
            executable = "static_transform_publisher",
            arguments = ["-0.609078", "-0.008" ,"-0.1", "0", "0", "0", "1", "base_link", "castor_cylinder"]),
        Node(package = "tf2_ros", 
            name="castor_ball_tf_broadcaster",
            executable = "static_transform_publisher",
            arguments = ["0", "-0" ,"-0.065", "0", "0", "0", "1", "castor_cylinder", "castor_ball"]),
    ])
    