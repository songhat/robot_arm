execute_process(COMMAND "/home/songhat/catkin_ws/build/panda_gazebo/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/songhat/catkin_ws/build/panda_gazebo/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
