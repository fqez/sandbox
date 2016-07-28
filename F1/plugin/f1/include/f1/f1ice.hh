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

#ifndef F1ICE_H
#define F1ICE_H


#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include <easyiceconfig/EasyIce.h>

#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/asio.hpp>

#include <f1/interfaces/motorsi.h>
#include <f1/interfaces/pose3di.h>
#include <f1/interfaces/pushcamerai.h>
#include <f1/interfaces/laseri.h>

#include <f1/f1sensors.hh>
#include <f1/f1control.hh>
#include <f1/cameraproxy.hh>

#include <f1/debugtools.h>

namespace f1{

class F1Ice
{
public:
    F1Ice(Ice::CommunicatorPtr ic, const F1Sensors *sensors, F1Control *control, CameraProxy *camproxy);
    virtual ~F1Ice();

    void run();
    void start();
    void stop();

    std::string _log_prefix;

protected:
    void bootstrap();

private:
    Ice::CommunicatorPtr ic;
    Ice::PropertiesPtr prop;
    Ice::ObjectAdapterPtr adapter;

private:
    const F1Sensors *sensor;
    F1Control *control;
    CameraProxy *camproxy;
    boost::mutex lock;

};

typedef boost::shared_ptr<F1Ice> F1IcePtr;

}//NS

#endif // QUADROTORICE_H
