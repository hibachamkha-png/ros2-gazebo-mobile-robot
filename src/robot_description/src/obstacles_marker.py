#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray


class ObstaclesMarker(Node):

    def __init__(self):
        super().__init__('obstacles_marker')

        self.publisher = self.create_publisher(
            MarkerArray,
            '/obstacles',
            10
        )

        self.timer = self.create_timer(1.0, self.publish_obstacles)

    def publish_obstacles(self):

        markers = MarkerArray()

        # Cone 1
        cone1 = Marker()
        cone1.header.frame_id = 'odom'
        cone1.header.stamp = self.get_clock().now().to_msg()
        cone1.ns = 'obstacles'
        cone1.id = 1
        cone1.type = Marker.CYLINDER
        cone1.action = Marker.ADD

        cone1.pose.position.x = 2.0
        cone1.pose.position.y = 0.0
        cone1.pose.position.z = 0.5

        cone1.scale.x = 0.5
        cone1.scale.y = 0.5
        cone1.scale.z = 1.0

        cone1.color.r = 1.0
        cone1.color.g = 0.5
        cone1.color.b = 0.0
        cone1.color.a = 1.0

        # Cone 2
        cone2 = Marker()
        cone2.header.frame_id = 'odom'
        cone2.header.stamp = self.get_clock().now().to_msg()
        cone2.ns = 'obstacles'
        cone2.id = 2
        cone2.type = Marker.CYLINDER
        cone2.action = Marker.ADD

        cone2.pose.position.x = -2.0
        cone2.pose.position.y = 1.0
        cone2.pose.position.z = 0.5

        cone2.scale.x = 0.5
        cone2.scale.y = 0.5
        cone2.scale.z = 1.0

        cone2.color.r = 1.0
        cone2.color.g = 0.5
        cone2.color.b = 0.0
        cone2.color.a = 1.0

        markers.markers.append(cone1)
        markers.markers.append(cone2)

        self.publisher.publish(markers)


def main(args=None):
    rclpy.init(args=args)

    node = ObstaclesMarker()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

