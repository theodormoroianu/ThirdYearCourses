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



#compute negative examples using 36 X 36 template

for idx, img_name in enumerate(image_names):
	print(idx,img_name)
	img = cv.imread(img_name)
	print("img shape")
	print(img.shape)		
	
	num_rows = img.shape[0]
	num_cols = img.shape[1]

	#genereaza 10 exemple negative fara sa compari cu nimic, iei ferestre la intamplare 36 x 36
	for i in range(10):
		
		x = np.random.randint(low=0, high=num_cols - width_hog)
		y = np.random.randint(low=0, high=num_rows - height_hog)
		
		bbox_curent = [x, y, x + width_hog, y + height_hog]
		
		xmin = bbox_curent[0]
		ymin = bbox_curent[1]
		xmax = bbox_curent[2]
		ymax = bbox_curent[3]	
		negative_example = img[ymin:ymax,xmin:xmax]
		filename = "..\\data\\exempleNegative\\" + str(idx) + "_" + str(i) + ".jpg"
		cv.imwrite(filename,negative_example)		
