import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_file_name = 'urdf/igvc24_bot.urdf'
    urdf = os.path.join(
        get_package_share_directory('igvc_sim'),
        urdf_file_name)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    position = [0.0,0.0,0.2]
    orientation = [0.0,0.0,0.0]

    from launch_ros.substitutions import FindPackageShare
    pkg_share = FindPackageShare(package='igvc_sim').find('igvc_sim')
    gazebo_models_path = os.path.join(pkg_share, 'meshes/igvc24/')
    os.environ["GAZEBO_MODEL_PATH"] = gazebo_models_path

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
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf]
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            output="screen" ,
            arguments=["0", "0", "0", "0", "0", "0", "map", "odom"]
        ),

    ])