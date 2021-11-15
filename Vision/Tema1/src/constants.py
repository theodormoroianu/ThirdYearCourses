"""
    Module with various contants.
"""

import cv2 as cv

def show_image(title, image):
    im = image.copy()
    im = cv.resize(im, dsize=(500, 500))

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