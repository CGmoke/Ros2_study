import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node = Node('my_python_node')
    node.get_logger().info('Hello from my Python node!')
    node.get_logger().warn('This is a warning message.')
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()