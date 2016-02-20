"""
File: Blind_Aid_Driver.py
Description: Driver for Blind Aid Glasses that listens for button
	presses for increasing, decreasing, muting volume and muting 
	motor vibration. Also maps IR Sensor range to a motor duty cycle
	effectively varying the vibration for haptic range feedback.
	As the range increases the vibration decreases as the range decreases
	the vibration intensifies.
Date Created: February 18, 2016
Date Last Edited: February 18, 2016
Author: Cameron Costanzo
Group: Jared Charter, Hayley Day, Gage Gwillim
"""	

import Dependencies.IRSensor as IRS
import Dependencies.Motor as Motor
import Dependencies.buttons as Buttons
import RPi.GPIO as GPIO
import time

#Constants
MAX_INTENSITY = 90
MIN_INTENSITY = 30
MAX_RANGE = 150
MIN_RANGE = 15
VOLUME_UP_PIN = 32
VOLUME_DOWN_PIN = 36
VOLUME_MUTE_PIN = 38
MOTOR_0_PIN = 16
MOTOR_1_PIN = 18
MOTOR_MUTE_PIN = 40
DEBOUNCE = 300

#Initialize GPIOs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(VOLUME_UP_PIN, GPIO.IN)
GPIO.setup(VOLUME_DOWN_PIN, GPIO.IN)
GPIO.setup(VOLUME_MUTE_PIN, GPIO.IN)
GPIO.setup(MOTOR_MUTE_PIN, GPIO.IN)

#Globals
volume = 100
motormute = False
muted = False

global motor0
motor0 = Motor.Motor(MOTOR_0_PIN)
global motor1
motor1 = Motor.Motor(MOTOR_1_PIN)

def scaleIntensity(range):
	intensity = (((MAX_INTENSITY - MIN_INTENSITY)*(MAX_RANGE - range))/(MAX_RANGE-MIN_RANGE)) + MIN_INTENSITY
	intensity = int(intensity)
	return intensity

def motor_mute(channel):
	global motor0
	global motor1
	global motormute
	if not motormute:
		print "Motor mute"
		motormute = True
		motor0.motorMute()
		motor1.motorMute()
	else:
		print "Motor unmute"
		motormute = False
		print int(motor0.getIntensity())
		print int(motor1.getIntensity())
		motor0.changeIntensity(int(motor0.getIntensity()))
		motor1.changeIntensity(int(motor1.getIntensity()))
	
GPIO.add_event_detect(VOLUME_UP_PIN, GPIO.RISING, callback=Buttons.volume_up, bouncetime=DEBOUNCE)
GPIO.add_event_detect(VOLUME_DOWN_PIN, GPIO.RISING, callback=Buttons.volume_down, bouncetime=DEBOUNCE)
GPIO.add_event_detect(VOLUME_MUTE_PIN, GPIO.RISING, callback=Buttons.volume_mute, bouncetime=DEBOUNCE)
GPIO.add_event_detect(MOTOR_MUTE_PIN, GPIO.RISING, callback=motor_mute, bouncetime=DEBOUNCE)


if __name__ == '__main__':
	global motor0
	global motor1
	print "Blind-Aid Driver started."
	irsensor0 = IRS.IRSensor(0)
	irsensor1 = IRS.IRSensor(1)
	
	try:
		range0 = 0
		range1 = 0
		intensity0 = 0
		intensity1 = 0
		print "Got in try"
		while(1):
			time.sleep(.1)
			# Get IR 0 Range
			range0 = irsensor0.updateRange()
			range0 = int(range0)
			# Get IR 1 Range
			range1 = irsensor0.updateRange()
			range1 = int(range1)
			# Scale motor intensity 0
			intensity0 = scaleIntensity(range0)
			# Scale motor intensity 1
			intensity1 = scaleIntensity(range1)
			print intensity0
			print intensity1
			# Updating the motor 0 intensity(changing duty cycle)
			if (MIN_RANGE <= range0 <= MAX_RANGE):
				#print "Intensity: ",intensity,
				#print "Range: ",range
				motor0.changeIntensity(intensity0)
			elif (range0 > MAX_RANGE):
				#print "Farther than 150 cm"
				motor0.changeIntensity(MAX_INTENSITY)
			elif range0 < MIN_RANGE:
				#print "Shorter than 15 cm"
				motor0.changeIntensity(0)

			# Updating the motor 1 intensity(changing duty cycle)
			if (MIN_RANGE <= range1 <= MAX_RANGE):
				#print "Intensity: ",intensity,
				#print "Range: ",range
				motor1.changeIntensity(intensity1)
			elif (range1 > MAX_RANGE):
				#print "Farther than 150 cm"
				motor1.changeIntensity(MAX_INTENSITY)
			elif range1 < MIN_RANGE:
				#print "Shorter than 15 cm"
				motor1.changeIntensity(0)


	except KeyboardInterrupt:
		motor0.motorStop()
		GPIO.cleanup()
		print "\nExiting..."
