from typing import List, Tuple
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import src.constants as constants
import src.square_extractor as sq_extractor
import src.unit_square_extractor as u_sq_extractor
import src.ocr as ocr
import src.union_find as uf

def process_classic(image: np.ndarray) -> List[List[int]]:
    """
        Processes a sudoku.
        Returns the digits of each cell, 0 if none
    """
    square = sq_extractor.extract_square_from_image(image)

    if constants.DEBUG:
        constants.show_image("sample", square)

    small_sq = u_sq_extractor.extract_unit_squares(square)

    digits = [[ocr.recognize_digit(small_sq[i][j]) for j in range(9)] for i in range(9)]

    if constants.DEBUG:
        print(np.array(digits))

    return digits

def process_jigsaw(image: np.ndarray) -> Tuple[List[List[int]], List[List[int]]]:
    """
        Processes a sudoku.
        Returns:
            * digits of each cell, 0 if none
            * The coloring of the cell (1-9)
    """
    square = sq_extractor.extract_square_from_image(image)

    if constants.DEBUG:
        constants.show_image("sample", square)

    small_sq = u_sq_extractor.extract_unit_squares(square)

    digits = [[ocr.recognize_digit(small_sq[i][j]) for j in range(9)] for i in range(9)]

    if constants.DEBUG:
        print(np.array(digits))
        
    l = u_sq_extractor.adjancy_by_edge_strength(square)

    unionfind = uf.UnionFind()

    for (x1, y1), (x2, y2) in l:
        id1 = unionfind.to_id(x1, y1)
        id2 = unionfind.to_id(x2, y2)

        unionfind.join(id1, id2)

    rez = unionfind.compute_classes()

    return digits, rez

