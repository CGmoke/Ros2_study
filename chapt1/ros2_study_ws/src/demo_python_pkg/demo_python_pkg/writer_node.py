import rclpy
from demo_python_pkg.person_node import PersonNode

class WriterNode(PersonNode):
    def __init__(self, name: str, age: int, book: str) -> None:
        print("WriterNode __init__方法被调用")
        super().__init__(name, age)
        self.book = book

def main():
    rclpy.init()
    node = WriterNode("张三", 40, "Python编程")
    print(node.introduce())
    print(f"擅长写:{node.book}")
    rclpy.shutdown()