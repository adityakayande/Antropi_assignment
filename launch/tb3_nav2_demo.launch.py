"""One-command demo: Gazebo + TurtleBot3 + Nav2 (with our map) + RViz."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

# Find our map and script relative to this file, so the repo works anywhere.
HERE = os.path.dirname(os.path.realpath(__file__))
PROJECT = os.path.dirname(HERE)
MAP_YAML = os.path.join(PROJECT, 'maps', 'tb3_world_map_v2.yaml')
STAMPER = os.path.join(PROJECT, 'scripts', 'cmd_vel_stamper.py')


def generate_launch_description():
    tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    nav2_bringup = get_package_share_directory('nav2_bringup')

    # 1. Gazebo world with the TurtleBot3 robot
    gazebo = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(tb3_gazebo, 'launch', 'turtlebot3_world.launch.py')))

    # 2. Nav2 stack, loading OUR saved map, following Gazebo's clock
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup, 'launch', 'bringup_launch.py')),
        launch_arguments={'map': MAP_YAML, 'use_sim_time': 'true'}.items())

    # 3. Converter: Nav2's Twist -> the robot's TwistStamped
    stamper = ExecuteProcess(
        cmd=['python3', STAMPER, '--ros-args', '-p', 'use_sim_time:=true'],
        output='screen')

    # 4. RViz with Nav2's preset layout
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(nav2_bringup, 'launch', 'rviz_launch.py')))

    # Give Gazebo a head start before the rest, so Nav2 finds the clock and robot.
    return LaunchDescription([
        gazebo,
        TimerAction(period=8.0, actions=[nav2, stamper, rviz]),
    ])
