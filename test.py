import rospy
from panda_robot import PandaArm
rospy.init_node("panda_demo") # initialise ros node
r = PandaArm() # create PandaArm instance
r.move_to_neutral() # moves robot to neutral pose; uses moveit if available, else JointTrajectory action client
pos,ori = r.ee_pose() # get current end-effector pose (3d position and orientation quaternion of end-effector frame in base frame)
r.get_gripper().home_joints() # homes gripper joints
r.get_gripper().open() # open gripper
r.get_gripper().close()
r.move_to_joint_position([-8.48556818e-02, -8.88127666e-02, -6.59622769e-01, -1.57569726e+00, -4.82374882e-04,  2.15975946e+00,  4.36766917e-01]) # move robot to the specified pose
r.move_to_cartesian_pose(pos,ori) # move the robot end-effector to pose specified by 'pos','ori'