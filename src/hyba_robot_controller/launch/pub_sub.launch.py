import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from visualization_msgs.msg import Marker


class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')

        self.publisher = self.create_publisher(
            String,
            'robot_command',
            10
        )

        self.marker_publisher = self.create_publisher(
            Marker,
            'visualization_marker',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_message
        )

        self.counter = 0

    def publish_message(self):

        msg = String()
        msg.data = f"Hello Robot {self.counter}"
        self.publisher.publish(msg)

        self.get_logger().info(
            f'Published: {msg.data}'
        )

        obstacles = [
            (2.5, 0.0),
            (3.5, 1.0),
            (4.5, -1.0),
            (5.5, 1.5),
            (6.5, -1.5),
            (7.5, 0.0),
        ]

        for i, (x, y) in enumerate(obstacles):

            marker = Marker()

            marker.header.frame_id = 'odom'
            marker.header.stamp = self.get_clock().now().to_msg()

            marker.ns = 'obstacles'
            marker.id = i

            marker.type = Marker.MESH_RESOURCE
            marker.mesh_resource = 'file:///home/hiba/navbot_ws/src/robot_description/model/meshes/traffic_cone.obj'
            marker.mesh_use_embedded_materials = True
            marker.action = Marker.ADD

            marker.pose.position.x = x
            marker.pose.position.y = y
            marker.pose.position.z = 0.4

            marker.pose.orientation.x = 0.0
            marker.pose.orientation.y = 0.0
            marker.pose.orientation.z = 0.0
            marker.pose.orientation.w = 1.0

            marker.scale.x = 0.5
            marker.scale.y = 0.5
            marker.scale.z = 0.8

            marker.color.r = 1.0
            marker.color.g = 0.5
            marker.color.b = 0.0
            marker.color.a = 1.0

            self.marker_publisher.publish(marker)

        self.counter += 1


def main(args=None):

    rclpy.init(args=args)

    node = PublisherNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
