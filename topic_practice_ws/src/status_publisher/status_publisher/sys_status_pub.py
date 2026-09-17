import rclpy
from rclpy.node import Node
from status_interfaces.msg import SystemStatus
import psutil
import platform 

class SysStatusPub(Node):
    def __init__(self, node_name="sys_status_pub"):
        super().__init__(node_name)
        self.status_publisher = self.create_publisher(SystemStatus, 'system_status', 10)
        self.timer = self.create_timer(1.0, self.timer_callback,)

    def timer_callback(self):
        """
        builtin_interfaces/Time stamp #时间记录戳
        string  host_name #主机名
        float32 cpu_percent #CPU 使用率
        float32 memory_percent #内存使用率
        float32 memory_total #内存总大小
        float32 memory_available #内存总大小
        float64 net_sent #网络发送数据总量 1MB= 8Mb
        float64 net_recv #网络数据接受总量 
        """
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        net_io_counters = psutil.net_io_counters()

        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.host_name = platform.node()
        msg.cpu_percent = cpu_percent
        msg.memory_percent = memory_info.percent
        msg.memory_total = memory_info.total / (1024 * 1024)  # Convert to MB
        msg.memory_available = memory_info.available / (1024 * 1024)  # Convert to MB
        msg.net_sent = net_io_counters.bytes_sent / (1024 * 1024)  # Convert to MB
        msg.net_recv = net_io_counters.bytes_recv / (1024 * 1024)  # Convert to MB

        self.get_logger().info(f'Publishing system status: {msg}')
        self.status_publisher.publish(msg)

def main():
    rclpy.init()
    node = SysStatusPub("sys_status_pub")
    rclpy.spin(node)
    rclpy.shutdown()
