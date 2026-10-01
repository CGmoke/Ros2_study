import rclpy
from rclpy.node import Node
from rclpy.time import Time #时间戳
from rclpy.duration import Duration #超时时间
from tf2_ros import Buffer, TransformListener #坐标缓存与坐标监听器
from tf_transformations import euler_from_quaternion #四元数转欧拉角函数

class TFListener(Node):

    def __init__(self):
        super().__init__('tf_listener')
        self.buffer_ = Buffer()
        self.listener_ = TransformListener(self.buffer_, self)
        self.timer_ = self.create_timer(1.0,self.get_transform)

    def get_transform(self):
        """
        查询 base_link 到 bottle_link 之间的坐标关系
        """
        try:
            result = self.buffer_.lookup_transform(
                'base_link','bottle_link',
                Time(),Duration(seconds=1.0)
            )
        except Exception as e:
            self.get_logger().warn(f'查询坐标变换失败：{e}')
            return

        transform = result.transform
        self.get_logger().info(f'平移：{transform.translation}')
        self.get_logger().info(f'旋转（四元数）：{transform.rotation}')

        rotation_euler = euler_from_quaternion([
            transform.rotation.x,
            transform.rotation.y,
            transform.rotation.z,
            transform.rotation.w,
        ])
        self.get_logger().info(f'旋转（RPY）：{rotation_euler}')

def main():
    rclpy.init()
    node = TFListener()
    rclpy.spin(node)
    rclpy.shutdown()
