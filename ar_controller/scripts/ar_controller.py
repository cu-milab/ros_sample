#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from ar_track_alvar_msgs.msg import AlvarMarkers

class turtleSim:
    def __init__(self):
        rospy.init_node('move_turtlesim', anonymous=True)
        self.twist_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1000)
        self.sub = rospy.Subscriber("/ar_pose_marker", AlvarMarkers, self.markerCallback) 
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        self.twist_pub.publish(twist)

        self.markers = []

 
    def markerCallback(self, marker):
        twist = Twist()
        r = rospy.Rate(10)
         
        twist.linear.x = 1.0
        twist.angular.z = 0.0

        for m in marker.markers: 
            # id4のマーカーを発見したら
            if(m.id == 4):
                for i in range(0, 10):
                    # ロボットの並進速度を配信
                    self.twist_pub.publish(twist)
                    # スリープ
                    r.sleep()

                    # 並進速度(x,y,z)と回転角速度(x,y,z,w)を表示
                    print(m.pose.pose.position.x, m.pose.pose.position.y, m.pose.pose.position.z, m.pose.pose.orientation.x, m.pose.pose.orientation.y, m.pose.pose.orientation.z, m.pose.pose.orientation.w)
            
 
if __name__ == '__main__':
 
    try:
        ts = turtleSim()
        rospy.spin()
    except rospy.ROSInterruptException: pass
