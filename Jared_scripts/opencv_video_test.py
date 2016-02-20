#imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#Initialize camera and grab raw camera data
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(640,480))

#allow time for camera to initialize
time.sleep(0.1)

#capture the frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
	#grab raw NumPy array representing the image & initialize timestamp
	image = frame.array
	
	#show the frame
	cv2.imshow("Frame",image)
	key = cv2.waitKey(1) & 0xFF

	#clear the stream for the next frame
	rawCapture.truncate(0)

	#if 'q' is pressed, quit
	if key== ord("q"):
		break
