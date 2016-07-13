#include "ros/ros.h"
#include "/home/shady/catkin_ws/devel/include/ros_compat/Num.h"
#include "/home/shady/catkin_ws/devel/include/ros_compat/Pose3d.h"
#include "/home/shady/catkin_ws/devel/include/ros_compat/Motors.h"
#include "opencv2/core/core.hpp"
#include "image_transport/image_transport.h"
#include "cv_bridge/cv_bridge.h"
#include "sensor_msgs/image_encodings.h"

class roscompat {
	
/* public member functions */
public:
	void translate_image_messages(const sensor_msgs::ImageConstPtr& msg, cv::Mat& image);
	void translate_laser_messages(const ros_compat::Num::ConstPtr& msg, std::vector<float>& laserdata);
	void translate_pose3d_messages(const ros_compat::Pose3d::ConstPtr& msg, std::vector<float>& pose);
	void translate_motor_messages(const ros_compat::Motors::ConstPtr& msg, std::vector<float>& motors);
};
