import numpy as np
import math
from math import cos, sin, exp
#from motorControl import *

PLATFORM = 11
ORANGE_RANGE = 2
CLAW_LENGTH = 12
HEIGHT_BASE = 8.5

ARM1 = 20.5
ARM2 = 22.5

def calculateAngle(a, b, c):
	# cosine rule to find angles of a triangle to find joint angles
	cosTheta = (a**2 + b**2 - c**2) / (2*a*b)
	theta = math.acos(cosTheta)
	return theta

def transformToWorld(centroid):
	## TESTED
	# size of the image in centimeters
        widthCM = float(23)
        lengthCM = float(30)
        # size of image in pixels
        IMG_LEN = 1304
        IMG_WIDTH = 1000
        # distance of base of robot from grid of orange
        baseDistance = 14

        # convert pixel coordinates to centimeteres
        coordinateCM =[widthCM/IMG_WIDTH*centroid[0], lengthCM/IMG_LEN*centroid[1]]
        # convert centimeters coordinates into world coordinate frame
        worldCoordinate = [round(coordinateCM[0] - widthCM/2, 1), round(lengthCM - coordinateCM[1] + baseDistance, 1)]
        print worldCoordinate
        return worldCoordinate

###def calculateDestinationAnglesOld(coordinate):
##	## Calculate joint angles from world coordinates. Inverse kinematics
##
##	# z coordinate of end effector 
##	heightEndEffector = PLATFORM + CLAW_LENGTH + ORANGE_RANGE 
##
##	# 3D coordinate of the end effector
##	endEffectorCoordinate = np.array([coordinate[0], coordinate[1], heightEndEffector])
##	# base coordinates
##	baseCoordinate = np.array([0, 0, HEIGHT_BASE])
##
##	# base of triangle between arm1, arm2 and gripper
##	triangleBase = np.linalg.norm(endEffectorCoordinate - baseCoordinate)
##
##	# calculate joint angles
##	angleBase = math.atan2(coordinate[1], coordinate[0])
##	angleArm2 = calculateAngle(ARM1, ARM2, triangleBase)
##	angleArm1 = calculateAngle(,,ARM2)
##	angleGripper = math.pi/2 + math.pi - (angleArm1 + angleArm2)
##
##	return [angleBase, angleArm1, angleArm2, angleGripper]

def calculateDestinationAngles(coordinate):
	## Calculate joint angles from world coordinates. Inverse kinematics
	## TESTED
	# z coordinate of end effector 
	heightEndEffector = PLATFORM + CLAW_LENGTH + ORANGE_RANGE

	# 3D coordinate of the end effector
	endEffectorCoordinate = np.array([coordinate[0], coordinate[1], heightEndEffector])
	#print 'End Effector Coordinate'
	#print endEffectorCoordinate
	# base coordinates
	baseCoordinate = np.array([0, 0, HEIGHT_BASE])
	#print 'Base coordinate'
	#print baseCoordinate

	# base of triangle between arm1, arm2 and gripper
	triangleBase = np.linalg.norm(endEffectorCoordinate - baseCoordinate)
	triangleBaseAngle = math.asin((endEffectorCoordinate[2]-baseCoordinate[2]) / triangleBase)
	#print 'Triangle base'
	#1print triangleBase

	# calculate joint angles
	angleBase = math.atan2(coordinate[1], coordinate[0])
	angleArm1 = triangleBaseAngle + calculateAngle(triangleBase, ARM1, ARM2)
	angleArm2 = calculateAngle(ARM1, ARM2, triangleBase)
	angleGripper = (math.pi/2 - triangleBaseAngle) + math.pi - (calculateAngle(triangleBase, ARM1, ARM2) + angleArm2) 
        print "Base:"
        print math.degrees(angleBase)
        print "Arm1"
        print math.degrees(angleArm1)
        print "Arm2"
        print math.degrees(angleArm2)
        print "Gripper"
        print math.degrees(angleGripper)
        
	return [angleBase, angleArm1, angleArm2, angleGripper]

def calculatePulseWidth(angles):
	## TESTED
	# separate each joint's angle
	baseTheta = math.degrees(angles[0])
	arm1Theta = math.degrees(angles[1])
	arm2Theta = math.degrees(angles[2])
	gripperTheta = math.degrees(angles[3])

	# convert angle to the pulse width required to reach that angle. Calculated by trail and error from practical observations. 
	# Completely dependent on how motors are connected to arm.
	pulseWidthBase = baseLinear(baseTheta)
	pulseWidthArm1 = arm1Profile(arm1Theta)
	pulseWidthArm2 = arm2Profile(arm2Theta)
	pulseWidthGripper = gripperLinear(gripperTheta)

	pulseWidths = [round(pulseWidthBase), round(pulseWidthArm1 - 250), round(pulseWidthArm2), round(pulseWidthGripper)+80]
