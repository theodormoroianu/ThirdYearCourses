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

# Checks the colors
def colored_checker(im):
    sq = s_e.extract_square_from_image(im)

    small_sq = u_s.extract_unit_squares(sq)


    for i in range(9):
        for j in range(9):
            s = small_sq[i][j].copy()
            s = cv.cvtColor(s,cv.COLOR_BGR2GRAY)
            s = cv.resize(s, dsize=(28, 28))
            _, s = cv.threshold(s, 100, 255, cv.THRESH_BINARY)
            cv.imwrite(f"img{i}{j}.jpg", s)

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

# Checks the colors
def grayscale_check(im):
    sq = s_e.extract_square_from_image(im)

    small_sq = u_s.extract_unit_squares(sq, O=0)

    D = small_sq[0][0].shape[0]
    WHERE = D // 4

    def match_vert(sq1: np.ndarray, sq2: np.ndarray) -> np.float32:
        if constants.DEBUG:
            sq1_copy = sq1.copy()
            sq1_copy[:WHERE, WHERE] *= 0
            sq2_copy = sq2.copy()
            sq2_copy[D-WHERE:, WHERE] *= 0

            constants.show_image("sq1", sq1_copy)
            constants.show_image("sq2", sq2_copy)        

        return sq1[:WHERE, WHERE].sum() + sq2[D-WHERE:, WHERE].sum()

    for i in range(1, 9):
        for j in range(9):
            cost = match_vert(small_sq[i][j], small_sq[i - 1][j])
            print(f"({i-1},{j})-({i},{j}): {cost}")
