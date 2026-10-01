import math
import time

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from service_interfaces.srv import Partrol


class TurtleControlNode(Node):
    def __init__(self, node_name='turtle_control'):
        super().__init__(node_name)
        self.cb_group_ = ReentrantCallbackGroup()  # 服务回调会阻塞，订阅需并行执行
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.subscription_ = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.pose_callback,
            10,
            callback_group=self.cb_group_
        )
        self.service_ = self.create_service(
            Partrol,
            'partol',
            self.partol_callback,
            callback_group=self.cb_group_
        )
        self.k_ = 1.0  # 比例增益
        self.max_linear_speed_ = 1.0  # 最大线速度
        self.max_angular_speed_ = 1.0  # 最大角速度
        self.target_x_ = None
        self.target_y_ = None
        self.reach_flag_ = False
        self.get_logger().info('小乌龟巡逻服务端已启动，等待服务请求...')

    def pose_callback(self, pose):
        if self.target_x_ is None or self.reach_flag_:
            return
        # 1.计算与目标位置的距离和角度差
        distance = math.sqrt(
            math.pow(self.target_x_ - pose.x, 2) + math.pow(self.target_y_ - pose.y, 2))
        angle = math.atan2(self.target_y_ - pose.y, self.target_x_ - pose.x) - pose.theta
        angle = math.atan2(math.sin(angle), math.cos(angle))  # 规范化到[-pi, pi]

        # 2.控制策略
        msg = Twist()
        if distance > 0.1:
            if abs(angle) > 0.2:
                # 角度误差大时先转向目标方向
                msg.angular.z = angle
            else:
                # 角度对准后边转边前进
                msg.angular.z = self.k_ * angle
                msg.linear.x = self.k_ * distance
        else:
            self.reach_flag_ = True
            self.get_logger().info(
                f'已到达目标位置: ({self.target_x_:.2f}, {self.target_y_:.2f})')

        # 3.限幅
        msg.linear.x = max(-self.max_linear_speed_, min(self.max_linear_speed_, msg.linear.x))
        msg.angular.z = max(-self.max_angular_speed_, min(self.max_angular_speed_, msg.angular.z))
        # 4.发布控制指令
        self.publisher_.publish(msg)

    def partol_callback(self, request, response):
        self.get_logger().info(
            f'收到巡逻目标: x={request.target_x:.2f}, y={request.target_y:.2f}')
        self.target_x_ = request.target_x
        self.target_y_ = request.target_y
        self.reach_flag_ = False
        # 等待 pose_callback 中判定到达目标
        while rclpy.ok() and not self.reach_flag_:
            time.sleep(0.05)
        response.result = Partrol.Response.SUCESS if self.reach_flag_ else Partrol.Response.FAIL
        self.target_x_ = None
        self.get_logger().info('本次巡逻任务结束')
        return response


def main():
    rclpy.init()
    node = TurtleControlNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()