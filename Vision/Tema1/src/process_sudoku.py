from typing import List
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import src.constants as constants
import src.square_extractor as sq_extractor
import src.unit_square_extractor as u_sq_extractor
import src.ocr as ocr

def process_classic(image: np.ndarray) -> List[List[int]]:
    """
        Processes a sudoku.
        Returns the digits of each cell, -1 if none
    """
    square = sq_extractor.extract_square_from_image(image)

    if constants.DEBUG:
        constants.show_image("sample", square)

    small_sq = u_sq_extractor.extract_unit_squares(square)

    digits = [[ocr.recognize_digit(small_sq[i][j]) for j in range(9)] for i in range(9)]

    return digits