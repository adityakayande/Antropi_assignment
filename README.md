# TurtleBot3 + Nav2 Autonomous Navigation (ROS 2 Jazzy, Gazebo)

A TurtleBot3 (waffle) navigates autonomously in Gazebo using the Nav2 stack,
on a map I built myself with SLAM, and avoids obstacles that are not on the saved map.

**Demo video:** https://youtu.be/0-hTNBYF0GI

![Map](maps/tb3_world_map_v2.png)

## What's in this repo
| Path | Purpose |
|---|---|
| `launch/tb3_nav2_demo.launch.py` | One command starts Gazebo, Nav2 (with my map), the velocity converter, and RViz |
| `maps/` | Map built with slam_toolbox (`.pgm`, `.yaml`, `.png`) |
| `scripts/cmd_vel_stamper.py` | Converts Nav2's `Twist` commands to the `TwistStamped` the robot expects |
| `scripts/spawn_obstacle.sh` | Spawns a box that is not in the saved map |
| `config/slam.rviz` | RViz layout used while mapping |

## Requirements
- Ubuntu 24.04, ROS 2 Jazzy (desktop install)
- Packages:
```
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup "ros-jazzy-nav2-minimal-tb*" \
  ros-jazzy-ros-gz ros-jazzy-turtlebot3-gazebo ros-jazzy-turtlebot3-teleop ros-jazzy-slam-toolbox
```

## Run
```
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=waffle
ros2 launch launch/tb3_nav2_demo.launch.py
```
1. Wait for Gazebo and RViz to open (can take 1-2 minutes, especially on WSL).
2. **Set the initial pose first**: click *2D Pose Estimate* in RViz on the robot, drag in the direction it faces. Nav2 navigation stays inactive until AMCL has a pose.
3. When the Navigation panel shows *active*, click *Nav2 Goal* and pick a free spot.

## Obstacle test
With the demo running:
```
./scripts/spawn_obstacle.sh 1.5 0.0
```
The box appears in the local costmap but not in the saved map. Send a goal behind it and the path bends around it.

## How it works
Obstacle avoidance comes from Nav2 itself: the static, obstacle and inflation costmap layers,
the global planner (route) and the local controller (live steering). No custom navigation
algorithm is used.

## Known issue and fix
In Jazzy, the TurtleBot3 Gazebo bridge subscribes to `/cmd_vel` as `TwistStamped`, while Nav2
publishes plain `Twist`. ROS 2 silently refuses to connect mismatched types, so Nav2 planned
and drove in RViz while the robot sat still in Gazebo. `scripts/cmd_vel_stamper.py` republishes
Nav2's output with a timestamp, which fixes it.

## Notes
- Map built by driving slowly around the arena with `slam_toolbox` and saving with `map_saver_cli`.
- Tested on Windows 11 + WSL2 (Ubuntu 24.04).
