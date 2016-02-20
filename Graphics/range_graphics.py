"""
File: haptic_range.py
Description: Basic script that inversely relates distance to haptic feedback.
	Closer the distance the stronger the vibration, farther the distance the
	weaker the vibration.
Date Created: January 26, 2016
Date Last Edited: January 27, 2016
Author: Cameron Costanzo
"""	

import Dependencies.IRSensor as IRS
import Dependencies.Motor as Motor
from graphics import *

#Constants
MAX_INTENSITY = 90
MIN_INTENSITY = 30
MAX_RANGE = 150
MIN_RANGE = 15

def scaleIntensity(range):
	intensity = (((MAX_INTENSITY - MIN_INTENSITY)*(MAX_RANGE - range))/(MAX_RANGE-MIN_RANGE)) + MIN_INTENSITY
	intensity = int(intensity)
	return intensity

if __name__ == '__main__':
	irsensor0 = IRS.IRSensor(0)
	motor0 = Motor.Motor(16)
	win = GraphWin()
	try:
		range = 0
		intensity = 0
		irstart = Point(0, 50)
		while(1):
			range = irsensor0.updateRange()
			range = int(range)
			intensity = scaleIntensity(range)
			if MIN_RANGE <= range <= MAX_RANGE:
				print "Intensity: ",intensity,
				print "Range: ",range
				motor0.changeIntensity(intensity)
				
				irfinish = Point(range,50)
				line = Line(irstart,irfinish)
				line.setFill("red")
				line.draw(win)
				line.undraw()	

			elif range > MAX_RANGE:
				print "Farther than 150 cm"
				motor0.changeIntensity(MAX_INTENSITY)
				irfinish = Point(MAX_RANGE,50)
				line = Line(irstart,irfinish)
				line.setFill("red")
				line.draw(win)
				line.undraw()	

				
			elif range < MIN_RANGE:
				print "Shorter than 15 cm"
				motor0.changeIntensity(MIN_INTENSITY)
		
				irfinish = Point(MIN_RANGE,50)
				line = Line(irstart,irfinish)
				line.setFill("red")
				line.draw(win)
				line.undraw()	




	except KeyboardInterrupt:
		motor0.motorStop()
		print "\nExiting..."

