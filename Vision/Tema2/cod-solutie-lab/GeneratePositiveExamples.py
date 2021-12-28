import os
import numpy as np
import cv2 as cv

root_path = "..\\simpsons_dataset_bogdan\\"

names  = ["bart", "homer", "lisa", "marge"]

image_names = []
bboxes = []
characters = []
nb_examples = 0


for name in names:
	filename_annotations = root_path + name + "_annotations.txt"
	f = open(filename_annotations)
	for line in f:
		a = line.split(os.sep)[-1]
		b = a.split(" ")
		
		image_name = root_path + name + "_simpson\\" + b[0]
		bbox = [int(b[1]),int(b[2]),int(b[3]),int(b[4])]
		character = b[5][:-1]
		
		image_names.append(image_name)
		bboxes.append(bbox)
		characters.append(character)
		nb_examples = nb_examples + 1

width_hog = 36
height_hog = 36



#compute positive examples using 36 X 36 template
number_roots = 1

for idx, img_name in enumerate(image_names):
	print(idx,img_name)
	img = cv.imread(img_name)
	bbox = bboxes[idx]
	xmin = bbox[0]
	ymin = bbox[1]
	xmax = bbox[2]
	ymax = bbox[3]
	print(xmin,ymin,xmax,ymax)
	face = img[ymin:ymax,xmin:xmax]
	print("original face shape:",face.shape)
	face_warped = cv.resize(face,(height_hog, width_hog))
	print("warped face shape:",face_warped.shape)
	filename = "..\\data\\exemplePozitive\\" + str(idx) + ".jpg"
	cv.imwrite(filename,face_warped)