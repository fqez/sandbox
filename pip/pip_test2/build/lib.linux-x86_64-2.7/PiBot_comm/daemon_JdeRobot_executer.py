#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------
# This program is executed by 'cron' every minute to check if
# JdeRobot_listener.py is running
# ----------------------------- Ignacio Arranz Águeda - 2018 ---

import logging
import time
import sys, os
import commands



def run():
   output = commands.getoutput('ps aux | grep "JdeRobotKids_listener.py" | grep -v grep | awk "{print $12}"')
   if output != "" and output.split()[-1] == "JdeRobotKids_listener.py":
      print output.split()[-1]
      print "The process is already running"
   else:
      print "The process does not exist. Initializing."
      os.system("/usr/bin/python ~/local_Downloader/JdeRobotKids_listener.py")
      print "Next check in a minute."


if __name__ == '__main__':
   run()
