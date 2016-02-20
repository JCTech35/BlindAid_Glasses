#imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from lab_quant import labquant

#Resolution
#resWidth = 640
#resHeight = 480
resWidth = 640
resHeight = 480
#Initialize camera and grab raw camera data
camera = PiCamera()
#camera.resolution = (640, 480)
camera.resolution = (resWidth,resHeight)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(resWidth,resHeight))

#allow time for camera to initialize
time.sleep(0.1)

#capture the frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
	#grab raw NumPy array representing the image & initialize timestamp
	image = frame.array
	
	#ROI
	#----------cv2.rectangle(image, (x,y), (x+w,y+h), color,thickness,
	#			line thickness, shift)
	#roiImage = cv2.rectangle(image, (224,144), (64,64),10,5)

	#Apply Median Filter
	image = cv2.medianBlur(image,7) #mask size of 7

	#Crop
	#crop_img = image[208:272, 288:352:] # Crop from x, y, w, h -> 100, 200, 300,400 #crop 64x64 at center
	crop_img = image[208:272, 288:352:] 

	#Color Quantize (segment)
	quantcrop_img = labquant(crop_img,8)

	#show the frame
	#cv2.imshow("Camera Feed",image)
	#cv2.imshow("Crop", crop_img)
	cv2.imshow("Quantized Crop", quantcrop_img)
	#cv2.imshow("Frame",image)
	key = cv2.waitKey(1) & 0xFF

	#clear the stream for the next frame
	rawCapture.truncate(0)
	
	#if 'q' is pressed, quit
	if key== ord("q"):
		break

