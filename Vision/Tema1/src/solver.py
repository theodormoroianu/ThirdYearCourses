from typing import List

from scipy.sparse.construct import rand
import src.process_sudoku as ps
import os
import cv2 as cv
import numpy as np
import src.unit_square_extractor as use
import src.square_extractor as se
import src.ocr as ocr
import random
from src.constants import INPUT_PATH, OUTPUT_PATH, CLASIC, JIGSAW


def print_clasic(test_name: str, digits: List[List[int]]):
    with open(OUTPUT_PATH + CLASIC + test_name + "_predicted.txt", "w") as fout:
        for i in range(9):
            fout.write(''.join(['o' if digits[i][j] == 0 else 'x' for j in range(9)]))
            if i != 8:
                fout.write('\n')
    with open(OUTPUT_PATH + CLASIC + test_name + "_bonus_predicted.txt", "w") as fout:
        for i in range(9):
            fout.write(''.join(['o' if digits[i][j] == 0 else str(digits[i][j]) for j in range(9)]))
            if i != 8:
                fout.write('\n')
    
def print_jigsaw(test_name: str, digits: List[List[int]], colors: List[List[int]]):
    with open(OUTPUT_PATH + JIGSAW + test_name + "_predicted.txt", "w") as fout:
        for i in range(9):
            fout.write(
                ''.join(
                    [str(colors[i][j]) + ('o' if digits[i][j] == 0 else 'x') for j in range(9)]
                )
            )
            if i != 8:
                fout.write('\n')
    with open(OUTPUT_PATH + JIGSAW + test_name + "_bonus_predicted.txt", "w") as fout:
        for i in range(9):
            fout.write(
                ''.join(
                    [str(colors[i][j]) + ('o' if digits[i][j] == 0 else str(digits[i][j])) for j in range(9)]
                )
            )
            if i != 8:
                fout.write('\n')
    

def solve():
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    if not os.path.exists(OUTPUT_PATH + CLASIC):
        os.makedirs(OUTPUT_PATH + CLASIC)
    if not os.path.exists(OUTPUT_PATH + JIGSAW):
        os.makedirs(OUTPUT_PATH + JIGSAW)
    
    # Clasic
    for im_name in os.listdir(INPUT_PATH + CLASIC):
        if im_name[-3:] != "jpg":
            continue
        t_img = cv.imread(INPUT_PATH + CLASIC + im_name)
        preds = ps.process_classic(t_img)

        print_clasic(im_name[:2], preds)
        print(f"Processed classic image {im_name}")

    # Jigsaw
    for im_name in os.listdir(INPUT_PATH + JIGSAW):
        if im_name[-3:] != "jpg":
            continue
        t_img = cv.imread(INPUT_PATH + JIGSAW + im_name)
        preds, divs = ps.process_jigsaw(t_img)

        print_jigsaw(im_name[:2], preds, divs)
        print(f"Processed jigsaw image {im_name}")

