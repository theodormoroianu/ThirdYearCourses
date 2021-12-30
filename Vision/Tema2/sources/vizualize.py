import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import sources.constants as constants
import sources.sliding_window as sliding_window
import os
import random
import sources.project_utils as project_utils

def vizualize(input_path):
    """
    prints ground truth and predictions
    """
    lines = open(input_path + "simpsons_validare.txt", "r").readlines()

    line = lines[random.randint(0, len(lines) - 1)]
    
    filename, xmin, ymin, xmax, ymax, face_name = line.split()
    xmin = int(xmin)
    xmax = int(xmax)
    ymin = int(ymin)
    ymax = int(ymax)
    
    img = plt.imread(input_path + "simpsons_validare/" + filename)
    predictions = sliding_window.find_faces(img)

    cv.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), thickness=3)
    cv.putText(img, "GT", (xmin, ymin),
                cv.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1)

    first = True
    for b_box, type, prob_type, prob in predictions[:min(10, len(predictions))]:
        if not first:
            print("Probability:", prob)
            if prob < 0.1:
                break
            cv.rectangle(img, (b_box[0][0], b_box[0][1]), (b_box[1][0], b_box[1][1]), (0, 255, 0), thickness=1)
            continue
        first = False
        cv.rectangle(img, (b_box[0][0], b_box[0][1]), (b_box[1][0], b_box[1][1]), (255, 0, 0), thickness=3)
        cv.putText(img, f"Class={type}, p={int(prob_type * 100)}, face={int(prob * 100)}", (b_box[0][0], b_box[0][1]),
                cv.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1)

        print("Intersection Over Reunion:", project_utils.intersection_over_reunion(
            ((xmin, ymin), (xmax, ymax)), b_box
        ))

    plt.imshow(img)
    plt.show()

