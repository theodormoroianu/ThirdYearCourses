"""
    Module with various contants.
"""

import matplotlib.pyplot as plt
import cv2 as cv

def show_image(title, image):
    im = image.copy()
    im = cv.resize(im, dsize=(500, 500))

    plt.imshow(im)
    plt.show()

    return

    cv.imshow(title, im)
    cv.waitKey(0)
    cv.destroyAllWindows()

# whether to show debug info or not
DEBUG = True

# Dimension of intermediate square
SQUARE_DIM = 1008

# Margin to loose on small squares
OFFSET_MARGIN = 15

# Show each digit
DEBUG_DIGITS = False

# Check if answer is ok
CHECK_ANSWER = True


INPUT_PATH = "antrenare/" # "evaluare/fake_test/"
OUTPUT_PATH = "evaluare/fisiere_solutie/Theodor_Moroianu/"
CLASIC = "clasic/"
JIGSAW = "jigsaw/"
TRAIN_DATA = "data/"
TRAIN_INPUT_PATH = "antrenare/"