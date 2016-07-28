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



#include "f1/f1plugin.hh"

GZ_REGISTER_MODEL_PLUGIN(f1::F1Plugin)

using namespace f1;
using namespace gazebo::physics;
using namespace gazebo::math;
using namespace gazebo::event;
using namespace gazebo::common;


F1Plugin::F1Plugin(){
    std::stringstream ss;
    ss << "["<<(void*)this<<"] ";
    ss >> _log_prefix;
    ONDEBUG_INFO(std::cout << _log_prefix << "F1Plugin::F1Plugin()" << std::endl;)
    sensors._log_prefix = _log_prefix;
    control._log_prefix = _log_prefix;
}

F1Plugin::~F1Plugin(){
    ONDEBUG_INFO(std::cout << _log_prefix << "F1Plugin::~F1Plugin()" << std::endl;)
    //icePlugin->stop();
}


void
F1Plugin::Load(ModelPtr _model, sdf::ElementPtr _sdf){
    ONDEBUG_INFO(std::cout << _log_prefix << "F1Plugin::Load()" << std::endl;)

    _log_prefix = "["+_model->GetName()+"] ";
    sensors._log_prefix = _log_prefix;
    control._log_prefix = _log_prefix;

    model = _model;
std::cout<< "A"<< std::endl;
    sensors.Load(model);
    std::cout<< "AI"<< std::endl;

    control.Load(model, _sdf);
    std::cout<< "B"<< std::endl;

    // Listen to the update event. This event is broadcast every
    // simulation iteration.
    updateConnection = Events::ConnectWorldUpdateBegin(
        boost::bind(&F1Plugin::OnUpdate, this, _1));

    sigintConnection = Events::ConnectSigInt(
        boost::bind(&F1Plugin::OnSigInt, this));

    this->InitializeIce(_sdf);
}


void
F1Plugin::Init(){
    ONDEBUG_INFO(std::cout << _log_prefix << "F1Plugin::Init()" << std::endl;)
    sensors.debugInfo();
    sensors.Init();

    sensors.cam[F1Sensors::CAM_LEFT]->SetActive(true);
    sensors.cam[F1Sensors::CAM_RIGHT]->SetActive(true);
    sensors.laser->SetActive(true);

    cameraproxy.registerCamera(sensors.cam[F1Sensors::CAM_LEFT]);
    cameraproxy.registerCamera(sensors.cam[F1Sensors::CAM_RIGHT]);
    cameraproxy.setActive(0);
    cameraproxy.setActive(1);

    control.Init(&sensors);

    icePlugin->start();
}


void
F1Plugin::OnUpdate(const UpdateInfo & ONDEBUG_VERBOSE(_info)){
    ONDEBUG_VERBOSE(std::cout << _log_prefix << "F1Plugin::OnUpdate()\n\t" << _info.simTime << std::endl;)
}

void
F1Plugin::OnSigInt(){
    ONDEBUG_INFO(std::cout << _log_prefix << "F1Plugin::OnSigInt()" << std::endl;)
    icePlugin->stop();
}


void
F1Plugin::Reset(){

}


void
F1Plugin::InitializeIce(sdf::ElementPtr _sdf){
    std::cout << _log_prefix << "F1Plugin::InitializeIce()" << std::endl;
    std::string iceConfigFile = "F1Plugin.cfg";
    if(_sdf->HasElement("iceConfigFile"))
        iceConfigFile =  _sdf->GetElement("iceConfigFile")->GetValue()->GetAsString();
    std::cout << _log_prefix << "\tconfig: "<< iceConfigFile << std::endl;
#if 0
    Ice::StringSeq args;
    args.push_back("--Ice.Config=" + iceConfigFile);
    Ice::CommunicatorPtr ic = Ice::initialize(args);
#else
    Ice::InitializationData id;
    id.properties = Ice::createProperties();
#if 0
    id.properties->load(iceConfigFile);
#else /// EasyIce
    easyiceconfig::loader::loadIceConfig(iceConfigFile, id.properties);
#endif
    Ice::CommunicatorPtr ic = Ice::initialize(id);
#endif
    std::cout<< "a"<< std::endl;

    std::string port;
    /// Get Adapter port from _sdf (static bad)
    if(_sdf->HasElement("iceAdapterPort"))
        port = _sdf->GetElement("iceAdapterPort")->Get<std::string>();
    std::cout<< "b"<< std::endl;

    /// Get port from model <name> (wolrd file, good enough)
    std::string name = model->GetName();
    boost::regex re("[0-9]+$");
    boost::sregex_iterator eof, m1(name.begin(), name.end(), re);
    if (m1!=eof){
        port = (*m1)[0];
    }
    if (!port.empty())
        id.properties->setProperty("F1.Adapter.Endpoints", "tcp -h localhost -p "+port); //ToDo: use regex replace instead hardcored text.
    std::cout<< "c"<< std::endl;

    std::cout << _log_prefix << "\tcreate Ice plugin..." << std::endl;
    icePlugin = F1IcePtr(new F1Ice(ic, &sensors, &control, &cameraproxy));
    icePlugin->_log_prefix = _log_prefix;
}
