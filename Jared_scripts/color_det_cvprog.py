
'''	This is my ECE438 final project C++ program implented in
	python with the OpenCV2 libraries and numpy used in place 
	of the CVIPlab functions. 
'''
#libs
from picamera.array import PiRGBArray
from picamera import PiCamera
from collections import namedtuple
import time
import cv2

#my libs
from lab_quant import labquant

#See namedtuple below
'''class Spectrum():
	def __init__(self, name, color[9], freq):
		self.name = name
		self.color = color
		self.freq = freq'''
#Above class can also be written: 
Spectrum = namedtuple("Spectrum", "name color freq")

#Color struct/tuple to store r,g,b values
Color = namedtuple("Color", "r g b")

#Resolution
resWidth = 640
resHeight = 480
#Initialize camera and grab raw camera data
camera = PiCamera()
camera.resolution = (resWidth,resHeight)
camera.framerate = 2
rawCapture = PiRGBArray(camera, size=(resWidth,resHeight))
#allow time for camera to initialize
time.sleep(0.1)

#shades
whiteshades = [
	Color(224 , 224 , 224), 
	Color(224 , 224 , 224),
	Color(224 , 224 , 224),
	Color(224 , 224 , 224),
	Color(224 , 224 , 224),
	Color(224 , 224 , 224),
	Color(224 , 224 , 224),
	Color(224 , 224 , 224),
	Color(255 , 255 , 255)]
pinkshades = [
	Color(51 , 0 , 51),
	Color(102 , 0 , 102),
	Color(153 , 0 , 153),
	Color(204 , 0 , 204),
	Color(255 , 0 , 255),
	Color(255 , 51 , 255),
	Color(255 , 102 , 255),
	Color(255 , 153 , 255),
	Color(255 , 204 , 255)]
magentashades = [
	Color(51 , 0 , 25),
	Color(102 , 0 , 51),
	Color(153 , 0 , 76),
	Color(204 , 0 , 102),
	Color(255 , 0 , 127),
	Color(255 , 51 , 153),
	Color(255 , 102 , 178),
	Color(255 , 153 , 204),
	Color(255 , 204 , 229)]
redshades = [
	Color(51 , 0 , 0),
	Color(102 , 0 , 0),
	Color(153 , 0 , 0),
	Color(204 , 0 , 0),
	Color(255 , 0 , 0),
	Color(255 , 51 , 51),
	Color(255 , 102 , 102),
	Color(255 , 153 , 153),
	Color(255 , 204 , 204)]
orangeshades = [
	Color(51 , 25 , 0),
	Color(102 , 51 , 0),
	Color(153 , 76 , 0),
	Color(204 , 102 , 0),
	Color(255 , 128 , 0),
	Color(255 , 153 , 51),
	Color(255 , 178 , 102),
	Color(255 , 204 , 153),
	Color(255 , 229 , 204)]
yellowshades = [
	Color(51 , 51 , 0),
	Color(102 , 102 , 0),
	Color(153 , 153 , 0),
	Color(204 , 204 , 0),
	Color(255 , 255 , 0),
	Color(255 , 255 , 51),
	Color(255 , 255 , 102),
	Color(255 , 255 , 153),
	Color(255 , 255 , 204)]
limeshades = [
	Color(25 , 51 , 0),
	Color(51 , 102 , 0),
	Color(76 , 153 , 0),
	Color(102 , 204 , 0),
	Color(128 , 255 , 0),
	Color(153 , 255 , 51),
	Color(178 , 255 , 102),
	Color(204 , 255 , 153),
	Color(229 , 255 , 204)]
greenshades = [
	Color(0 , 51 , 0),
	Color(0 , 102 , 0),
	Color(0 , 153 , 0),
	Color(0 , 204 , 0),
	Color(0 , 255 , 0),
	Color(51 , 255 , 51),
	Color(102 , 255 , 102),
	Color(204 , 255 , 153),
	Color(229 , 255 , 204)]
aquashades = [
	Color(0 , 51 , 25),
	Color(0 , 102 , 51),
	Color(0 , 153 , 76),
	Color(0 , 204 , 102),
	Color(0 , 255 , 128),
	Color(51 , 255 , 153),
	Color(102 , 255 , 178),
	Color(153 , 255 , 204),
	Color(204 , 255 , 229)]
lightblueshades = [
	Color(0 , 51 , 51),
	Color(0 , 102 , 102),
	Color(0 , 153 , 153),
	Color(0 , 204 , 204),
	Color(0 , 255 , 255),
	Color(51 , 255 , 255),
	Color(102 , 255 , 255),
	Color(153 , 255 , 255),
	Color(204 , 255 , 255)]
blueshades = [
	Color(0 , 25 , 51),
	Color(0 , 51 , 102),
	Color(0 , 76 , 153),
	Color(0 , 102 , 204),
	Color(0 , 128 , 255),
	Color(51 , 153 , 255),
	Color(102 , 178 , 255),
	Color(153 , 204 , 255),
	Color(204 , 229 , 255)]
deepblueshades = [
	Color(0 , 0 , 51),
	Color(0 , 0 , 102),
	Color(0 , 0 , 153),
	Color(0 , 0 , 204),
	Color(0 , 0 , 255),
	Color(51 , 51 , 255),
	Color(102 , 102 , 255),
	Color(153 , 153 , 255),
	Color(204 , 204 , 255)]
