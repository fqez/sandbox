include_directories(
    ${GAZEBO_INCLUDE_DIRS}
    ${INTERFACES_CPP_DIR}
    ${LIBS_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${easyiceconfig_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Headers trick for IDEs
file(GLOB_RECURSE turtlebot_headers "include/**")
add_library(turtlebot_headers ${turtlebot_headers})
set_target_properties(turtlebot_headers PROPERTIES LINKER_LANGUAGE CXX)

link_directories(
    ${GAZEBO_LIBRARY_DIRS}
    ${easyiceconfig_LIBRARY_DIRS}
)

#set( CMAKE_CXX_FLAGS "-Wall" )

set(SOURCES src/f1plugin.cc
        src/f1ice.cc

        src/f1control.cc
        src/f1sensors.cc

        src/cameraproxy.cc

        src/interfaces/motorsi.cpp
        src/interfaces/laseri.cpp
        src/interfaces/pose3di.cpp
        src/interfaces/camerai.cpp
        src/interfaces/pushcamerai.cpp
        src/interfaces/cameraibase.cpp
)

add_library(f1plugin SHARED ${SOURCES})
# Gazebo
target_link_libraries(f1plugin ${GAZEBO_libraries})
set_target_properties(f1plugin PROPERTIES COMPILE_FLAGS "${GAZEBO_CXX_FLAGS}")

# Ice
target_link_libraries(f1plugin
        Ice
        IceUtil
        JderobotInterfaces
        ${ZeroCIce_LIBRARIES}
        ${easyiceconfig_LIBRARIES}
)

# Application
target_link_libraries(f1plugin
        ${OpenCV_LIBS}
        ${PCL_LIBRARIES}
        ${OpenCV_LIBRARIES}
        CameraPlugin
        colorspacesmm
)

INSTALL (TARGETS f1plugin DESTINATION share/jderobot/gazebo/plugins/f1/ COMPONENT core)
FILE(GLOB_RECURSE CFG_FILES ${CMAKE_CURRENT_SOURCE_DIR}/cfg/*.cfg)
INSTALL (FILES ${CFG_FILES} DESTINATION share/jderobot/gazebo/plugins/f1/ COMPONENT core)

