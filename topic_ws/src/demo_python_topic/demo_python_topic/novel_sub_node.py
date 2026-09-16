import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class NovelSubNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name} has been started.")
        self.novels_queue_ = Queue()#创建队列
        self.novel_subscriber = self.create_subscription(String, 'novel_topic', self.subscription_callback, 10)
        self.speech_thread = threading.Thread(target=self.speak_novel)
        self.speech_thread.start()


    def subscription_callback(self, msg):
        self.novels_queue_.put(msg.data)

    def speak_novel(self):
        speaker = espeakng.Speaker()
        speaker.voice = 'zh'  # Set the voice to Chinese
        while rclpy.ok():
            if self.novels_queue_.qsize() > 0:
                text = self.novels_queue_.get()
                self.get_logger().info(f"朗读: {text}")
                # Use espeakng to speak the line
                speaker.say(text)
                speaker.wait()  # Wait for the speech to finish before continuing
            else:
                time.sleep(1)  # Sleep for a while if the queue is empty to avoid busy waiting


def main():
    rclpy.init()
    node = NovelSubNode("novel_sub_node")
    rclpy.spin(node)
    rclpy.shutdown()
