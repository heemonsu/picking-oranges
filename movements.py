from kinematics import *
from motorControl import *

right_box = [860.0, 1325.0, 1150.0, 1075]
left_box = [1710.0, 1325.0, 1150.0, 1075]

# def openClaw():
# 	open_claw()

# def closeClaw():
# 	close_claw()

def goToCoordinate(coordinate):
	## Function to move motors

	# Calculate arm joint angles from coordinate values
	destination_angles = calculateDestinationAngles(coordinate)

	# Calculate pulse width need to reach a particular joint angles
	pulse_widths = calculatePulseWidth(destination_angles)

	# move motors
	moveMotors(pulse_widths)
	print "Motors moved."

# def goToInitial():
# 	moveToInital()

def placeOrange(coordinate, maturity):
	moveToInitial()
        open_claw()

        time.sleep(0.5)
        button = raw_input("move to intiial done.")

        goToCoordinate(coordinate)
        time.sleep(0.5)
        close_claw()
	time.sleep(0.5)
	button = raw_input("go to coordinate done.")

        transitPosition()
        time.sleep(0.5)

        button = raw_input("transit position done")
        moveMotors(left_box if maturity==0 else right_box)
        time.sleep(0.5)
        open_claw()

        
        button = raw_input("move to box done.")
        time.sleep(0.5)
        returnToInitial()
        time.sleep(0.5)


