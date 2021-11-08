"""
    Module extracting a square from a given image.
"""

from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

import src.constants as constants

SQUARE_DIM = constants.SQUARE_DIM

def _apply_preprocessing(img: np.ndarray) -> np.ndarray:
    image = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    image_m_blur = cv.medianBlur(image, 5)
    image_g_blur = cv.GaussianBlur(image_m_blur, (0, 0), 11) 
    image_sharpened = cv.addWeighted(image_m_blur, 2., image_g_blur, -1., 0)
    _, thresh = cv.threshold(image_sharpened, 150, 255, cv.THRESH_BINARY)

    
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv.erode(thresh, kernel)
    
    if constants.DEBUG:
        constants.show_image("median blurred",image_m_blur)
        constants.show_image("gaussian blurred",image_g_blur)
        constants.show_image("sharpened",image_sharpened)    
        constants.show_image("threshold of blur",thresh)
    
    edges =  cv.Canny(thresh ,150,400)
    # gray: np.ndarray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # gray_m_blur = cv.medianBlur(gray, 11)
    # gray_g_blur = cv.GaussianBlur(gray_m_blur, (0, 0), 11) 
    # sharpened = cv.addWeighted(gray_m_blur, 1.2, gray_g_blur, -0.8, 0)

    # final = sharpened

    # # final = sharpened + 255 / 2 - sharpened.mean()
    # # final[final > 255] = 255
    # # final[final < 0] = 0
    # # final = final.astype(np.uint8)

    # if constants.DEBUG:
    #     constants.show_image("Initial image", gray)
    #     constants.show_image("Median blur", gray_m_blur)
    #     constants.show_image("Gaussian Blur blur", gray_g_blur)
    #     constants.show_image("Sharpened", sharpened)
    #     constants.show_image("before threshold", final)

    # #apply threshold
    # threshold = cv.threshold(gray, 60, 255, cv.THRESH_BINARY)[1]

    # if constants.DEBUG:
    #     constants.show_image("after threshold", threshold)
    
    # return threshold
    return edges

def _find_corners(edges: np.ndarray) -> List[List[Tuple[int, int]]]:
    """ Returns the 4 corners of the square from a processed image.
    
    Returns a matrix of 2x2 with the 4 corners.
    """
    contours, _ = cv.findContours(edges,  cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0

    if constants.DEBUG:
        constants.show_image("Edges", edges)
   
   
    for i in range(len(contours)):
        if(len(contours[i]) >3):
            possible_top_left = None
            possible_bottom_right = None
            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point

                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + possible_bottom_right[1] :
                    possible_bottom_right = point

            diff = np.diff(contours[i].squeeze(), axis = 1)
            possible_top_right = contours[i].squeeze()[np.argmin(diff)]
            possible_bottom_left = contours[i].squeeze()[np.argmax(diff)]
            if cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left

    if constants.DEBUG:
        image_copy = cv.cvtColor(edges.copy(),cv.COLOR_GRAY2BGR)
        cv.circle(image_copy,tuple(top_left),4,(0,0,255),-1)
        cv.circle(image_copy,tuple(top_right),4,(0,0,255),-1)
        cv.circle(image_copy,tuple(bottom_left),4,(0,0,255),-1)
        cv.circle(image_copy,tuple(bottom_right),4,(0,0,255),-1)
        constants.show_image("detected corners",image_copy)

    return [
        [top_left, top_right],
        [bottom_left, bottom_right],
    ]

def _4_points_transform(img: np.ndarray, points: List[List[Tuple[int, int]]]) -> np.ndarray:
    tl = points[0][0]
    tr = points[0][1]
    bl = points[1][0]
    br = points[1][1]

    rect = (tl, tr, br, bl)
    rect = [[rect[i][j] for j in [0, 1]] for i in range(4)]
    rect = np.array(rect)
    rect = rect.astype(np.float32)

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    # compute the perspective transform matrix and then apply it
    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(img, M, (maxWidth, maxHeight))
    
    if constants.DEBUG:
        constants.show_image("4-point transform", warped)

    # return the warped image
    return warped

def extract_square_from_image(img: np.ndarray) -> np.ndarray:
    """Extracts the sudoku square from the given image.
    
    What it does:
     * Uses a bunch of filters for enhancing the border of the square.
     * Applying a binary threshold (hopefully) isolating the border of the square.
     * Uses cv.findContour for getting a list of all possible contours
     * Finds the largest contour, and returns it.
    """
    img = cv.resize(img, dsize=(1000, 1000))
    processed = _apply_preprocessing(img)

    corners = _find_corners(processed)

    square = _4_points_transform(img, corners)

    square = cv.resize(square, dsize=(SQUARE_DIM, SQUARE_DIM))

    return square
