#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <chrono>
#include "turtlesim/msg/pose.hpp"

using namespace std::chrono_literals;

class TurtleControlNode : public rclcpp::Node
{
private:
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;//发布者的智能指针
  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscription_;//订阅者的智能指针
  double target_x_ = {5.0}; // 目标位置的x坐标
  double target_y_ = {5.0}; // 目标位置的y坐标
  double k_ = {1.0}; // 比例增益
  double max_line_speed_ = {1.0}; // 最大线速度
  double max_angular_speed_ = {1.0}; // 最大角速度



public:
  explicit TurtleControlNode(const std::string & node_name) : Node(node_name)
    {
    
      publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel", 10);
      subscription_ = this->create_subscription<turtlesim::msg::Pose>(
        "turtle1/pose",
        10,
        std::bind(&TurtleControlNode::on_pose_received, this, std::placeholders::_1)
      );
      
    }
    void on_pose_received(const turtlesim::msg::Pose::SharedPtr pose)
    { 
        //1.获取当前位置
        auto current_x = pose->x;
        auto current_y = pose->y;
        RCLCPP_INFO(this->get_logger(), "当前位置: (%.2f, %.2f)", current_x, current_y);
        //2.计算当前小海龟与目标位置差和角度差
        auto distance = std::sqrt(std::pow(target_x_ - current_x, 2) + std::pow(target_y_ - current_y, 2));
        RCLCPP_INFO(this->get_logger(), "当前位置与目标位置之间的误差: %.2f", distance);
        auto angle = std::atan2(target_y_ - current_y, target_x_ - current_x) - pose->theta;
        RCLCPP_INFO(this->get_logger(), "当前位置与目标位置之间的角度误差: %.2f", angle);
        //3.控制策略
        auto msg = geometry_msgs::msg::Twist();
        if (distance > 0.1)
        {
            if (fabs(angle) > 0.2)
            {
                msg.angular.z = fabs(angle);
            }else
            {
                msg.angular.z = k_*distance;
            }
        }
        //4.限制线速度和角速度
        if (msg.linear.x > max_line_speed_)
        {
            msg.linear.x = max_line_speed_;
        }
        if (msg.angular.z > max_angular_speed_)
        {
            msg.angular.z = max_angular_speed_;
        }
        //5.发布控制指令
        publisher_->publish(msg);
    }
};


int main(int argc, char* argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<TurtleControlNode>("turtle_control_node");
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}