#!/bin/bash

# Downloading web-gui:
wget -q https://git.io/voEUQ -O /tmp/raspap && bash /tmp/raspap

#    IP address: 10.3.141.1
#        Username: admin
#        Password: secret
#    DHCP range: 10.3.141.50 to 10.3.141.255
#    SSID: raspi-webgui
#    Password: ChangeMe

#write out current crontab
crontab -l > crontab_jderobotkids
#echo new cron into cron file
echo "* * * * * /usr/bin/python ~/local_Downloader/daemon_JdeRobot_executer.py" >> jderobotkids
#install new cron file
crontab crontab_jderobotkids
rm crontab_jderobotkids

#mkdir /home/pi/listener
#mkdir /home/pi/running

#sudo cp listener_daemon.sh /etc/init.d/
#sudo cp JdeRobot_kids_execute.py /usr/local/bin/

# Open this file when the deployenment is complete.
#printf sudo nano /usr/local/bin/JdeRobot_kids_execute.py
