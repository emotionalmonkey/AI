#!/usr/bin/env python

"""
This is a skeleton code.
"""

from copy import deepcopy
import math
import numpy
import random
from threading import Thread, Lock
import sys

import actionlib
import control_msgs.msg
import geometry_msgs.msg
import moveit_commander
import moveit_msgs.msg
import moveit_msgs.srv
import rospy
import sensor_msgs.msg
import tf
import trajectory_msgs.msg

def convert_to_message(T):
    t = geometry_msgs.msg.Pose()
    position = tf.transformations.translation_from_matrix(T)
    orientation = tf.transformations.quaternion_from_matrix(T)
    t.position.x = position[0]
    t.position.y = position[1]
    t.position.z = position[2]
    t.orientation.x = orientation[0]
    t.orientation.y = orientation[1]
    t.orientation.z = orientation[2]
    t.orientation.w = orientation[3]        
    return t

def convert_from_message(msg):
    R = tf.transformations.quaternion_matrix((msg.orientation.x,
                                              msg.orientation.y,
                                              msg.orientation.z,
                                              msg.orientation.w))
    T = tf.transformations.translation_matrix((msg.position.x, 
                                               msg.position.y, 
                                               msg.position.z))
    return numpy.dot(T,R)

def convert_from_trans_message(msg):
    R = tf.transformations.quaternion_matrix((msg.rotation.x,
                                              msg.rotation.y,
                                              msg.rotation.z,
                                              msg.rotation.w))
    T = tf.transformations.translation_matrix((msg.translation.x, 
                                               msg.translation.y, 
                                               msg.translation.z))
    return numpy.dot(T,R)
   
class Node(object):
    def __init__(self, config, parent=None):
        self.config = config
        self.parent = parent           

