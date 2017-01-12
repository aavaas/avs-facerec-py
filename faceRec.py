import os
import sys
import cv2
import numpy as np
import urllib2

persons ={0 : "aavaas", 1: "aavaas"}

def detect(img, cascade):
	rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(100, 100), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
	if len(rects) == 0:
		return []
	rects[:,2:] += rects[:,:2]
	return rects
	

def draw_rects(img, rects, color):
	for x1, y1, x2, y2 in rects:
		cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
		break
	

def read_images(path, sz=None):
	"""Reads the images in a given folder, resizes images on the fly if size is given.
	sz: A tuple with the size Resizes

	Returns:
		A list [X,y]
			X: The images, which is a Python list of numpy arrays.
			y: The corresponding labels (the unique number of the subject, person) in a Python list.
	"""
	c = 0
	X,y = [], []
	for dirname, dirnames, filenames in os.walk(path):
		for subdirname in dirnames:
			subject_path = os.path.join(dirname, subdirname)
			for filename in os.listdir(subject_path):
				try:
					im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
					# resize to given size (if given)
					if (sz is not None):
						im = cv2.resize(im, sz)
					X.append(np.asarray(im, dtype=np.uint8))
					y.append(c)
				except IOError, (errno, strerror):
					print "I/O error({0}): {1}".format(errno, strerror)
				except:
					print "Unexpected error:", sys.exc_info()[0]
					raise
			c = c+1
	return [X,y]

	
if __name__ == "__main__":    
	# Now read in the image data.
	[X,y] = read_images("trainingfaces")	
	# Convert labels to 32bit integers
	# because the labels will truncated else in 64bit machines,
	y = np.asarray(y, dtype=np.int32)
	# Create the Eigenfaces model. We are going to use the default
	model = cv2.createEigenFaceRecognizer()	
	# Learn the model. Remember our function returns Python lists,
	# so we use np.asarray to turn them into NumPy lists to make
	# the OpenCV wrapper happy:
	model.train(np.asarray(X), np.asarray(y))

	##-------------------------------------------
	
	
	video_src = 0
	cascade_fn = "Haar/haarcascade_frontalface_alt.xml"    

	cascade = cv2.CascadeClassifier(cascade_fn)

	cam = cv2.VideoCapture(0)
	
	iflag = 0
	intrucnt = 0
	while True:
		ret, img = cam.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#gray = cv2.equalizeHist(gray)
		gray = cv2.GaussianBlur(gray,(7,7),0)
		
		rects = detect(gray, cascade)
		#display
		draw_rects(gray, rects, (0, 255, 0)) 
		cv2.imshow("main", gray)
		
		#if face found
		if len(rects) != 0:			
			for x1, y1, x2, y2 in rects:
				roi = gray[y1:y2, x1:x2]
				break
			cv2.imshow('face',roi)
			
			# predicted label and the associated distance:
			roi = cv2.equalizeHist(roi)
			roi =cv2.resize(roi, (92,112))
			[p_label, p_distance] = model.predict(np.asarray(roi, dtype=np.uint8))
			# Print it:
			print "Predicted label = %d (distance=%.2f)" % (p_label, p_distance)
			
			if p_distance < 6000 and p_label<4:
				print "detected" , persons[p_label]
				iflag = 0
				intrucnt =0
			else:
				if iflag == 0:
					intrucnt += 1
					print "intruder mabe", intrucnt
					if intrucnt > 5:
						print "INTRUDER DETECTED"
						#response = urllib2.urlopen("http://192.168.43.151:8001/sync/iset");
						iflag = 1
		
		
		
		
		key = 0xFF & cv2.waitKey(1000)		
		if  key == 27:
			break
	
	cv2.destroyAllWindows()


	##--------------------------------------------
