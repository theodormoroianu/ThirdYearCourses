"""
    Extracts unit squares from a given table
"""

from typing import List
import numpy as np
import src.constants as constants
import matplotlib.pyplot as plt

def extract_unit_squares(square: np.ndarray, O: int = constants.OFFSET_MARGIN) -> List[List[np.ndarray]]:
    """
        Extracts 1x1 squares from a big (9x9) one.
        Leaves constants.OFFSET_MARGIN pixels out of each image.
        O reprezents the nr of pixels to remove from the 4 corners
    """

    small_squares = [[None for i in range(9)] for j in range(9)]

    D = constants.SQUARE_DIM // 9

    for i in range(9):
        for j in range(9):
            piece = square[i * D : (i + 1) * D, j * D : (j + 1) * D]
            piece = piece[O : D - O, O : D - O]

            small_squares[i][j] = piece

    if constants.DEBUG:
        fig, axes = plt.subplots(nrows=9, ncols=9)

        for i in range(9):
            for j in range(9):
                axes[i][j].axis('off')
                axes[i][j].imshow(small_squares[i][j])
        plt.show()

    return small_squares