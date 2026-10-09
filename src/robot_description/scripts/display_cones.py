#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point


class DisplayCones(Node):
    def __init__(self):
        super().__init__('display_cones')
        self.publisher = self.create_publisher(
            MarkerArray, '/cone_markers', 10
        )
        self.timer = self.create_timer(1.0, self.publish_cones)

    def make_marker(self, marker_id, x, y, marker_type):
        marker = Marker()
        marker.header.frame_id = 'odom'
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = 'traffic_cones'
        marker.id = marker_id
        marker.type = marker_type
        marker.action = Marker.ADD
        marker.pose.position.x = x
        marker.pose.position.y = y
        marker.pose.orientation.w = 1.0
        marker.color.a = 1.0
        return marker

    def make_cone_surface(self, marker_id, x, y, z1, r1, z2, r2, color):
        marker = self.make_marker(
            marker_id, x, y, Marker.TRIANGLE_LIST
        )

        # Echelle non nulle pour RViz2
        marker.scale.x = 1.0
        marker.scale.y = 1.0
        marker.scale.z = 1.0

        marker.color.r, marker.color.g, marker.color.b = color
        segments = 32

        for i in range(segments):
            a1 = 2.0 * math.pi * i / segments
            a2 = 2.0 * math.pi * (i + 1) / segments

            p1 = Point(x=r1 * math.cos(a1), y=r1 * math.sin(a1), z=z1)
            p2 = Point(x=r1 * math.cos(a2), y=r1 * math.sin(a2), z=z1)
            p3 = Point(x=r2 * math.cos(a1), y=r2 * math.sin(a1), z=z2)
            p4 = Point(x=r2 * math.cos(a2), y=r2 * math.sin(a2), z=z2)

            marker.points.extend([p1, p2, p3, p2, p4, p3])

        return marker


    def publish_cones(self):
        markers = MarkerArray()
        cones = [(1, 2.0, 0.0), (10, -2.0, 1.0)]

        for base_id, x, y in cones:
            base = self.make_marker(
                base_id, x, y, Marker.CYLINDER
            )
            base.pose.position.z = 0.06
            base.scale.x = 0.50
            base.scale.y = 0.50
            base.scale.z = 0.12
            base.color.r = 0.05
            base.color.g = 0.05
            base.color.b = 0.05
            markers.markers.append(base)

            # Partie orange inferieure
            markers.markers.append(self.make_cone_surface(
                base_id + 1, x, y, 0.12, 0.21, 0.34, 0.15,
                (1.0, 0.30, 0.0)
            ))

            # Bande blanche
            markers.markers.append(self.make_cone_surface(
                base_id + 2, x, y, 0.34, 0.15, 0.43, 0.125,
                (1.0, 1.0, 1.0)
            ))

            # Partie orange superieure et pointe
            markers.markers.append(self.make_cone_surface(
                base_id + 3, x, y, 0.43, 0.125, 0.76, 0.008,
                (1.0, 0.30, 0.0)
            ))

        self.publisher.publish(markers)


def main():
    rclpy.init()
    node = DisplayCones()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

