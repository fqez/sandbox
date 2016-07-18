/*
 *
 *  Copyright (C) 1997-2015 JdeRobot Developers Team
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see http://www.gnu.org/licenses/. 
 *
 *  Authors : 	Roberto Calvo <rocapal [at] gsyc [dot] es>
 *  			David Lobato Bravo <dav.lobato [dat] gmail [dot] com>
 *
 */

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "roscompat/Num.h"
#include "roscompat/roscompat.h"

#include "image_transport/image_transport.h"
#include "cv_bridge/cv_bridge.h"
#include "sensor_msgs/image_encodings.h"

#include "opencv2/opencv.hpp"

#include <iostream>
#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include <jderobot/camera.h>
#include <visionlib/colorspaces/colorspacesmm.h>
#include "viewer.h"
#include "parallelIce/cameraClient.h"
#include "easyiceconfig/EasyIce.h" 

//Global variables for ROS translation.
roscomp* rc;
cv::Mat cam_frame;
cameraview::Viewer viewer;

void chatterCallback(const roscompat::Num::ConstPtr& msg)
{
  	viewer.displayFrameRate(msg->num);
}

void cameracallback(const sensor_msgs::ImageConstPtr& image_msg) {
	rc->translate_image_messages(image_msg, cam_frame);

	viewer.display(cam_frame);

	
}

int main(int argc, char** argv){

	int status;	
	jderobot::cameraClient* camRGB;

	Ice::CommunicatorPtr ic = EasyIce::initialize(argc,argv);;
	Ice::PropertiesPtr prop = ic->getProperties();
	
	//0: Ice    other:ROS
	int driver = prop->getPropertyAsIntWithDefault("Ice.Driver", 0);

	if (driver == 0) {   //Try to connect with ICE

		std::cout << "Receiving data from ICE interfaces" << std::endl;
		try{
		
			Ice::ObjectPrx base = ic->propertyToProxy("Cameraview.Camera.Proxy");


			if (0==base)
				throw "Could not create proxy";


			camRGB = new jderobot::cameraClient(ic,"Cameraview.Camera.");

			if (camRGB == NULL){
				throw "Invalid proxy";
			}
			camRGB->start();

			while(viewer.isVisible()){
				//jderobot::ImageDataPtr data = camRGB->getImageData(format);

				camRGB->getImage(cam_frame);
				viewer.display(cam_frame);
				viewer.displayFrameRate(camRGB->getRefreshRate());
			}
	
			camRGB->stop_thread();
			delete(camRGB);

		}catch (const Ice::Exception& ex) {
			std::cerr << ex << std::endl;
			status = 1;
		} catch (const char* msg) {
			std::cerr << msg << std::endl;
			status = 1;
		}
	}else{     //Try to connect ROS

		std::cout << "Receiving data from ROS messages" << std::endl;

		/*ros::init(argc, argv, "listener");

	  	ros::NodeHandle n,nh;
	  	image_transport::ImageTransport it(nh);
	  	image_transport::Subscriber camera_sub = it.subscribe("cameratopic", 1000, cameracallback);

	  	ros::Subscriber sub = n.subscribe("chatter", 1001, chatterCallback);

	  	ros::spin();*/
	}

	if (ic)
		ic->destroy();

	return status;
}
