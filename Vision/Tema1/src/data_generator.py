from typing import List
import numpy as np
import os
from src.constants import TRAIN_INPUT_PATH, CLASIC, JIGSAW, TRAIN_DATA
import random
import cv2 as cv
import src.square_extractor as se
import src.unit_square_extractor as use
import src.ocr as ocr


def augment(img: np.ndarray) -> List[np.ndarray]:
    """
        Performs data augmentation on the image
    """
    ans = [img]

    a = img.copy()
    a *= 0
    dx = random.randint(1, 6)
    dy = random.randint(1, 6)
    
    a[dx:, dy:] = img[:-dx, :-dy]
    ans.append(a)

    b = img.copy()

    for _ in range(10):
        x = random.randint(0, a.shape[0] - 1)
        y = random.randint(0, a.shape[0] - 1)
        b[x][y] = 255 * random.randint(0, 1)

    ans.append(b)

    c = img.copy().astype(np.float32)
    power = random.randint(700, 1300) / 1000
    c[c > 255] = 255
    c = (c * power).astype(np.uint8)
    ans.append(c)

    return ans

def get_classic_label(im_name):
    with open(TRAIN_INPUT_PATH + CLASIC + im_name[:-4] + "_bonus_gt.txt", 'r') as fin:
        d = fin.read().split()
        d = [[int(i) if i != 'o' else 0 for i in v] for v in d]
        return d

def get_jigsaw_label(im_name):
    with open(TRAIN_INPUT_PATH + JIGSAW + im_name[:-4] + "_bonus_gt.txt", 'r') as fin:
        d = fin.read().split()
        d = [[d[i][2 * j + 1] for j in range(9)] for i in range(9)]
        d = [[int(i) if i != 'o' else 0 for i in v] for v in d]
        return d

cnt = 0
def save_img(img: np.ndarray, label):
    global cnt
    cv.imwrite(TRAIN_DATA + str(label) + "/" + str(cnt) + ".jpg", img)
    cnt += 1

def process_img(img: np.ndarray, labels):
    square = se.extract_square_from_image(img)
    small_sq = use.extract_unit_squares(square)

    for i in range(9):
        for j in range(9):
            for au in augment(ocr.preprocess_digit(small_sq[i][j])):
                save_img(au, labels[i][j])

def generate_train_data():
    """
        Extracts numbers from cells and places them into the TRAIN_DATA folder
    """
    if not os.path.exists(TRAIN_DATA):
        os.makedirs(TRAIN_DATA)
    
    for i in range(10):
        if not os.path.exists(TRAIN_DATA + str(i) + "/"):
            os.makedirs(TRAIN_DATA + str(i) + "/")    

    # Clasic
    for im_name in os.listdir(TRAIN_INPUT_PATH + CLASIC):
        if im_name[-3:] != "jpg":
            continue
        if int(im_name[0]) >= 1 and (int(im_name[1]) > 5 or int(im_name[0]) == 2):
            continue

        t_img = cv.imread(TRAIN_INPUT_PATH + CLASIC + im_name)
        labels = get_classic_label(im_name)
        process_img(t_img, labels)

        print(f"Processed classic image {im_name}")

    # Jigsaw
    for im_name in os.listdir(TRAIN_INPUT_PATH + JIGSAW):
        if im_name[-3:] != "jpg":
            continue
        if int(im_name[0]) >= 3:
            continue
        t_img = cv.imread(TRAIN_INPUT_PATH + JIGSAW + im_name)
        labels = get_jigsaw_label(im_name)
        process_img(t_img, labels)

        print(f"Processed jigsaw image {im_name}")
        