class MoveArm(object):

    def __init__(self):
        print "Motion Planning Initializing..."
        # Prepare the mutex for synchronization
        self.mutex = Lock()

        # Some info and conventions about the robot that we hard-code in here
        # min and max joint values are not read in Python urdf, so we must hard-code them here
        self.num_joints = 7
        self.q_min = []
        self.q_max = []
        self.q_min.append(-3.1459);self.q_max.append(3.1459)
        self.q_min.append(-3.1459);self.q_max.append(3.1459)
        self.q_min.append(-3.1459);self.q_max.append(3.1459)
        self.q_min.append(-3.1459);self.q_max.append(3.1459)
        self.q_min.append(-3.1459);self.q_max.append(3.1459)
        self.q_min.append(-3.1459);self.q_max.append(3.1459)
        self.q_min.append(-3.1459);self.q_max.append(3.1459)
        # How finely to sample each joint
        self.q_sample = [0.05, 0.05, 0.05, 0.1, 0.1, 0.1, 0.1]
        self.joint_names = ["lwr_arm_0_joint",
                            "lwr_arm_1_joint",
                            "lwr_arm_2_joint",
                            "lwr_arm_3_joint",
                            "lwr_arm_4_joint",
                            "lwr_arm_5_joint",
                            "lwr_arm_6_joint"]

        # Subscribes to information about what the current joint values are.
        rospy.Subscriber("/joint_states", sensor_msgs.msg.JointState, 
                         self.joint_states_callback)

        # Subscribe to command for motion planning goal
        rospy.Subscriber("/motion_planning_goal", geometry_msgs.msg.Transform,
                         self.move_arm_cb)

        # Publish trajectory command
        self.pub_trajectory = rospy.Publisher("/joint_trajectory", trajectory_msgs.msg.JointTrajectory, 
                                              queue_size=1)        

        # Initialize variables
        self.joint_state = sensor_msgs.msg.JointState()

        # Wait for moveit IK service
        rospy.wait_for_service("compute_ik")
        self.ik_service = rospy.ServiceProxy('compute_ik',  moveit_msgs.srv.GetPositionIK)
        print "IK service ready"

        # Wait for validity check service
        rospy.wait_for_service("check_state_validity")
        self.state_valid_service = rospy.ServiceProxy('check_state_validity',  
                                                      moveit_msgs.srv.GetStateValidity)
        print "State validity service ready"

        # Initialize MoveIt
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.group_name = "lwr_arm"
        self.group = moveit_commander.MoveGroupCommander(self.group_name) 
        print "MoveIt! interface ready"

        # Options
        self.subsample_trajectory = True
        print "Initialization done."

    def get_joint_val(self, joint_state, name):
        if name not in joint_state.name:
            print "ERROR: joint name not found"
            return 0
        i = joint_state.name.index(name)
        return joint_state.position[i]

    def set_joint_val(self, joint_state, q, name):
        if name not in joint_state.name:
            print "ERROR: joint name not found"
        i = joint_state.name.index(name)
        joint_state.position[i] = q

    """ Given a complete joint_state data structure, this function finds the values for 
    our arm's set of joints in a particular order and returns a list q[] containing just 
    those values.
    """
    def q_from_joint_state(self, joint_state):
        q = []
        for i in range(0,self.num_joints):
            q.append(self.get_joint_val(joint_state, self.joint_names[i]))
        return q

    """ Given a list q[] of joint values and an already populated joint_state, this 
    function assumes that the passed in values are for a our arm's set of joints in 
    a particular order and edits the joint_state data structure to set the values 
    to the ones passed in.
    """
    def joint_state_from_q(self, joint_state, q):
        for i in range(0,self.num_joints):
            self.set_joint_val(joint_state, q[i], self.joint_names[i])

    """ This function will perform IK for a given transform T of the end-effector. It 
    returns a list q[] of 7 values, which are the result positions for the 7 joints of 
    the left arm, ordered from proximal to distal. If no IK solution is found, it 
    returns an empy list.
    """
    def IK(self, T_goal):
        req = moveit_msgs.srv.GetPositionIKRequest()
        req.ik_request.group_name = self.group_name
        req.ik_request.robot_state = moveit_msgs.msg.RobotState()
        req.ik_request.robot_state.joint_state = self.joint_state
        req.ik_request.avoid_collisions = True
        req.ik_request.pose_stamped = geometry_msgs.msg.PoseStamped()
        req.ik_request.pose_stamped.header.frame_id = "world_link"
        req.ik_request.pose_stamped.header.stamp = rospy.get_rostime()
        req.ik_request.pose_stamped.pose = convert_to_message(T_goal)
        req.ik_request.timeout = rospy.Duration(3.0)
        res = self.ik_service(req)
        q = []
        if res.error_code.val == res.error_code.SUCCESS:
            q = self.q_from_joint_state(res.solution.joint_state)
        return q

    """ This function checks if a set of joint angles q[] creates a valid state, or 
    one that is free of collisions. The values in q[] are assumed to be values for 
    the joints of the left arm, ordered from proximal to distal. 
    """
    def is_state_valid(self, q):
        req = moveit_msgs.srv.GetStateValidityRequest()
        req.group_name = self.group_name
        current_joint_state = deepcopy(self.joint_state)
        current_joint_state.position = list(current_joint_state.position)
        self.joint_state_from_q(current_joint_state, q)
        req.robot_state = moveit_msgs.msg.RobotState()
        req.robot_state.joint_state = current_joint_state
        res = self.state_valid_service(req)
        return res.valid 
    
    def find_closest_node(self, tree, new_node):
        min_length = None
        closest_node = None
        for t in tree:
            length = numpy.linalg.norm(new_node - t.config)
            
            if not min_length or length < min_length:
                min_length = length
                closest_node = t
                
                if min_length < 3.3:
                    #print("min_length:",min_length)
                    return closest_node
                
        return closest_node
    

    def is_collision_free(self, q_goal, new_node):
        q_goal = numpy.array(q_goal)
        new_node = numpy.array(new_node)
        # calculate total sections for minimum discretization
        sections = int(round(max(numpy.true_divide(abs(q_goal-new_node), self.q_sample))))  
        
        # value for each section
        sub = (q_goal - new_node)/sections         
        
        # check each segment is collision free randomly
        d = list(range(1,sections))
        
        for i in range(len(d)):
            start_node = new_node + (sub * d.pop(random.randrange(len(d))))
            if not self.is_state_valid(start_node):                
                return False
        
        return True

    def get_path(self, node):
        path = [node.config]
        parent_node = node.parent 
        while parent_node is not None:            
            path.append(parent_node.config)
            parent_node = parent_node.parent
        path.reverse()
        #print("Path", len(path))
        return path if len(path) < 4 else self.trim_node(path)

    def trim_node(self, path):
        # initialize trim_path with q_start
        trim_path = [path[0]]    
        start_index = 0
        last_index = len(path)-1                  
        while start_index < last_index:  

            next_index = start_index+2

            if next_index > last_index:
                trim_path.append(path[start_index+1])                
                return trim_path

            if self.is_collision_free(path[next_index],path[start_index]):
                trim_path.append(path[next_index])
                start_index = next_index      
            else: 
                trim_path.append(path[start_index+1])
                start_index+=1
        
        return trim_path

    def motion_plan(self, q_start, q_goal, q_min, q_max):        
        #print(q_start, q_goal)
        # Replace this with your code
        tree = set()
        tree.add(Node(q_start))
        max_node = 0        
        while max_node < 1000:            
            new_node = numpy.array([random.uniform(q_min[j],q_max[j]) for j in range(self.num_joints)])
            if self.is_state_valid(new_node):
                max_node +=1
                
                closest_node = self.find_closest_node(tree,new_node)
                if self.is_collision_free(new_node,closest_node.config):
                    node = Node(new_node,closest_node)
                    tree.add(node)
                    
                    if self.is_collision_free(q_goal,new_node):
                        goal = Node(q_goal,node)
                        tree.add(goal)
                        return self.get_path(goal)
                        
        
        print("Do not find the path to goal")        
        return [q_start,q_goal]  
        # ===========================

    
    def create_trajectory(self, q_list, v_list, a_list, t):
        joint_trajectory = trajectory_msgs.msg.JointTrajectory()
        for i in range(0, len(q_list)):
            point = trajectory_msgs.msg.JointTrajectoryPoint()
            point.positions = list(q_list[i])
            point.velocities = list(v_list[i])
            point.accelerations = list(a_list[i])
            point.time_from_start = rospy.Duration(t[i])
            joint_trajectory.points.append(point)
        joint_trajectory.joint_names = self.joint_names
        return joint_trajectory

    def create_trajectory(self, q_list):
        joint_trajectory = trajectory_msgs.msg.JointTrajectory()
        for i in range(0, len(q_list)):
            point = trajectory_msgs.msg.JointTrajectoryPoint()
            point.positions = list(q_list[i])
            joint_trajectory.points.append(point)
        joint_trajectory.joint_names = self.joint_names
        return joint_trajectory

    def project_plan(self, q_start, q_goal, q_min, q_max):
        q_list = self.motion_plan(q_start, q_goal, q_min, q_max)
        joint_trajectory = self.create_trajectory(q_list)
        return joint_trajectory

    def move_arm_cb(self, msg):
        T = convert_from_trans_message(msg)
        self.mutex.acquire()
        q_start = self.q_from_joint_state(self.joint_state)
        print "Solving IK"
        q_goal = self.IK(T)
        if len(q_goal)==0:
            print "IK failed, aborting"
            self.mutex.release()
            return
        print "IK solved, planning"
        trajectory = self.project_plan(numpy.array(q_start), q_goal, self.q_min, self.q_max)
        if not trajectory.points:
            print "Motion plan failed, aborting"
        else:
            print "Trajectory received with " + str(len(trajectory.points)) + " points"
            self.execute(trajectory)
        self.mutex.release()
        
    def joint_states_callback(self, joint_state):
        self.mutex.acquire()
        self.joint_state = joint_state
        self.mutex.release()

    def execute(self, joint_trajectory):
        self.pub_trajectory.publish(joint_trajectory)

if __name__ == '__main__':
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_arm', anonymous=True)
    ma = MoveArm()
    rospy.spin()