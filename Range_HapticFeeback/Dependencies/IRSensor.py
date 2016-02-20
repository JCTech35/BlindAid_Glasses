"""
File: IRSensor.py
Description: IR Sensor class for use in the Blind-Aid glasses project.
Date Created: January 25, 2016
Date Last Edited: January 25, 2016
Author: Cameron Costanzo
"""

import IRSensor_Read as IRS

class IRSensor(object):
	conn = IRS.setup()

	def __init__(self, channel):
		self.range = 0
		self.channel = channel
		
	def getRange(self):
		return self.range
		
	def updateRange(self):
		voltage = 5*IRS.read(self.conn, self.channel, 0)
		self.range = 61.681 * (voltage+0.000001) ** -1.133
		return self.range
		
	def setChannel(self, channel):
		self.channel = channel

	def getChannel(self):
		return self.channel
	
