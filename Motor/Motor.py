"""
File: Motor.py
Description: Motor class for use in the blind aid glasses project.
Date Created: January 21, 2016
Date Last Edited: January 21, 2016
Author: Cameron Costanzo
"""

import RPi.GPIO as GPIO

#Constants
FREQ = 70 #Hz
MIN_DC = 30 #%
MAX_DC = 90 #%

class Motor(object):
	
	def __init__(self, pin, intensity = 0):
		self.intensity = intensity
		self.pin = pin
		self.motor = self.setup()

	def getIntensity(self):
		return self.intensity

	def getPin(self):
		return self.pin

	def setIntensity(self, intensity):
		self.intensity = intensity

	def setPin(self, pin):
		self.pin = pin		
	
	def changeIntensity(self, intensity):
		if MIN_DC <= intensity <= MAX_DC:
			self.motor.ChangeDutyCycle(intensity)
		else:
			raise ValueError("Motor intensity outside of acceptable bounds.")
			
	def motorMute(self):
		self.motor.ChangeDutyCycle(0)
		GPIO.output(int(self.pin), GPIO.LOW)

	def motorStop(self):
		self.motor.ChangeDutyCycle(0)
		GPIO.output(int(self.pin), GPIO.LOW)
		self.motor.stop()
		GPIO.cleanup(self.getPin())
			
	def setup(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.getPin(), GPIO.OUT)
		motor = GPIO.PWM(self.getPin(), FREQ)
		motor.start(self.getIntensity())
		return motor
