#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image, PointCloud2
from cv_bridge import CvBridge
import cv2
from sensor_msgs import point_cloud2 as pc2
import numpy as np
import threading
bridge = CvBridge()

depth_image = None
color_image = None
point_cloud = None
lock = threading.Lock()

def depth_callback(msg):
    global depth_image
    try:
        with lock:
            # 将ROS的Image消息转换为OpenCV图像格式
            depth_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
    except Exception as e:
        print(e)

def color_callback(msg):
    global color_image
    try:
        with lock:
            # 将ROS的Image消息转换为OpenCV图像格式
            color_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    except Exception as e:
        print(e)

def point_cloud_callback(msg):
    global point_cloud
    try:
        with lock:
            point_cloud = msg
    except Exception as e:
        print(e)

def show_images_and_point_cloud():
    while not rospy.is_shutdown():
        with lock:
            if depth_image is not None:
                # 显示深度图像
                cv2.imshow("Depth Image", depth_image)
            if color_image is not None:
                # 显示彩色图像
                cv2.imshow("Color Image", color_image)
            if point_cloud is not None:
                # 提取点云信息
                pc_data = pc2.read_points(point_cloud, field_names=("x", "y", "z"), skip_nans=True)
                pc_array = []
                for p in pc_data:
                    pc_array.append([p[0], p[1], p[2]])
                pc_array = np.array(pc_array)

                # 打印点云信息
                print("Point Cloud Shape:", pc_array.shape)
                print("Point Cloud Sample:")
                print(pc_array[:10, :])

        cv2.waitKey(1)

def main():
    rospy.init_node('kinect_depth_color_viewer', anonymous=True)

    # 创建一个订阅器，订阅Kinect相机的深度图像话题
    rospy.Subscriber('/camera/depth/image_raw', Image, depth_callback)

    # 创建一个订阅器，订阅Kinect相机的彩色图像话题
    rospy.Subscriber('/camera/color/image_raw', Image, color_callback)

    # 创建一个订阅器，订阅Kinect相机的点云话题
    rospy.Subscriber('/camera/depth/points', PointCloud2, point_cloud_callback)

    # 启动显示图像和点云的线程
    thread = threading.Thread(target=show_images_and_point_cloud)
    thread.start()

    rospy.spin()

    # 关闭OpenCV窗口
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
