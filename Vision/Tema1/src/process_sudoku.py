import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import src.constants as constants
import src.square_extractor as sq_extractor
import src.unit_square_extractor as u_sq_extractor


def process_sudoku(path: str):
    """
        Processes a sudoku
    """
    img = cv.imread(path)
    square = sq_extractor.extract_square_from_image(img)

    constants.show_image("sample", square)

    small_sq = u_sq_extractor.extract_unit_squares(square)