#	pulseWidths = [round(pulseWidthBase), round(pulseWidthArm1), round(pulseWidthArm2), round(pulseWidthGripper)+170]

	return pulseWidths

def baseProfile(x):
	a0 =1364  
	a1 =59.05  
	b1 =276.9  
	a2 =-83.02  
	b2 =-116.3  
	a3 =60  
	b3 =49.51  
	a4 =-45.38  
	b4 =-12.66  
	a5 =26  
	b5 =-0.3138 
	a6 =-10.68  
	b6 =7.196  
	a7 =6.349  
	b7 =-3.003  
	w =0.05797 

        result = a0 + a1*cos(x*w) + b1*sin(x*w) + a2*cos(2*x*w) + b2*sin(2*x*w) + a3*cos(3*x*w) + b3*sin(3*x*w) + a4*cos(4*x*w) + b4*sin(4*x*w) + a5*cos(5*x*w) + b5*sin(5*x*w) + a6*cos(6*x*w) + b6*sin(6*x*w) + a7*cos(7*x*w) + b7*sin(7*x*w)

	return result

def arm1Profile(x):
	a1 =1511  
	b1 =90.31  
	c1 =50.18  
	a2 =27.99  
	b2 =65.06  
	c2 =3.921
	a3 =31.66
	b3 =55.39  
	c3 =6.103  
	a4 =13.1
	b4 =48.26  
	c4 =2.526
	a5 =574  
	b5 =31.05  
	c5 =28.38 

	result = a1*exp(-((x-b1)/c1)**2) + a2*exp(-((x-b2)/c2)**2) + a3*exp(-((x-b3)/c3)**2) + a4*exp(-((x-b4)/c4)**2) + a5*exp(-((x-b5)/c5)**2)

	return result

def arm2Profile(x):
	a0 =        2765  
	a1 =        1954  
	b1 =        2568  
	a2 =      -211.5  
	b2 =        2725  
	a3 =       -1561  
	b3 =        1384  
	a4 =       -1412  
	b4 =      -71.39  
	a5 =      -558.3  
	b5 =      -608.7 
	a6 =       22.33 
	b6 =      -406.6  
	a7 =       121.2  
	b7 =      -105.6  
	a8 =        46.4 
	b8 =      0.1721 
	w =     0.03954  

	result = a0 + a1*cos(x*w) + b1*sin(x*w) + a2*cos(2*x*w) + b2*sin(2*x*w) + a3*cos(3*x*w) + b3*sin(3*x*w) + a4*cos(4*x*w) + b4*sin(4*x*w) + a5*cos(5*x*w) + b5*sin(5*x*w) + a6*cos(6*x*w) + b6*sin(6*x*w) + a7*cos(7*x*w) + b7*sin(7*x*w) + a8*cos(8*x*w) + b8*sin(8*x*w)

	return result

def gripperProfile(x):

	a0 = -2.835e+007  
	a1 = -5.019e+007  
	b1 =   4.02e+007
	a2 =  5.873e+006  
	b2 =  6.866e+007  
	a3 =  5.353e+007  
	b3 =  1.865e+007  
	a4 =  2.201e+007 
	b4 = -2.706e+007  
	a5 = -8.587e+006 
	b5 = -1.326e+007  
	a6 =  -4.84e+006  
	b6 =  1.393e+006  
	a7 =       -4092  
	b7 =  1.021e+006  
	a8 =  9.626e+004  
	b8 =  2.789e+004  
	w =     0.01231  

	result =a0 + a1*cos(x*w) + b1*sin(x*w) + a2*cos(2*x*w) + b2*sin(2*x*w) + a3*cos(3*x*w) + b3*sin(3*x*w) + a4*cos(4*x*w) + b4*sin(4*x*w) + a5*cos(5*x*w) + b5*sin(5*x*w) + a6*cos(6*x*w) + b6*sin(6*x*w) + a7*cos(7*x*w) + b7*sin(7*x*w) + a8*cos(8*x*w) + b8*sin(8*x*w)

	return result

def arm1Linear(x):
	p1 = 10.41
	p2 = 650.9
	result = p1*x +p2
	return result

def arm2Linear(x):
	p1 = -8.0709
	p2 = 1948
	result = p1*x + p2

def gripperLinear(x):
	p1 = 9.13
	p2 = -95.74
	result = p1 * x + p2
	return result

def baseLinear(x):
	p1 = 8.235
	p2 = 505.5
	result = p1*x + p2
	return result



