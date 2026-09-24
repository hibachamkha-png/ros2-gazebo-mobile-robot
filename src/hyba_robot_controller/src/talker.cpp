#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class Talker : public rclcpp::Node
{
public:
    Talker() : Node("talker"), count_(0)
    {
        publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);

        timer_ = this->create_wall_timer(
            1s,
            std::bind(&Talker::publish_message, this)
        );
    }

private:
    void publish_message()
    {
        auto message = std_msgs::msg::String();

        message.data = "Hello World: " + std::to_string(count_++);

        publisher_->publish(message);

        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;

    int count_;
};


int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<Talker>();

    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}
