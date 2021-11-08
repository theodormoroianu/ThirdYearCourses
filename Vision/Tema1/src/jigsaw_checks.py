import src.constants as constants
import cv2 as cv
import numpy as np
import src.square_extractor as s_e
import src.unit_square_extractor as u_s
import matplotlib.pyplot as plt

def normalize(im):
    avg = np.mean(im, axis=(0, 1))
    nrm = np.sqrt((avg * avg).sum())

    im /= nrm

def distance(im1, im2):
    avg1 = np.mean(im1, axis=(0, 1))
    avg2 = np.mean(im2, axis=(0, 1))

    mse = (avg1 * avg2).sum()
    return mse

CUT = 0.998

def checker(im):
    sq = s_e.extract_square_from_image(im)

    small_sq = u_s.extract_unit_squares(sq)

    for i in range(9):
        for j in range(9):
            small_sq[i][j] = small_sq[i][j].astype(np.float32)
            normalize(small_sq[i][j])

    color = [[-1 for i in range(9)] for j in range(9)]
    cnt = 0

    for i in range(9):
        for j in range(9):
            if color[i][j] != -1:
                continue
            color[i][j] = cnt

            for k in range(9):
                for l in range(9):
                    dif = distance(small_sq[i][j], small_sq[k][l])
                    if dif > CUT:
                        if color[k][l] != -1 and color[k][l] != cnt:
                            print("NOOPE!!")
                        color[k][l] = cnt
                    # print(f"Distance between ({i}, {j}) and ({k}, {l}) is {dif}")
            cnt += 1

    plt.imshow(color)
    plt.show()