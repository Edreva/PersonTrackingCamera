cmake_minimum_required(VERSION 3.12.0)

project(PersonTracker)

find_package( OpenCV REQUIRED )

add_executable (Tracker main.cpp)

target_link_libraries( ${OpenCV_LIBS} )
