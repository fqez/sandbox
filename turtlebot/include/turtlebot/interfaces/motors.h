#include <boost/bind.hpp>
#include "gazebo.hh"
#include "physics/physics.hh"
#include "common/common.hh"
#include "transport/transport.hh"

#include "plugins/RayPlugin.hh"

// ICE utils includes
#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>

#include <easyiceconfig/EasyIce.h> 

// JDErobot general ice component includes
#include <jderobot/motors.h>


#ifndef MOTORS_H
#define	MOTORS_H

namespace gazebo {

    class Motors : public ModelPlugin {
    public:

        Motors();
        virtual void Load(physics::ModelPtr _model, sdf::ElementPtr _sdf);
        virtual void Init();

        std::string nameMotors;
        float vel, w;
        pthread_mutex_t mutex;
        pthread_mutex_t mutexMotor;

        struct motor_t {
            float v;
            float w;
            float l;
        };


        motor_t robotMotors;

    private:
        void OnUpdate();
        //void OnVelMsg(ConstPosePtr &_msg);
        transport::NodePtr node;
        transport::SubscriberPtr velSub;

        physics::ModelPtr model;
        physics::JointPtr leftJoint, rightJoint;
        event::ConnectionPtr updateConnection;
        double wheelSpeed[2];
        double torque;
        double wheelSeparation;
        double wheelRadius;
        common::Time prevUpdateTime;

        physics::LinkPtr link, leftWheelLink, rightWheelLink;
        double sum;

        int count;

        //event::ConnectionPtr updateConnection; Alex
        //physics::ModelPtr model; Alex
    };
}




#endif	/* POSE_H */

