import RPi.GPIO as GPIO
import time

#Constants
PWM1 = 16 
PWM2 = 13

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(PWM1, GPIO.OUT)
	GPIO.setup(PWM2, GPIO.OUT)
	
	motor1 = GPIO.PWM(PWM1, 70)
	motor1.start(0)
	return motor1

if __name__ == '__main__':
	motor1 = setup()
	time.sleep(3)
	motor1.ChangeDutyCycle(70.5) #HEHEHE, JARED WAS HERE!!! 
	# time.sleep(3)
	try:
		while 1:
			'''for dc in xrange(0,100,5):
				print dc
				motor1.ChangeDutyCycle(dc)
				time.sleep(4)
			for dc in xrange(100, -1, -5):
				print dc		
				motor1.ChangeDutyCycle(dc)
				time.sleep(4 )'''
			motor1.ChangeDutyCycle(35)
			time.sleep(2)
			motor1.ChangeDutyCycle(90)
			time.sleep(2)
	except KeyboardInterrupt:
		pass
	motor1.stop()
	GPIO.cleanup()
