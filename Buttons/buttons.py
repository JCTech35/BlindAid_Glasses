"""
File: Buttons.py
Description: Testing using buttons with detect event capabilities
Date Created: February 4, 2016
Date Last Edited: February 4, 2016
Author: Cameron Costanzo
"""

import os
import RPi.GPIO as GPIO
from subprocess import call

VOLUME_UP_PIN = 32
VOLUME_DOWN_PIN = 36
VOLUME_MUTE_PIN = 38
MOTOR_MUTE_PIN = 40

GPIO.setmode(GPIO.BOARD)

GPIO.setup(VOLUME_UP_PIN, GPIO.IN)
GPIO.setup(VOLUME_DOWN_PIN, GPIO.IN)
GPIO.setup(VOLUME_MUTE_PIN, GPIO.IN)
GPIO.setup(MOTOR_MUTE_PIN, GPIO.IN)

volume = 100
muted = False

#Volume UP
def volume_up(channel):
	global volume
	print "Volume up!"
	volume = volume + 5
	if volume >= 100:
		volume = 100
	call(["sudo","amixer","set", "PCM", "--", str(volume)+'%'])
	
#Volume DOWN
def volume_down(channel):
	global volume
	print "Volume down!"
	volume = volume - 5
	if volume <= 0:
		volume = 0
	call(["sudo","amixer","set", "PCM", "--", str(volume)+'%'])

#Motor Mute
def motor_mute(channel):
	print "Motor mute"

#Volume Mute
def volume_mute(channel):
	global volume
	global muted
	if muted:
		print "Unmute"
		call(["sudo","amixer","set", "PCM", "--", str(volume)+'%'])
		muted = False
	else:
		call(["sudo","amixer","set", "PCM", "--", str(0)+'%'])
		muted = True
		print "Mute"

""""GPIO.add_event_detect(VOLUME_UP_PIN, GPIO.RISING, callback=volume_up, bouncetime=300)
GPIO.add_event_detect(VOLUME_DOWN_PIN, GPIO.RISING, callback=volume_down, bouncetime=300)
GPIO.add_event_detect(VOLUME_MUTE_PIN, GPIO.RISING, callback=volume_mute, bouncetime=300)
GPIO.add_event_detect(MOTOR_MUTE_PIN, GPIO.RISING, callback=motor_mute, bouncetime=300)
 
try:
	print "Waiting for button presses..."
	while(1):
		continue
		#do nothing
except KeyboardInterrupt:
	print "\nClosing!"
	GPIO.cleanup()"""
