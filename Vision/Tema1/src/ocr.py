"""
    Module able to recognize digits
"""

import src.constants as constants
import pytesseract as ts
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def recognize_digit(digit: np.ndarray) -> int:
    """
        Initialize the digit recognition
    """

    image = cv.cvtColor(digit, cv.COLOR_BGR2GRAY)
    _, image = cv.threshold(image, 100, 255, cv.THRESH_BINARY)

    # if constants.DEBUG:
    #     constants.show_image("Digit", image)

    predicted = ts.image_to_string(image, config="--psm 10")

    try:
        if len(predicted) < 1:
            raise Exception()
        d = int(predicted[0])
        if d < 0 or d > 9:
            raise Exception()
        return d
    except:
        return -1