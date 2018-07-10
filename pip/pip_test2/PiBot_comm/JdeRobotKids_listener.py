#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------
# This program check and move files from "listener" folder to
# "running" folder and then, execute the code.
# ----------------------------- Ignacio Arranz Águeda - 2018 ---

import logging
import time
import sys, os
import commands



def run():

    while True:
        content = commands.getoutput('ls ~/local_Downloader/listener/')
	try:
            content = content.split(".")
  	except:
	    content = content.split()
   	print "\n\n"
        print content
        if content != "":
            # If the files are compressed
            if content[-1] == "zip":
                print "Decompress zip:\n"
                os.system("unzip -o ~/local_Downloader/listener/exercise.zip -d listener/")
                os.system("rm listener/exercise.zip")
        
                print "Moving files"
                os.system("mv listener/*.py running/")
                os.system("mv listener/*.cfg running/")


                # CODE TO RUN THE ROBOT PROGRAM - HERE


            elif content[-1] == "tar":
                print "Decompressing tar:\n"
                os.system("tar -zxvf ~/local_Downloader/listener/exercise.tar -C listener/")


                # CODE TO RUN THE ROBOT PROGRAM - HERE


            else:
                print "Moving files"
                os.system("mv ~/local_Downloader/listener/*.py *.cfg ~/local_Downloader/running")


                # CODE TO RUN THE ROBOT PROGRAM - HERE

           
        else:
            print "No files in directory"

        time.sleep(5)



if __name__ == '__main__':
    run()
