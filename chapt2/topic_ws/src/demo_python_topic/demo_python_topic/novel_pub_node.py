import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue


class NovelPubNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name} has been started.")
        self.novels_queue_ = Queue()#创建队列
        self.novel_publisher = self.create_publisher(String, 'novel_topic', 10)
        self.create_timer(5, self.timer_callback)
        

    def timer_callback(self):
        if self.novels_queue_.qsize() > 0:
            line = self.novels_queue_.get()
            msg = String()
            msg.data = line
            self.novel_publisher.publish(msg)
            self.get_logger().info(f"Published: {line}")

    def download(self, url):
            response = requests.get(url)
            response.encoding = 'utf-8'
            text = response.text
            word_count = len(text.split())
            self.get_logger().info(f"URL: {url} -> Word Count: {word_count}")
            for line in text.splitlines():
                self.novels_queue_.put(line)  # 将每一行小说放入队列


def main():
    rclpy.init()
    node = NovelPubNode("novel_pub_node")
    node.download("https://www.baidu.com")
    rclpy.spin(node)
    rclpy.shutdown()
