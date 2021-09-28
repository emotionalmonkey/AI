#!/usr/bin/env python

"""
This is a skeleton code.
"""

import rospy
import numpy
import tf
import tf2_ros
import geometry_msgs.msg

def publish_transforms():  
    #object_transform
    tr1 = tf.transformations.translation_matrix((0.0, 1.0, 1.0))
    q1 = tf.transformations.quaternion_matrix(tf.transformations.quaternion_from_euler(0.79, 0.0, 0.79))
    T1 = tf.transformations.concatenate_matrices(q1,tr1)
    send_transform(T1, "base_frame", "object_frame")

    #robot_transform
    tr2 = tf.transformations.translation_matrix((0.0, -1.0, 0.0))
    q2 = tf.transformations.quaternion_matrix(tf.transformations.quaternion_about_axis(1.5, (0,0,1)))  
    T2 = tf.transformations.concatenate_matrices(q2,tr2)
    send_transform(T2, "base_frame", "robot_frame")    
    
    #robot_to_camera
    tr3 = tf.transformations.translation_matrix((0.0, 0.1, 0.1))
    q3 = tf.transformations.quaternion_matrix(tf.transformations.quaternion_from_euler(0.0, 0.0, 0.0))
    T3 = tf.transformations.concatenate_matrices(q3,tr3)
    
    robot_base = tf.transformations.inverse_matrix(T2)
    camera_robot = tf.transformations.inverse_matrix(T3)
    camera_object = tf.transformations.concatenate_matrices(camera_robot,robot_base,T1) 
    
    camera_tr = tf.transformations.translation_from_matrix(camera_object)  
       
    x_axis = (1,0,0)
    uv1 = x_axis/ numpy.linalg.norm(x_axis)
    uv2 = camera_tr /numpy.linalg.norm(camera_tr)
    dotProduct = numpy.dot(uv1,uv2)
    angle = numpy.arccos(dotProduct)
    crossProduct = numpy.cross(x_axis,camera_tr) 
    
    q3 = tf.transformations.quaternion_matrix(tf.transformations.quaternion_about_axis(angle, crossProduct)) 
    T3 = tf.transformations.concatenate_matrices(T3,q3)
    send_transform(T3, "robot_frame","camera_frame") #camera_transform    
    
def send_transform(T, parent, child):
    t = geometry_msgs.msg.TransformStamped()
    t.header.frame_id = parent
    t.header.stamp = rospy.Time.now()
    t.child_frame_id = child
    translation = tf.transformations.translation_from_matrix(T)
    rotation = tf.transformations.quaternion_from_matrix(T)
    t.transform.translation.x = translation[0]
    t.transform.translation.y = translation[1]
    t.transform.translation.z = translation[2]
    t.transform.rotation.x = rotation[0]
    t.transform.rotation.y = rotation[1]
    t.transform.rotation.z = rotation[2]
    t.transform.rotation.w = rotation[3]        
    br.sendTransform(t)

if __name__ == '__main__':
    rospy.init_node('project2_solution')

    br = tf2_ros.TransformBroadcaster()
    rospy.sleep(0.5)

    while not rospy.is_shutdown():
        publish_transforms()
        rospy.sleep(0.05)
