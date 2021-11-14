"""
    Extracts unit squares from a given table
"""

from typing import List, Tuple
import numpy as np
import src.constants as constants
import matplotlib.pyplot as plt
import src.square_extractor as s_e
import cv2 as cv

def extract_edges(square: np.ndarray) -> Tuple[List[List[np.ndarray]], List[List[np.ndarray]]]:
    """
        Computes edges between small squares of a big square.
        Returns (9x8 orizontal edges, 8x9 vertical edges)
    """

    square = s_e._make_wb(square)
    square = 255 - square   
    kernel = np.ones((10, 10))
    square = cv.erode(square, kernel)
    
    if constants.DEBUG:
        plt.imshow(square)
        plt.show()

    D = square.shape[0] // 9
    OFFSET = D // 3
    WIDTH = D // 5

    oriz = [[None for i in range(8)] for j in range(9)]
    vert = [[None for i in range(9)] for j in range(8)]

    for i in range(9):
        for j in range(9):
            if j != 8:
                oriz[i][j] = square[D*i+OFFSET : D*(i+1)-OFFSET, D*(j+1)-WIDTH : D*(j+1)+WIDTH]
            if i != 8:
                vert[i][j] = square[D*(i+1)-WIDTH : D*(i+1)+WIDTH, D*j+OFFSET : D*(j+1)-OFFSET]
            
    return oriz, vert

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

def adjancy_by_edge_strength(square: np.ndarray) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
        Gets a square, and returns the adjancy sorted by the edges (small edges first)
    """

    oriz, vert = extract_edges(square)

    lst = []
    for i in range(9):
        for j in range(9):
            if i != 8:
                lst.append(((i, j), (i + 1, j)))
            if j != 8:
                lst.append(((i, j), (i, j + 1)))

    def power(p):
        (x1, y1), (x2, y2) = p
        if x1 == x2:
            return oriz[x1][y1].sum()
        else:
            return vert[x1][y1].sum()

    lst = sorted(lst, key=power)

    return lst
