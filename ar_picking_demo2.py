#!/usr/bin/env python
# -*- coding: utf-8 -*-    #日本語のコメントを入れるためのおまじない

import sys, math, copy
import rospy, tf, geometry_msgs.msg

from moveit_commander import MoveGroupCommander, RobotCommander
from geometry_msgs.msg import Pose, PoseStamped
from ar_track_alvar_msgs.msg import AlvarMarkers


def open_gripper():
    print("Opening Gripper...")
    gripper_joint_angle[0] = -0.01
    gripper_group.set_joint_value_target(gripper_joint_angle)
    plan2 = gripper_group.go()
    gripper_group.stop()
    gripper_group.clear_pose_targets()
    rospy.sleep(1)


def close_gripper():
    print("Closing Gripper...")
    gripper_joint_angle[0] = 0.0
    gripper_group.set_joint_value_target(gripper_joint_angle)
    plan2 = gripper_group.go()
    gripper_group.stop()
    gripper_group.clear_pose_targets()
    rospy.sleep(1)


ar_pose = geometry_msgs.msg.Pose()

#今回はこの関数は使わない
def ar_marker_CB(msg):
    try:
        listener = tf.TransformListener()
        for marker_data in msg.markers:
            #globals()["position"+str(marker_data.id)] = geometry_msgs.msg.Pose()
            rospy.sleep(1)
            (trans, rot) = listener.lookupTransform('/world', '/ar_marker_%s' %(marker_data.id), rospy.Time(0))
            eval("position"+str(marker_data.id)).position.x = trans[0]
            eval("position"+str(marker_data.id)).position.y = trans[1]
            eval("position"+str(marker_data.id)).position.z = trans[2]
            eval("position"+str(marker_data.id)).orientation.x = rot[0]
            eval("position"+str(marker_data.id)).orientation.y = rot[1]
            eval("position"+str(marker_data.id)).orientation.z = rot[2]
            eval("position"+str(marker_data.id)).orientation.w = rot[3]
    except:
        pass

#rospy.Subscriber('/ar_pose_marker', AlvarMarkers, ar_marker_CB)

if __name__ == '__main__':
    
    node_name = "ar_picking_demo"
    rospy.init_node(node_name, anonymous=True) # ノードの初期化
    
    listener = tf.TransformListener()

    ## MoveGroupCommanderオブジェクトのインスタンス生成。これがジョイントへのインタフェースになる。
    ## このインタフェースは運動計画と動作実行に使われる。
    group = MoveGroupCommander("arm")
    gripper_group = MoveGroupCommander("gripper")    
    group.set_planning_time(600.0) # 動作計画に使う時間[s]の設定
    
    # 初期姿勢の取得
    pose_init = group.get_current_pose()  # エンドエフェクタの位置(x, y, z)を取得
    rospy.loginfo( "Get Initial Pose\n{}".format( pose_init ) )
    rpy_init  = group.get_current_rpy()   # エンドエフェクタの姿勢(roll, pitch, yaw)を取得
    rospy.loginfo("Get Initial RPY:{}".format( rpy_init ) )
    
    # グリッパの初期値を取得
    gripper_joint_angle = gripper_group.get_current_joint_values()
    print("Get Current Gripper angle:\n{}\n".format(gripper_joint_angle))

    marker_number = input("ARマーカーのidを入力:")
    print("marker_number:",marker_number)

    open_gripper()
    rospy.loginfo("Starting Pose 1")
    pose_target_1 = Pose()
    pose_target_1.position.x = 0.03 # エンドエフェクタの位置(x,y,z)を指定
    pose_target_1.position.y = 0.0
    pose_target_1.position.z = 0.10
    yaw = -math.atan2(pose_target_1.position.y, pose_target_1.position.x)
    q = tf.transformations.quaternion_from_euler(yaw, 0.0, 0.0) # エンドエフェクタの姿勢(yaw,pitch,roll)を指定
    pose_target_1.orientation.x =  q[0]
    pose_target_1.orientation.y =  q[1]
    pose_target_1.orientation.z =  q[2]
    pose_target_1.orientation.w =  q[3]   
    group.set_joint_value_target(pose_target_1, True) # 指定された位置姿勢をプランニング
    group.go() # プランニング結果を実行
    rospy.sleep(1.0)
    pose_current = group.get_current_pose()
    rospy.loginfo("Get Current Pose:\n{}\n".format(pose_current )) 
     
    rospy.loginfo("Starting Pose 2")
    pose_target_2 = Pose()
    ##############################
    ###以下マーカーのピッキング###
    ##############################
    marker_position = eval("position"+str(marker_number))
    print("marker:",marker_position.position.x)
    #指定マーカーの座標を取得
    (trans, rot) = listener.lookupTransform('/world', '/ar_marker_%s' %(str(marker_number)), rospy.Time(0))
    #座標を代入
    pose_target_2.position.x = trans[0]#marker_position.position.x
    pose_target_2.position.y = trans[1]#marker_position.position.y
    pose_target_2.position.z = trans[2] + 0.04#marker_position.position.z + 0.04 # エンドエフェクタと床の衝突を防ぐために、0.04[m]の余裕を持たせている 
    yaw = -math.atan2(pose_target_2.position.y, pose_target_2.position.x)
    q = tf.transformations.quaternion_from_euler(yaw, math.pi/2.0, 0.0)
    pose_target_2.orientation.x = q[0]
    pose_target_2.orientation.y = q[1]
    pose_target_2.orientation.z = q[2]
    pose_target_2.orientation.w = q[3]
    group.set_joint_value_target(pose_target_2, True)
    #実行
    group.go()    
    rospy.sleep(1.0)
    pose_current = group.get_current_pose()
    rospy.loginfo( "Get Current Pose:\n{}\n".format(pose_current)) 
    close_gripper()

    rospy.loginfo("Starting Pose 3")
    pose_target_3 = Pose()
    pose_target_3.position.x = 0.1
    pose_target_3.position.y = 0.1
    pose_target_3.position.z = 0.15
    yaw = -math.atan2(pose_target_3.position.y, pose_target_3.position.x)
    q = tf.transformations.quaternion_from_euler(yaw, math.pi/4.0, 0.0)
    pose_target_3.orientation.x =  q[0]
    pose_target_3.orientation.y =  q[1]
    pose_target_3.orientation.z =  q[2]
    pose_target_3.orientation.w =  q[3]   
    group.set_joint_value_target(pose_target_3, True)
    group.go()
    rospy.sleep(1.0)
    pose_current = group.get_current_pose()
    rospy.loginfo("Get Current Pose:\n{}\n".format(pose_current))
    open_gripper()
    
    rospy.loginfo("Starting Pose 4")
    pose_target_4 = Pose()
    pose_target_4.position.x = 0.05
    pose_target_4.position.y = 0.0
    pose_target_4.position.z = 0.15
    yaw = -math.atan2(pose_target_4.position.y, pose_target_4.position.x)
    q = tf.transformations.quaternion_from_euler(yaw, 0.0, 0.0)
    pose_target_4.orientation.x =  q[0]
    pose_target_4.orientation.y =  q[1]
    pose_target_4.orientation.z =  q[2]
    pose_target_4.orientation.w =  q[3]   
    group.set_joint_value_target(pose_target_4, True)
    group.go()
    rospy.sleep(1.0)
    pose_current = group.get_current_pose()
    rospy.loginfo("Get Current Pose:\n{}\n".format(pose_current))
