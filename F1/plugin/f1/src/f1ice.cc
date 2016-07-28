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
 *       Francisco Perez Salgado <f.perez475@gmai.com>
 */


#include <f1/f1ice.hh>

using namespace f1;
using namespace f1::interfaces;
using namespace Ice;

F1Ice::F1Ice(CommunicatorPtr ic, const F1Sensors *sensors, F1Control *control, CameraProxy *camproxy):
    ic(ic),
    sensor(sensors),
    control(control),
    camproxy(camproxy)
{
    assert(ic != 0);
}

F1Ice::~F1Ice(){
    stop();
}

void
F1Ice::stop(){
    ONDEBUG_INFO(std::cout<<_log_prefix << "F1Ice::stop()" << std::endl;)
    lock.lock();
    if (ic && !ic->isShutdown()){
        std::cout<<_log_prefix << "Shuting down Ice..." << std::endl;
        adapter->deactivate();
        ic->shutdown();
    }
    lock.unlock();
}

void
F1Ice::start(){
    /// boost::thread "thread" lifetime survives "object" lifetime if
    /// thread was running when object is deleted
    /// Is same effect that detach()
    /// Therefore, there is no needed to manage object lifetime neither
    /// delete it.
   boost::thread(boost::bind(&F1Ice::run, this));
}

void
F1Ice::run(){
#if 0
    // Register to handle the signals that indicate when the server should exit.
    // It is safe to register for the same signal multiple times in a program,
    // provided all registration for the specified signal is made through Asio.
    // API changed from 1.47 to 1.59 (now requires io_service)
    boost::asio::io_service _io_service;
    boost::asio::signal_set _signals(_io_service);
    _signals.add(SIGINT);
    _signals.add(SIGTERM);
    _signals.async_wait(boost::bind(&F1Ice::stop, this));
#endif

    bootstrap();

    ic->waitForShutdown();

    std::cout<<_log_prefix << "Ice is down now" << std::endl;
}

void F1Ice::bootstrap(){
    lock.lock();
    if (ic->isShutdown()) return;

    prop = ic->getProperties();
    std::cout<< "aa"<< std::endl;

    adapter = ic->createObjectAdapter("Formula1.Adapter");
    std::cout<<_log_prefix << "Ice adapter listening at " << std::endl;
    std::cout<<_log_prefix << "\t" << adapter->getEndpoints()[0]->toString() << std::endl;

    std::string name;

    name = prop->getProperty("F1.Motors.Name");
    ObjectPtr motorsi = new MotorsI(control);
    adapter->add(motorsi, ic->stringToIdentity(name));

    name = prop->getProperty("F1.Pose3D.Name");
    ObjectPtr posei = new Pose3DI(sensor, control);
    adapter->add(posei, ic->stringToIdentity(name));

    ObjectPtr laseri = new LaserI(sensor);
    name = prop->getProperty("F1.Laser.Name");
    adapter->add(laseri, ic->stringToIdentity(name));

    //ObjectPtr camerai = new CameraI(sensor);
    ObjectPtr cameraiL;
    {
        PushCameraI *_cameraiL = new PushCameraI();
        camproxy->registerConsumer(ICameraConsumerPtr(_cameraiL));
        cameraiL = ObjectPtr(_cameraiL);
    }
    name = prop->getProperty("F1.CameraL.Name");
    adapter->add(cameraiL, ic->stringToIdentity(name));

    ObjectPtr cameraiR;
    {
        PushCameraI *_cameraiR = new PushCameraI();
        camproxy->registerConsumer(ICameraConsumerPtr(_cameraiR));
        cameraiR = ObjectPtr(_cameraiR);
    }
    name = prop->getProperty("F1.CameraR.Name");
    adapter->add(cameraiR, ic->stringToIdentity(name));

    adapter->activate();

    std::cout<<_log_prefix<< "Ice booststrap done." << std::endl;
    lock.unlock();
}
