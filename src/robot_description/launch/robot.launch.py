import os
import xacro

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Package path
    pkg_path = get_package_share_directory(
        'robot_description'
    )


    # Xacro file
    xacro_file = os.path.join(
        pkg_path,
        'model',
        'robot.xacro'
    )


    # World file
    world_file = os.path.join(
        pkg_path,
        'model',
        'empty_world.world'
    )


    # Convert xacro to URDF
    robot_description = xacro.process_file(
        xacro_file
    ).toxml()



    # Launch Gazebo with world
    gazebo = IncludeLaunchDescription(

        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),

        launch_arguments={
            'world': world_file
        }.items()

    )



    # Robot state publisher
    robot_state_publisher = Node(

        package='robot_state_publisher',

        executable='robot_state_publisher',

        parameters=[
            {
                'robot_description': robot_description
            }
        ],

        output='screen'

    )



    # Spawn robot from robot_description topic
    spawn_robot = Node(

        package='gazebo_ros',

        executable='spawn_entity.py',

        arguments=[

            '-entity',
            'mobile_robot',

            '-topic',
            'robot_description'

        ],

        output='screen'

    )



    return LaunchDescription([

        gazebo,

        robot_state_publisher,

        spawn_robot

    ])
