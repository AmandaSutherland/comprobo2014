#!/usr/bin/env python

## Wall follow code for the Neato robots 

import rospy
import time 
import math 
#from math import cos radians sqrt 
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan

#rospy.init_node('listener', anonymous=True)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

desired_distance_to_wall = -1.0
valid_measurements= {}


# def getch():
#     """ Return the next character typed on the keyboard """
#     import sys, tty, termios
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch

def scan_received(msg):
    # gets decent readings from the robot 
    """ Callback function for msg of type sensor_msgs/LaserScan """
    average_distance_wall = 0
    valid_measurements = {}
    for i in range(len(msg.ranges)):
        if msg.ranges[i] > 0 and msg.ranges[i] < 7:
            valid_measurements[i]=(msg.ranges[i])
    if len(valid_measurements) > 0:
        min_angle = min(valid_measurements, key=valid_measurements.get)
        average_distance_wall = sum(valid_measurements.values())/float(len(valid_measurements))
    else:
        average_distance_wall = -1.0 
    angle_increment(valid_measurements)
    cluster_search(valid_measurements)
    #turn_to_wall(valid_measurements)
    nearing_wall(valid_measurements, average_distance_wall, min_angle)
       # obstacle_avoid(valid_measurements)
       # print valid_measurements

def angle_increment(valid_measurements):
    #increments along the angle in dict valid_measurements 
    if index > len(valid_measurements):
        loop_index = index - len(valid_measurements)
    elif index < 0:
        loop_index - index - len(valid_measurements)
    else: loop_index = index
    return loop_index
    print angle_increment

### Wall Follow functions 

def nearing_wall(valid_measurements, average_distance_wall):
    #gets the robit near the wall 
    if average_distance_wall != -1.0 and min_angle <90:
        return Twist(Vector3(0.1, 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
    elif average_distance_wall != -1.0 and 90 < min_angle:
        return Twist(Vector3(-0.1*(average_distance_wall - 1.0), 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
    else:
        return Twist(Vector3(0.0, 0.0, 0.0), Vector3(0.0, 0.0, 0.0))

def turn_to_wall(desired_angle_to_wall):
    #turns to face the wall 
    orient = False 
    follow = False 
    min_angle = 0 
    return Twist(Vector3(0.0, 0.0, 0.0) and Vector3(0.0, 0.0, 0.02*(min_angle - desired_angle_to_wall)))
    orient = True 
    print "Turning to wall. Theoretically orient = True" 
    wallfollow(orient)

def wallfollow(valid_measurements, orient):
    for angle in range(350,360 and 0,10):
        if angle+90 in valid_measurements and 90-angle in valid_measurements:
            back = valid_measurements[angle+90]
            front = valid_measurements[90-angle]
    if not -0.1 < back-front < 0.1:
        follow = False 
    if -0.05 < black - front < 0.05:
        return Twist(Vector3(0.1, 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
    else: 
        return Twist(Vector3(0.1, 0.0, 0.0), Vector3(0.0, 0.0, 0.03*(front-back)))

### Obstacle avoid functions 
 
def define_cluster(point, past_point):
    #determines if points are one thing/cluster 
    angle_change = radians(0)-point(0)
    dist = sqrt(point(1)**2 + past_point(1)**2 - point(1)*past_point(1)*cos(angle_dif))
    if dist < 0.5: 
        return True
    else: 
        return False 

def cluster_search(valid_measurements):
   #looks at valid_measurements and determines if there are data clusters 
   #to avoid 
    lidar_datapoints = []
    for key in valid_measurements.keys():
        lidar_onepoint = key, valid_measurements[key]
        lidar_datapoints.append(lidar_onepoint)
    cluster = []
    for point in lidar_datapoints:
        if cluster == []:
            cluster.append(point)
        elif define_cluster(point, cluster(-1)):
            cluster.apppend(point)
        else:
            cluster.append(cluster)
            cluster = []
    return cluster
    print cluster_search

### other seperate functions 

def publishing_msg():
    #publishes msg and other useful things 
    """ Run loop for the wall node """
    rospy.init_node('wall', anonymous=True)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        msg = Twist(linear=Vector3(x=(desired_distance_to_wall-1)*.2))
        pub.publish(msg)
        r.sleep()


if __name__ == '__main__':
    try:
        sub = rospy.Subscriber('/scan', LaserScan, scan_received)
        rospy.init_node('teleop', anonymous=True)
        """ Run loop for the wall node """
        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            msg = Twist(linear=Vector3(x=(desired_distance_to_wall-1)*.2))
            pub.publish(msg)
            r.sleep
            rospy.spin()
        

    except rospy.ROSInterruptException: pass