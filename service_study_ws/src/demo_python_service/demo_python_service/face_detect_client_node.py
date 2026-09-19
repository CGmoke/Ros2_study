import rclpy
from rclpy.node import Node
from service_interfaces.srv import FaceDetector
import cv2
import os
from ament_index_python.packages import get_package_share_directory
from cv_bridge import CvBridge
import time

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node') 
        self.bridge = CvBridge()
        self.default_image_path = os.path.join(
            get_package_share_directory('demo_python_service'), 'resource', 'imagecopy.png')
        self.get_logger().info('人脸检测客户端已启动！')
        self.get_logger().info(f'默认图像路径：{self.default_image_path}')
        self.client = self.create_client(FaceDetector, 'face_detect')
        self.image = cv2.imread(self.default_image_path)
        self.get_logger().info('人脸检测服务已创建！')

    def send_request(self):
        #判断服务端是否在线
        while self.client.wait_for_service(timeout_sec=1.0) == False:
            self.get_logger().info('检测服务端未启动，等待中...')
            time.sleep(1.0)
        self.get_logger().info('检测服务端已启动！')
        
        request = FaceDetector.Request()
        request.image = self.bridge.cv2_to_imgmsg(self.image, encoding='bgr8')
        #发送请求,等待处理
        future = self.client.call_async(request)
        self.get_logger().info('检测服务端已响应！')
        # while not future.done():
        #     time.sleep(1.0)
        rclpy.spin_until_future_complete(self, future)#等待服务端处理完成
        response = future.result()
        self.get_logger().info(f'检测到{response.number}个人脸！')
        self.show_response(response)



    
    def show_response(self,response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]
            self.get_logger().info(f'人脸{i}的位置为：top={top}, right={right}, bottom={bottom}, left={left}')
            cv2.rectangle(self.image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow('face_detect', self.image)
        cv2.waitKey(0)
    
def main():
    rclpy.init()
    node = FaceDetectClientNode()
    node.send_request()
    node.destroy_node()
    rclpy.shutdown()