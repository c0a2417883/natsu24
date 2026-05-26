#include <functional>
#include <memory>
#include <string>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

#include "Serial.h"
#include "natsu24/main.h"
#include "nav_msgs/msg/odometry.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include "std_msgs/msg/int32_multi_array.hpp"

using std::placeholders::_1;
using namespace std::chrono_literals;

class Natsu24 : public rclcpp::Node {
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr cmd_pub_;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
    rclcpp::Subscription<std_msgs::msg::Int32MultiArray>::SharedPtr sw_sub_;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr l1_sub_, l2_sub_, l3_sub_, l4_sub_;
    rclcpp::TimerBase::SharedPtr timer_;

    float robot_pos_[3] = {0};
    double robot_odometer_[2] = {0};
    bool switch_flag_[SWITCH_SIZE] = {false};
    float tof_distance_[4] = {0};

   public:
    Natsu24() : Node("natsu24") {
        cmd_pub_ = this->create_publisher<std_msgs::msg::Float64MultiArray>("/wheel_controller/commands", 10);
        odom_sub_ = this->create_subscription<nav_msgs::msg::Odometry>(
            "/odom", 10, std::bind(&Natsu24 ::odom_cb, this, _1));
        sw_sub_ = this->create_subscription<std_msgs::msg::Int32MultiArray>(
            "/sw", 10, std::bind(&Natsu24 ::sw_cb, this, _1));
        l1_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/laser1", 10, std::bind(&Natsu24 ::l1_cb, this, _1));
        l2_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/laser2", 10, std::bind(&Natsu24 ::l2_cb, this, _1));
        l3_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/laser3", 10, std::bind(&Natsu24 ::l3_cb, this, _1));
        l4_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/laser4", 10, std::bind(&Natsu24 ::l4_cb, this, _1));

        setup();
    }

   private:
    void odom_cb(const nav_msgs::msg::Odometry::SharedPtr msg) {
        static double prev_pos_x = msg->pose.pose.position.x;
        static double prev_pos_y = msg->pose.pose.position.y;
        robot_pos_[0] = msg->pose.pose.position.x;
        robot_pos_[1] = msg->pose.pose.position.y;
        double roll, pitch, yaw;
        geometry_quat_to_rpy(roll, pitch, yaw, msg->pose.pose.orientation);
        robot_pos_[2] = yaw;
        double diff_x = (robot_pos_[0] - prev_pos_x);
        double diff_y = (robot_pos_[1] - prev_pos_y);
        prev_pos_x = robot_pos_[0];
        prev_pos_y = robot_pos_[1];
        yaw = -yaw;
        robot_odometer_[0] += diff_x * cos(yaw) - diff_y * sin(yaw);
        robot_odometer_[1] += diff_x * sin(yaw) + diff_y * cos(yaw);

        im.yaw = robot_pos_[2];
        encoder.cnt[0] = -robot_odometer_[0] / 0.024 / (2 * M_PI) * (2048 * 4);
        encoder.cnt[1] = -robot_odometer_[1] / 0.024 / (2 * M_PI) * (2048 * 4);
        for (int i = 0; i < SWITCH_SIZE; ++i) switch_[i] = switch_flag_[i];
        for (int i = 0; i < 4; ++i) tof.distance[i] = tof_distance_[i];

        loop();
        // シリアル通信
        if (Serial.n > 0) {
            RCLCPP_INFO(this->get_logger(), Serial.buf, Serial.n);
            Serial.n = 0;
        }

        for (int i = 0; i < SWITCH_SIZE; ++i) switch_flag_[i] = false;
        // モーター
        publishCmd(motor_vel);
    }
    void sw_cb(const std_msgs::msg::Int32MultiArray::SharedPtr msg) {
        int i = 0;
        for (auto &a : msg->data) {
            switch_flag_[i] = a;
            if (++i == SWITCH_SIZE)
                return;
        }
    }
    void l1_cb(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
        tof_distance_[0] = msg->ranges[0];
    }
    void l2_cb(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
        tof_distance_[1] = msg->ranges[0];
    }
    void l3_cb(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
        tof_distance_[2] = msg->ranges[0];
    }
    void l4_cb(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
        tof_distance_[3] = msg->ranges[0];
    }
    void geometry_quat_to_rpy(double &roll, double &pitch, double &yaw, geometry_msgs::msg::Quaternion &geometry_quat) {
        tf2::Quaternion q(geometry_quat.x, geometry_quat.y, geometry_quat.z, geometry_quat.w);
        tf2::Matrix3x3 m(q);
        m.getRPY(roll, pitch, yaw);
    }
    void publishCmd(float *motor_vel) {
        auto cmd = std_msgs::msg::Float64MultiArray();
        cmd.data.resize(4);
        cmd.data[0] = motor_vel[0];
        cmd.data[1] = motor_vel[1];
        cmd.data[2] = motor_vel[2];
        cmd.data[3] = motor_vel[3];
        cmd_pub_->publish(cmd);
    }
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Natsu24>());
    rclcpp::shutdown();
    return 0;
}