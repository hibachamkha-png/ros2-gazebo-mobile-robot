
import os
import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    # Chemin du package robot_description
    pkg_path = get_package_share_directory('robot_description')

    # Fichier du robot
    xacro_file = os.path.join(
        pkg_path,
        'model',
        'robot.xacro'
    )

    # Monde Gazebo original
    world_file = os.path.join(
    pkg_path,
    'worlds',
    'cone_world.world'
)
    # Vérifier que les fichiers existent
    if not os.path.isfile(xacro_file):
        raise FileNotFoundError(
            f"Fichier robot.xacro introuvable : {xacro_file}"
        )

    if not os.path.isfile(world_file):
        raise FileNotFoundError(
            f"Fichier empty_world.world introuvable : {world_file}"
        )

    # Convertir le fichier Xacro en URDF
    robot_description = xacro.process_file(xacro_file).toxml()

    # Lancer Gazebo avec le monde original
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

    # Publier la description du robot
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description
            }
        ]
    )

    # Ajouter le robot dans Gazebo
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


