import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import sources.constants as constants
import sources.sliding_window as sliding_window
import os
import random
import sources.project_utils as project_utils


def read_images(folder_path):
    # (filename, image)
    images = []
    
    # read all images from folder
    for filename in os.listdir(folder_path):
        img = plt.imread(folder_path + filename)
        images.append(img)

    return images

def vizualize(input_path):
    """
    prints ground truth and predictions
    """
    
    imgs = read_images(input_path)

    for im in imgs:
        preds = sliding_window.find_faces(im)

        for b_box, prob in preds[-1]:
            if prob > 0.95:
                cv.rectangle(im, (b_box[0][0], b_box[0][1]), (b_box[1][0], b_box[1][1]), (255, 0, 0), thickness=3)
            
        plt.imshow(im)
        plt.show()

