import rclpy
from rclpy.node import Node

class PersonNode(Node):
    def __init__(self, name: str, age: int):
        super().__init__('person_node')
        print("PersonNode __init__方法被调用")
        self.name = name
        self.age = age

    def introduce(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."


def main():
    rclpy.init()
    node = PersonNode("Alice", 30)
    node2 = PersonNode("光头强", 25)   
    introduction = node.introduce()
    introduction2 = node2.introduce()
    rclpy.spin(node)
    rclpy.shutdown()
    print(introduction)
    print(introduction2)
    

if __name__ == '__main__':
    main()