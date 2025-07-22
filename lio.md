[Home](./index.html)

Akshay Gulabrao 19 July 2025

# LIDAR Odometry

A current difficulty in robotics is localization with respect to features in GPS/GNSS denied areas. In such areas, robots must use features which are stable and discard unstable features. Humans intuitively have a grasp of what is reliable as a feature and unrealiable. Robots currently fuse together sensor information of:

1. An IMU, which streams angular and linear acceleration
2. A camera, which can find stationary points while in motion
3. LiDAR, which provides accurate depth measurements

IMUs should be paired with camera or LiDAR because IMUs have error in the acceleration, which accumulates over time. 

## The Kalman Filter

Popular tool to deal with sensor noise systematically. They merge a model of prediction error with sensor error.
