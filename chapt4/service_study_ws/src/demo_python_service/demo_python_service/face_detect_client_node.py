import rclpy
from rclpy.node import Node
from service_interfaces.srv import FaceDetector
import cv2
import os
from ament_index_python.packages import get_package_share_directory
from cv_bridge import CvBridge
import time
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType

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


    def call_set_parameters(self,parameters):
        """
        调用设置参数服务
        :param parameters: 参数列表
        """
        #1.创建一个客户端，等待服务上线
        update_param = self.create_client(SetParameters, 'face_detect_node/set_parameters')
        while update_param.wait_for_service(timeout_sec = 1.0) == False:
            self.get_logger().info('设置参数服务未启动，等待中...')
            time.sleep(1.0)
        self.get_logger().info('设置参数服务已启动！')
        
        #2.创建一个请求
        request = SetParameters.Request()
        request.parameters = parameters
        #3.发送请求
        future = update_param.call_async(request)
        self.get_logger().info('设置参数服务已响应！')
        #4.等待服务端处理完成
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        self.get_logger().info(f'设置参数服务返回结果：{response}')
        return response
    
    def update_detect_model(self,model='hog'):
        """根据传入的model，构造parameters,然后调用call_set_parameters方法更新服务参数"""
        param = Parameter(name='model')    
        param.name = 'model'
        param_value = ParameterValue(string_value=model)
        param_value.string_value = model
        param_value .type = ParameterType.PARAMETER_STRING
        param.value = param_value
        response = self.call_set_parameters([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f'设置参数成功！')
            else:
                self.get_logger().info(f'设置参数失败！原因：{result.reason}')




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
        # self.show_response(response)



    
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
    node.update_detect_model('hog')
    node.get_logger().info('模型更新完成！')
    node.send_request()
    node.destroy_node()
    rclpy.shutdown()