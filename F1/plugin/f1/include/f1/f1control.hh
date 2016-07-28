/*
 *  Copyright (C) 1997-2015 JDE Developers Team
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
 *  Authors :
 *       Victor Arribas Raigadas <v.arribas.urjc@gmai.com>
 */

#ifndef F1CONTROL_H
#define F1CONTROL_H


#include <gazebo/common/common.hh>
#include <gazebo/physics/physics.hh>

#include "transport/transport.hh"

#include <f1/f1sensors.hh>

namespace f1{

class F1Control {
public:
    F1Control();
    virtual ~F1Control();
    void setSensors(F1Sensors *sensors);

/// Control commands
public:

    pthread_mutex_t mutex;
    pthread_mutex_t mutexMotor;

    struct motor_t {
        float v;
        float w;
        float l;
        double wheelMax;
        double wheelMin;
        double targetRightSteerPos,targetLeftSteerPos;
    };
    motor_t robotMotors;

    std::string _log_prefix;

/// Control
protected:
   F1Sensors *sensors;

/// Gazebo
public:
    void Load(gazebo::physics::ModelPtr model, sdf::ElementPtr _sdf);
    void Init(F1Sensors* sensors);
    void OnUpdate(const gazebo::common::UpdateInfo & _info);
    void teleport(gazebo::math::Pose pose);

private:
    gazebo::event::ConnectionPtr updateConnection;
    gazebo::physics::ModelPtr model;
    gazebo::physics::InertialPtr inertial;
    gazebo::physics::JointPtr driveLeftJoint, driveRightJoint, steeringLeftJoint, steeringRightJoint;

    gazebo::transport::NodePtr node;
    gazebo::transport::SubscriberPtr velSub;
    gazebo::common::Time prevUpdateTime;

    double wheelSeparation;
    double wheelRadius;
    double motorspeed;

};


typedef boost::shared_ptr<F1Control> F1ControlPtr;

}//NS

#endif // QUADROTORPLUGIN_H
