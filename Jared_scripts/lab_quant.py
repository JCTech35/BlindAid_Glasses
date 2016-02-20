# import the necessary packages
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import argparse
import cv2
from itertools import groupby
from collections import namedtuple

x = 0

fo = open("quantimage.txt", "w")

def labquant(image, n_clusters):
	global x
	(h, w) = image.shape[:2]
	 
	# convert the image from the RGB color space to the L*a*b*
	# color space -- since we will be clustering using k-means
	# which is based on the euclidean distance, we'll use the
	# L*a*b* color space where the euclidean distance implies
	# perceptual meaning
	image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
	 
	# reshape the image into a feature vector so that k-means
	# can be applied
	image = image.reshape((image.shape[0] * image.shape[1], 3))
	 
	# apply k-means using the specified number of clusters andimage = cv2.imread(args		["image"])
	# then create the quantized image based on the predictions
	clt = MiniBatchKMeans(n_clusters)
	labels = clt.fit_predict(image)
	quant = clt.cluster_centers_.astype("uint8")[labels]
	 
	#print(type(quant))
	#print(type(quant[0][0]))
	'''if x != 1:
		print(quant)
		#print(max(groupby(sorted(quant)), key = quant.count)) #doesnt work

		unique,pos = np.unique(quant,return_counts)
		counts = np.bincount(pos)
		maxpos = counts.argmax()

		print(unique[maxpos], counts[maxpos])
		x = 1'''

	# reshape the feature vectors to images
	quant = quant.reshape((h, w, 3))
	#image = image.reshape((h, w, 3))
	 
	# convert from L*a*b* to RGB
	quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
	#image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)

	'''if x != 1:
		#print(quant)
		#print(max(groupby(sorted(quant)), key = quant.count)) #doesnt work
		for pix in quant:
				pix = str(pix)
				print(pix)
		unique,pos = np.unique(quant,return_inverse = True)
		counts = np.bincount(pos)
		maxpos = counts.argmax()
		print(unique[maxpos], counts[maxpos])
		x = 1'''

	'''counter = {}
	for pix in quant:
		pix = str(pix)
		fo.write(pix + "\n")
		try:
			counter[pix] += 1
			maxpix = pix
			maxcount = int(counter[pix])
		except KeyError:
			counter[pix] = 1

	fo.close()'''

	maxcount= 0
	maxcolor = ""
	counter = {}
	#print(quant[0][0])
	for row in quant:
		for pix in row:
			strpix = str(pix)
			#print "new: " 
			#fo.write(pix + "\n")
			try:
				counter[strpix] +=1
			except:
				counter[strpix] = 1
			if int(counter[strpix]) > maxcount:
				maxcolor = pix
				maxcount = int(counter[strpix])

	#fo.close()

	#print "Maxcolor is: "
	#print maxcolor#<-------IT IS IN BGR NOT RGB! WTF!!!
	print maxcolor, maxcount

	# display the images and wait for a keypress
	#cv2.imshow("image", np.hstack([image, quant]))
	#return np.hstack([image, quant])
	return quant, maxcolor
