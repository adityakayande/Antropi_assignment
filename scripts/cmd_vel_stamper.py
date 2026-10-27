#!/usr/bin/env python3
"""Converts Nav2's Twist velocity commands into TwistStamped.

Jazzy's TurtleBot3 Gazebo bridge expects TwistStamped on /cmd_vel,
but Nav2 publishes plain Twist. This node bridges the two.
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped


class CmdVelStamper(Node):
    def __init__(self):
        super().__init__('cmd_vel_stamper')
        self.pub = self.create_publisher(TwistStamped, 'cmd_vel', 10)
        self.sub = self.create_subscription(
            Twist, 'cmd_vel_smoothed', self.on_twist, 10)

    def on_twist(self, msg: Twist):
        out = TwistStamped()
        out.header.stamp = self.get_clock().now().to_msg()
        out.header.frame_id = 'base_link'
        out.twist = msg
        self.pub.publish(out)


def main():
    rclpy.init()
    node = CmdVelStamper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
