project(test)

cmake_minimum_required(VERSION 2.8.3)

find_package(catkin REQUIRED COMPONENTS visualstates
)

catkin_package()
include_directories(${catkin_INCLUDE_DIRS})
install(PROGRAMS test.py DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
