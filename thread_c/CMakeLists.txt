cmake_minimum_required(VERSION 2.8.3)
project(multi_rtsp)

set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_FLAGS "-std=c++17 -pthread")
#-DEIGEN_USE_MKL_ALL")
#set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")


if(CMAKE_BUILD_TYPE AND (CMAKE_BUILD_TYPE STREQUAL "Debug"))
    message("Debug mode:${CMAKE_C_FLAGS_DEBUG}")
elseif(CMAKE_BUILD_TYPE AND (CMAKE_BUILD_TYPE STREQUAL "Release"))
    message("Release mode:${CMAKE_C_FLAGS_RELEASE}")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")
else()
    message("else:${CMAKE_BUILD_TYPE}")
    message("else:${CMAKE_C_FLAGS_RELEASE}")
endif()

find_package(OpenCV REQUIRED)

# message(WARNING "OpenCV_VERSION: ${OpenCV_VERSION}")


set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
#set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} "-pthread")


#include_directories(src)
#add_subdirectory(./ThirdParty/GeographicLib/)
#include_directories(./ThirdParty/GeographicLib/include/)


add_executable(multi_rtsp
        video_streaming.h
        video_streaming.cpp
        multi_rtsp.cpp
#        src/ros_node_test.cpp
#        src/main_vins_no_ros.cpp
#        src/main_rtk_gps_converter.cpp
#        src/main_global_bundle_ajustment.cpp
        )

target_link_libraries(multi_rtsp
        ${OpenCV_LIBS}
        )


#add_executable(colmap_fusion
#        src/estimator/parameters.cpp
#        src/estimator/estimator.cpp
#        src/estimator/feature_manager.cpp
#        src/factor/pose_local_parameterization.cpp
#        src/factor/projectionTwoFrameOneCamFactor.cpp
#        src/factor/projectionTwoFrameTwoCamFactor.cpp
#        src/factor/projectionOneFrameTwoCamFactor.cpp
#        src/factor/marginalization_factor.cpp
#        src/utility/utility.cpp
#        src/utility/visualization.cpp
#        src/utility/CameraPoseVisualization.cpp
#        src/initial/solve_5pts.cpp
#        src/initial/initial_aligment.cpp
#        src/initial/initial_sfm.cpp
#        src/initial/initial_ex_rotation.cpp
#        src/featureTracker/feature_tracker.cpp
#        src/colmap_fusion.cpp)
#
#target_link_libraries(colmap_fusion
#        ${catkin_LIBRARIES}
#        ${OpenCV_LIBS}
#        ${CERES_LIBRARIES}
#        )


#add_executable(colmap_fusion src/colmap_fusion_test.cpp)
#target_link_libraries(colmap_fusion vins_lib)

#add_executable(kitti_odom_test src/KITTIOdomTest.cpp)
#target_link_libraries(kitti_odom_test vins_lib)

#add_executable(kitti_gps_test src/KITTIGPSTest.cpp)
#target_link_libraries(kitti_gps_test vins_lib)

