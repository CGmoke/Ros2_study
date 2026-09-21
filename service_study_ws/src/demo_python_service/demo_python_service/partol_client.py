import random

import rclpy
from rclpy.node import Node
from service_interfaces.srv import Partrol


class PartolClientNode(Node):
    def __init__(self, node_name='partol_client'):
        super().__init__(node_name)
        self.client_ = self.create_client(Partrol, 'partol')
        self.get_logger().info('小乌龟巡逻客户端已启动！')

    def send_request(self, target_x, target_y):
        # 等待服务端上线
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('巡逻服务端未启动，等待中...')
        request = Partrol.Request()
        request.target_x = target_x
        request.target_y = target_y
        future = self.client_.call_async(request)
        rclpy.spin_until_future_complete(self, future)  # 等待服务端处理完成
        response = future.result()
        if response.result == Partrol.Response.SUCESS:
            self.get_logger().info(
                f'已到达目标位置: ({target_x:.2f}, {target_y:.2f})')
        else:
            self.get_logger().warn(
                f'巡逻失败: ({target_x:.2f}, {target_y:.2f})')

    def start_partol(self):
        """循环随机生成目标点，让小乌龟不停巡逻"""
        while rclpy.ok():
            target_x = random.uniform(1.0, 10.0)
            target_y = random.uniform(1.0, 10.0)
            self.get_logger().info(
                f'发送巡逻目标: x={target_x:.2f}, y={target_y:.2f}')
            self.send_request(target_x, target_y)


def main():
    rclpy.init()
    node = PartolClientNode()
    node.start_partol()
    rclpy.shutdown()