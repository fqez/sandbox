# Pepper - primeros pasos

## Conexiones

* Conectarse a la red wifi que genera Pepper:
	* **IP:** 198.17.0.190
	* **credenciales para la red Wifi:** R0b0t1c4$
	* **credenciaes para el web GUI:** nao/nao

## PYTHONPATH
* Asegurarse de que el sdk naoqi de python esta en el pythonpath (descargar de la web de softbank):

   ``` export PYTHONPATH=${PYTHONPATH}:/home/jmplaza/Desktop/pepper/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages```

## Lanzar interfaces

* Lanzar interfaces del pepper

   ``` roslaunch pepper_bringup pepper_full.launch nao_ip:=198.17.0.190 roscore_ip:=127.0.0.1 network_interface:=wlo1```

    * Donde:
		* nao_ip es la ip del pepper
		* roscore_ip es la ip del roscore (localhost)
		* network_interface es la interfaz de red a la que esta conectado el pepper (ifconfig para saber el nombre)



### Topics:

Lista de topics de pepper y su correspondencia

    Cámara frontal superior RGB: /pepper_robot/naoqi_driver/camera/front/image_raw
    Cámara frontal inferior RGB: /pepper_robot/naoqi_driver/camera/bottom/image_raw
    Cámara RGBD: 
    Cámara IR:
    Base motores: /cmd_vel (hay que poner al robot en posicion incial con coreographe - de momento- )s

