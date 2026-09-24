import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from visualization_msgs.msg import Marker


class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')

        # =========================
        # Publisher robot_command
        # =========================

        self.publisher = self.create_publisher(
            String,
            'robot_command',
            10
        )

        # =========================
        # Publisher pour RViz2
        # =========================

        self.marker_publisher = self.create_publisher(
            Marker,
            'visualization_marker',
            10
        )

        # Timer
        self.timer = self.create_timer(
            1.0,
            self.publish_message
        )

        self.counter = 0

    def publish_message(self):

        # =========================
        # Message String
        # =========================

        msg = String()

        msg.data = f"Hello Robot {self.counter}"

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Published: {msg.data}'
        )

        # =========================
        # Marker pour RViz2
        # =========================

        marker = Marker()

        marker.header.frame_id = 'base_link'
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = 'robot'
        marker.id = 0

        marker.type = Marker.SPHERE
        marker.action = Marker.ADD

        # Position du marker
        marker.pose.position.x = 0.5
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.5

        marker.pose.orientation.w = 1.0

        # Taille
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2

        # Transparence
        marker.color.a = 1.0

        # Couleur
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0

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