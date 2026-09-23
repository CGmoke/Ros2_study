#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp" //提供消息接口
#include "tf2/LinearMath/Quaternion.h"//提供tf2：：Quaternion类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp" //消息类型转换函数
#include "tf2_ros/transform_listener.hpp"
#include "tf2_ros/buffer.h"
#include <chrono>
using namespace std::chrono_literals;

class TFListener:public rclcpp::Node
{
    private:
        std::shared_ptr<tf2_ros::TransformListener> listener_;
        rclcpp::TimerBase::SharedPtr timer_;
        std::shared_ptr<tf2_ros::Buffer> buffer_;

       public:
        TFListener():Node("tf_listener")  
        {   
            this->buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
            this->listener_ = std::make_shared<tf2_ros::TransformListener>(*this->buffer_, this);
            this->timer_ = this->create_wall_timer(
                std::chrono::milliseconds(100),
                std::bind(&TFListener::getTransform,this));   
            
        }
    void getTransform() 
    {
        try
        {
            auto transform = this->buffer_->lookupTransform("base_link","target_point",this->get_clock()->now(),rclcpp::Duration::from_seconds(1.0));
            auto translation = transform.transform.translation;
            auto rotation = transform.transform.rotation;
            double roll,pitch,yaw;
            tf2::Quaternion q;
            tf2::fromMsg(rotation, q);
            tf2::Matrix3x3(q).getRPY(roll, pitch, yaw);
            RCLCPP_INFO(this->get_logger(), "translation: %f, %f, %f, roll: %f, pitch: %f, yaw: %f", translation.x, translation.y, translation.z, roll, pitch, yaw);
        }
        catch(const std::exception& e)
        {
            RCLCPP_ERROR(this->get_logger(), "%s", e.what());
        }   
        
    }
    // geometry_msgs::msg::TransformStamped transform;
    //     transform.header.stamp = this->get_clock()->now();
    //     transform.header.frame_id = "map";
    //     transform.child_frame_id = "base_link";
    //     transform.transform.translation.x = 5.0;
    //     transform.transform.translation.y = 3.0;
    //     transform.transform.translation.z = 0.0;
    //     tf2::Quaternion q;
    //     q.setRPY(0.0,0.0,60*M_PI/180.0);
    //     transform.transform.rotation = tf2::toMsg(q); 
    //     this->listener_->sendTransform(transform);
};

int main(int argc,char* argv[])
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<TFListener>();
    node->getTransform();
    rclcpp::spin(node);
    return 0;
}