#!/usr/bin/env python
import time
import pigpio
import math

PULSE_WIDTH = 1500
MIN_PULSE_WIDTH = 500
MAX_PULSE_WIDTH = 2500

# Width change variable
WIDTH_CHANGE = 70

# Sleep time
DELAY = 0.4

# Initial values of servo motors
BASE_PULSE_INIT = 1260
ARM1_PULSE_INIT = 1350 # calculated
ARM2_PULSE_INIT = 1000
GRIPPER_PULSE_INIT = 1850
CLAW_PULSE_INIT = 1800

CLAW_OPEN = 1000
CLAW_CLOSE = 1600

right_box = [860.0, 1325.0, 1150.0, 1075]
left_box = [1710.0, 1325.0, 1150.0, 1075]


## pulseInitial = [1100, 1100, ARM2_PULSE_INIT, GRIPPER_PULSE_INIT]
## pulseFinal = [1600, 1700, ARM2_PULSE_INIT, GRIPPER_PULSE_INIT]

# GPIO connection pins
baseGPIO = 2
arm1GPIO = 3
arm2GPIO = 4
gripperGPIO = 17
clawGPIO = 27

# Initial pulses of motors
pulseBase = BASE_PULSE_INIT
pulseArm1 = ARM1_PULSE_INIT
pulseArm2 = ARM2_PULSE_INIT
pulseGripper = GRIPPER_PULSE_INIT
pulseClaw = CLAW_PULSE_INIT

# Claw Positions
clawOpenPosition = CLAW_OPEN
clawClosePosition = CLAW_CLOSE


class motor(object):
    # Class self parameters declaration
    def __init__(self, gpioPin, initPulse):
        print 'Initialised'
        self.motorPi = pigpio.pi()
        self.initialPos = initPulse 
        self.pulse = initPulse
        self.gpioPin = gpioPin

    def simpleMove(self, nextPulse):
        self.motorPi.set_servo_pulsewidth(self.gpioPin, nextPulse)
        print("Servo moved to {} micro pulses".format(nextPulse))
        
    # Move motor to destination pulse
    def move(self, nextPulse):
        # Calcute change required to reach destination
        pwmWidthChange = nextPulse - self.pulse
        # Initialise 2 variables for later use
        initial = self.pulse
        position = initial

        # Calculate new pulse of the motor
        self.pulse += pwmWidthChange
        
        # Define velocity and accelaration values
        velocity = 5
        acceleration = 2

        # Limit destination pulse between 500 -2500
        if self.pulse < 500:
            self.pulse = MIN_PULSE_WIDTH
            print "Minimum position reached."

        if self.pulse > 2500:
            self.pulse = MAX_PULSE_WIDTH
            print "Max position reached."

        # Use this variable for loop
        destination = self.pulse

        # while position of motor is between initial and destination position
        while min(initial, destination)<= position <= max(initial, destination):
            # Mid point calculation of motion for changing accelaration
            middle = initial + (destination - initial)/2
            # Set accelaration direction, accelaration is positive halfway and negative in the other half
            acc_direction = 1 if min(initial, middle) <= position <= max(initial, middle) else -0.6
            vel_direction = 1 if destination >= initial else -1 


            self.motorPi.set_servo_pulsewidth(self.gpioPin, position)
            
            # Update position and velocity according to velocity and accelaration respectively
            position +=  vel_direction * velocity
            velocity += acc_direction * acceleration

            # Set maximum and minimum velocity limits. Calculated by practical trail and error
            velocity = 20 if velocity > 20 else velocity
            velocity = 5 if velocity < 5 else velocity
            print ("Position : {}".format(position))
            print ("Velocity : {}".format(velocity))
            # Delay to be safe
            time.sleep(0.005)

        # This set_servo_pulsewidth is probably redundant, but I don't want to remove it, because I trust by earlier self.
        self.motorPi.set_servo_pulsewidth(self.gpioPin, self.pulse)
        print("Servo moved to {} micro pulses".format(self.pulse))


    def stop(self):
        # End class connection
        self.motorPi.stop()

# Motor class initialisation
base = motor(baseGPIO, BASE_PULSE_INIT)
arm1 = motor(arm1GPIO, ARM1_PULSE_INIT)
arm2 = motor(arm2GPIO, ARM2_PULSE_INIT)
gripper = motor(gripperGPIO, GRIPPER_PULSE_INIT)
claw = motor(clawGPIO, CLAW_PULSE_INIT)


def moveToInitial():
    # move to initial positions
    base.move(base.initialPos)
    time.sleep(0.1)
    arm2.move(arm2.initialPos)
    time.sleep(0.1)
    arm1.move(arm1.initialPos)
    time.sleep(0.1)
    gripper.move(gripper.initialPos)
    time.sleep(0.1)
    # claw.move(claw.initialPos)

def moveMotors(pulse_widths):   

    try:  
        # move motor only whe button is pressed. Safety step.
        # button = raw_input("Press button to move the motors.")

        print "Base :"
        print pulse_widths[0]
        base.move(pulse_widths[0])

        time.sleep(0.2)

        print "Arm2 :"
        print pulse_widths[2]
        if pulse_widths[2] < arm2.pulse:
            arm2.simpleMove(pulse_widths[2])
        else:
            arm2.move(pulse_widths[2])

        time.sleep(0.2)

        print "Arm1 :"
        print pulse_widths[1]
        arm1.move(pulse_widths[1])
        time.sleep(0.2)
        
        print "Gripper :"
        print pulse_widths[3]
        gripper.move(pulse_widths[3])

        time.sleep(0.2)
        
        
    except KeyboardInterrupt:
        # End the code by keyboard interrupt 
        moveToInitial()
        base.stop()
        arm1.stop()
        arm2.stop()
        gripper.stop()
        print "Program exited"

def open_claw():
    claw.simpleMove(CLAW_OPEN)
    print "Claw is open."

def close_claw():
    claw.simpleMove(CLAW_CLOSE)
    print "Claw is closed."

def pick_drop():
    open_claw()
    time.sleep(0.5)
    close_claw()
    time.sleep(0.5)
    print "Pick/drop complete."

def returnToInitial():
    gripper.move(gripper.initialPos)
    time.sleep(0.1)
    arm2.move(arm2.initialPos)
    time.sleep(0.1)
    arm1.move(arm1.initialPos)
    time.sleep(0.1)
    base.move(base.initialPos)
    time.sleep(0.1)
    
def transitPosition():
    arm2.move(825)
    time.sleep(0.1)
    arm1.move(1500)
    time.sleep(0.1)
    base.move(base.pulse)
    time.sleep(0.1)

        



        
        
