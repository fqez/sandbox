# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "roscompat: 2 messages, 0 services")

set(MSG_I_FLAGS "-Iroscompat:/home/fran/git/testRos/src/libs/roscompat/msg;-Istd_msgs:/opt/ros/jade/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(roscompat_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg" NAME_WE)
add_custom_target(_roscompat_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "roscompat" "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg" ""
)

get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg" NAME_WE)
add_custom_target(_roscompat_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "roscompat" "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(roscompat
  "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/roscompat
)
_generate_msg_cpp(roscompat
  "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/roscompat
)

### Generating Services

### Generating Module File
_generate_module_cpp(roscompat
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/roscompat
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(roscompat_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(roscompat_generate_messages roscompat_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg" NAME_WE)
add_dependencies(roscompat_generate_messages_cpp _roscompat_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg" NAME_WE)
add_dependencies(roscompat_generate_messages_cpp _roscompat_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(roscompat_gencpp)
add_dependencies(roscompat_gencpp roscompat_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS roscompat_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(roscompat
  "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/roscompat
)
_generate_msg_eus(roscompat
  "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/roscompat
)

### Generating Services

### Generating Module File
_generate_module_eus(roscompat
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/roscompat
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(roscompat_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(roscompat_generate_messages roscompat_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg" NAME_WE)
add_dependencies(roscompat_generate_messages_eus _roscompat_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg" NAME_WE)
add_dependencies(roscompat_generate_messages_eus _roscompat_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(roscompat_geneus)
add_dependencies(roscompat_geneus roscompat_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS roscompat_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(roscompat
  "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/roscompat
)
_generate_msg_lisp(roscompat
  "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/roscompat
)

### Generating Services

### Generating Module File
_generate_module_lisp(roscompat
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/roscompat
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(roscompat_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(roscompat_generate_messages roscompat_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg" NAME_WE)
add_dependencies(roscompat_generate_messages_lisp _roscompat_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg" NAME_WE)
add_dependencies(roscompat_generate_messages_lisp _roscompat_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(roscompat_genlisp)
add_dependencies(roscompat_genlisp roscompat_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS roscompat_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(roscompat
  "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/roscompat
)
_generate_msg_py(roscompat
  "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/roscompat
)

### Generating Services

### Generating Module File
_generate_module_py(roscompat
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/roscompat
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(roscompat_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(roscompat_generate_messages roscompat_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Pose3d.msg" NAME_WE)
add_dependencies(roscompat_generate_messages_py _roscompat_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/fran/git/testRos/src/libs/roscompat/msg/Num.msg" NAME_WE)
add_dependencies(roscompat_generate_messages_py _roscompat_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(roscompat_genpy)
add_dependencies(roscompat_genpy roscompat_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS roscompat_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/roscompat)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/roscompat
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(roscompat_generate_messages_cpp std_msgs_generate_messages_cpp)

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/roscompat)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/roscompat
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
add_dependencies(roscompat_generate_messages_eus std_msgs_generate_messages_eus)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/roscompat)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/roscompat
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(roscompat_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/roscompat)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/roscompat\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/roscompat
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(roscompat_generate_messages_py std_msgs_generate_messages_py)
