from launch import LaunchDescription, LaunchContext
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler, OpaqueFunction, ExecuteProcess
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
    gazebo_path = PythonLaunchDescriptionSource([
            PathJoinSubstitution([FindPackageShare("natsu24"),"launch","gazebo.launch.py"])
            ])
    world_path = PathJoinSubstitution([FindPackageShare("natsu24"),"world","natsu24.world"])
    
    gazebo_launch = IncludeLaunchDescription(gazebo_path, 
                    launch_arguments = {
                        'world_path': world_path,
                        'spawn_x': '2.983',
                        'spawn_y': '0.25',
                        #'spawn_x': '1.75',
                        #'spawn_y': '3.0',
                        'spawn_yaw': '-1.571'
                    }.items())
    
    node_natsu24 = Node(
        package="natsu24",
        executable="natsu24",
        output="both",
    )
    
    nodes = [
        gazebo_launch,
        #node_natsu24
    ]
    
    return LaunchDescription(nodes)