purpleshades = [
	Color(25 , 0 , 51),
	Color(51 , 0 , 102),
	Color(76 , 0 , 153),
	Color(102 , 0 , 204),
	Color(127 , 0 , 255),
	Color(153 , 51 , 255),
	Color(178 , 102 , 255),
	Color(204 , 153 , 255),
	Color(229 , 204 , 255)]
blackshades = [
	Color(0 , 0 , 0),
	Color(0 , 0 , 0),
	Color(0 , 0 , 0),
	Color(0 , 0 , 0),
	Color(0 , 0 , 0),
	Color(0 , 0 , 0),
	Color(0 , 0 , 0),
	Color(0 , 0 , 0),
	Color(32 , 32 , 32)]


'''
white = Spectrum(name = "white",  color = whiteshades, freq = 1000)
pink = Spectrum(name = "pink", color = pinkshades, freq = 946)
magenta = Spectrum("magenta", magentashades, 892)
red = Spectrum("red", redshades, 838)
orange = Spectrum("orange", orangeshades, 785)
yellow = Spectrum("yellow", yellowshades, 731)
lime = Spectrum("lime", limeshades, 677)
green = Spectrum("green", greenshades, 623)
aqua = Spectrum("aqua", aquashades, 569)
lightblue = Spectrum("lightblue", lightblueshades, 515)
blue = Spectrum("blue", blueshades, 462)
deepblue = Spectrum("deepblue", deepblueshades, 408)
purple = Spectrum(name = "purple", color = purpleshades, freq = 354)
black = Spectrum("black", blackshades, 300)'''

colorspectrum = [Spectrum(name = "white",  color = whiteshades, freq = 1000), 
	Spectrum(name = "pink", color = pinkshades, freq = 946),
	Spectrum("magenta", magentashades, 892),
	Spectrum("red", redshades, 838),
	Spectrum("orange", orangeshades, 785),
	Spectrum("yellow", yellowshades, 731),
	Spectrum("lime", limeshades, 677),
	Spectrum("green", greenshades, 623),
	Spectrum("aqua", aquashades, 569),
	Spectrum("lightblue", lightblueshades, 515),
	Spectrum("blue", blueshades, 462),
	Spectrum("deepblue", deepblueshades, 408),
	Spectrum(name = "purple", color = purpleshades, freq = 354),
	Spectrum("black", blackshades, 300)]

#debugging
#print(getattr(white,'color'))
#print("The last shade of purple is:", purple.color[8].r)

#The following for-loop was from the opencv_roi_test.py script
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
	minDiff = 1000
	#grab raw NumPy array representing the image & initialize timestamp
	image = frame.array
	
	#Apply Median Filter
	image = cv2.medianBlur(image,7) #mask size of 7

	#Crop
	#crop_img = image[208:272, 288:352:] # Crop from x, y, w, h -> 100, 200, 	300,400 		#crop 64x64 at center
	crop_img = image[208:272, 288:352:] 

	#Color Quantize (segment) - returns the segmented image and maxcolor
	quantcrop_img,maxcolors = labquant(crop_img,8) 
	
	#Vars for the BGR values of the maxcolor
	#print maxcolors
	maxB =  maxcolors[0]
	maxG = maxcolors[1]
	maxR = maxcolors[2]

	diff = [ ]
	greyDiff = [ ]
	minDiff = 1000
	for i in xrange(0,13):
		diff.append([ ])
		for j in xrange(0,8):
			diff[i].append([ ])
			diff[i][j] = abs(maxR - colorspectrum[i].color[j].r) + abs(maxG - colorspectrum[i].color[j].g) +  abs(maxB - colorspectrum[i].color[j].b)
			#print("diff is: %d", diff[i][j])
			if(diff[i][j] < minDiff):
				minDiff = diff[i][j]
				minDiffIndex = i
				#print("Distance: %d for Color: %d, %d, %d", minDiff, colorspectrum[i].color[j].r, colorspectrum[i].color[j].g, colorspectrum[i].color[j].b)
			elif(diff[i][j] == minDiff):
				print("THEY ARE EQUAL!")

	isgrey = 0
	greyDiff.append(abs(maxR - maxR) + abs(maxG - maxR) + abs(maxB - maxR))
	greyDiff.append(abs(maxR - maxG) + abs(maxG - maxG) + abs(maxB - maxG))
	greyDiff.append(abs(maxR - maxB) + abs(maxG - maxB) + abs(maxB - maxB))

	for g in xrange(0,2):
		print("\nGrey Diff Is: %d", greyDiff[g])
		if(greyDiff[g] <= 30) and (greyDiff[g] < minDiff):
			isgrey = 1

	print("Majority Color: ", maxR,maxG, maxB)

	if (isgrey == 0):
		print('The color is: %s which is frequency: %d Hz', colorspectrum[minDiffIndex].name, colorspectrum[minDiffIndex].freq)
	elif(isgrey == 1): 
		print("\nThe color is: grey")

	#show the frame
	#cv2.imshow("Camera Feed",image)
	#cv2.imshow("Crop", crop_img)
	#key = cv2.waitKey(1) & 0xFF

	#clear the stream for the next frame
	rawCapture.truncate(0)
	
	#if 'q' is pressed, quit
	#if key== ord("q"):
		#break
