#include "ros_compat.h"

void roscompat::translate_image_messages(const sensor_msgs::ImageConstPtr& msg, cv::Mat& image) {
	cv_bridge::CvImagePtr cv_ptr;
	try {
		cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
	} catch (cv_bridge::Exception& e) {
		ROS_ERROR("cv_bridge exception: %s", e.what());
		return;
	}
	image = cv_ptr->image;
}

void roscompat::translate_laser_messages(const ros_compat::Num::ConstPtr& msg, std::vector<float>& laserdata) {
	laserdata = std::vector<float>(msg->numArr.begin(), msg->numArr.end());
}
	
void roscompat::translate_pose3d_messages(const ros_compat::Pose3d::ConstPtr& msg, std::vector<float>& pose) {
	pose.push_back(msg->x);
	pose.push_back(msg->y);
	pose.push_back(msg->z);
	pose.push_back(msg->h);
	pose.push_back(msg->q0);
	pose.push_back(msg->q1);
	pose.push_back(msg->q2);
	pose.push_back(msg->q3);
}
	
void roscompat::translate_motor_messages(const ros_compat::Motors::ConstPtr& msg, std::vector<float>& motors) {
	motors.push_back(msg->w);
	motors.push_back(msg->v);
	motors.push_back(msg->l);
}
