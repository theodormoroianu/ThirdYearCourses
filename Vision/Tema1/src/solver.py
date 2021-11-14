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

INPUT_PATH = "antrenare/" # "evaluare/fake_test/"
OUTPUT_PATH = "evaluare/fisiere_solutie/Theodor_Moroianu/"
CLASIC = "clasic/"
JIGSAW = "jigsaw/"
TRAIN_DATA = "data/"

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


def generate_train_data():
    """
        Extracts numbers from cells and places them into the TRAIN_DATA folder
    """
    if not os.path.exists(TRAIN_DATA):
        os.makedirs(TRAIN_DATA)
    
    for i in range(10):
        if not os.path.exists(TRAIN_DATA + str(i) + "/"):
            os.makedirs(TRAIN_DATA + str(i) + "/")
    
    def get_classic_label(im_name):
        with open(INPUT_PATH + CLASIC + im_name[:-4] + "_bonus_gt.txt", 'r') as fin:
            d = fin.read().split()
            d = [[int(i) if i != 'o' else 0 for i in v] for v in d]
            return d

    def get_jigsaw_label(im_name):
        with open(INPUT_PATH + JIGSAW + im_name[:-4] + "_bonus_gt.txt", 'r') as fin:
            d = fin.read().split()
            d = [[d[i][2 * j + 1] for j in range(9)] for i in range(9)]
            d = [[int(i) if i != 'o' else 0 for i in v] for v in d]
            return d

    cnt = 0

    def save_img(img: np.ndarray, label):
        nonlocal cnt
        cv.imwrite(TRAIN_DATA + str(label) + "/" + str(cnt) + ".jpg", img)
        cnt += 1

    def augment(img: np.ndarray) -> List[np.ndarray]:
        ans = [img]

        a = img.copy()
        a *= 0
        a[3:, 4:] = img[:-3, :-4]
        ans.append(a)

        b = img.copy()

        for _ in range(10):
            x = random.randint(0, a.shape[0] - 1)
            y = random.randint(0, a.shape[0] - 1)
            b[x][y] = 255 * random.randint(0, 1)

        ans.append(b)

        c = img.copy()

        return ans



    def process_img(img: np.ndarray, labels):
        square = se.extract_square_from_image(img)
        small_sq = use.extract_unit_squares(square)

        for i in range(9):
            for j in range(9):
                for au in augment(ocr.preprocess_digit(small_sq[i][j])):
                    save_img(au, labels[i][j])

    # Clasic
    for im_name in os.listdir(INPUT_PATH + CLASIC):
        if im_name[-3:] != "jpg":
            continue
        if int(im_name[0]) >= 1 and (int(im_name[1]) > 5 or int(im_name[0]) == 2):
            continue

        t_img = cv.imread(INPUT_PATH + CLASIC + im_name)
        labels = get_classic_label(im_name)
        process_img(t_img, labels)

        print(f"Processed classic image {im_name}")

    # Jigsaw
    for im_name in os.listdir(INPUT_PATH + JIGSAW):
        if im_name[-3:] != "jpg":
            continue
        if int(im_name[0]) >= 3:
            continue
        t_img = cv.imread(INPUT_PATH + JIGSAW + im_name)
        labels = get_jigsaw_label(im_name)
        process_img(t_img, labels)

        print(f"Processed jigsaw image {im_name}")
        