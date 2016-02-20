import Motor
import time
try:
	motor2 = Motor.Motor(13)
	motor1 = Motor.Motor(16)
	print "motor1"
	print motor1.intensity, motor1.pin
	while(1):
		print "up"
		for i in xrange(30,90,1):
			motor1.changeIntensity(i)
			motor2.changeIntensity(i)
			time.sleep(.5)
		print "down"
		for i in xrange(90,30,-1):
			motor1.changeIntensity(i)
			motor2.changeIntensity(i)
			time.sleep(.5)
except KeyboardInterrupt:
	motor1.motorStop()
	motor2.motorStop()

