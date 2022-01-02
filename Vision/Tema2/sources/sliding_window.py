"""
Goes through a sliding window to check each pixel independently.

TODO:
 * Decide when a PIXEL is viable to being part of a guy's face.
 * Do partial sums on those pixels.
 * Find a criteria to ignore windows with not enough yellow pixels.
"""

from typing import List, Tuple
import numpy as np
import sources.network_pytorch as network
import sources.constants as constants
import cv2 as cv
import matplotlib.pyplot as plt
import sources.project_utils as project_utils

def find_best_sliding_window_face(image: np.ndarray, type: int):
    
    matchy_windows: List[Tuple[float, Tuple[Tuple[int, int], Tuple[int, int]]]] = []

    window_dim = min(image.shape[0], image.shape[1])

    while window_dim >= constants.MINIMAL_WINDOWS_PIXEL_SIZE:
        stride = int(window_dim * constants.SLIDING_WINDOW_STRIDE)

        bart_max = 0.

        for ymin in range(0, image.shape[0] - window_dim + 1, stride):
            for xmin in range(0, image.shape[1] - window_dim + 1, stride):
                sliding_window = image[ymin:ymin+window_dim, xmin:xmin+window_dim, :]
                labels = network.recognize_image(sliding_window)
                
                bart_max = max(bart_max, labels[0][0].item())

                matchy_windows.append((
                    -labels[0][type].item(),
                    ((xmin, ymin), (xmin+window_dim-1, ymin+window_dim-1))
                ))

        print("max bart:", bart_max)
        # rescale sliding window
        print("Scale:", window_dim)
        window_dim = window_dim * constants.SLIDING_WINDOW_RESCALE_FACTOR
        window_dim = int(window_dim)

    matchy_windows.sort()

    for i in range(10):

        print("Best match: ", matchy_windows[i][0])

        ((xmin, ymin), (xmax, ymax)) = matchy_windows[i][1]
        img = image.copy()
        cv.rectangle(img, (xmin, ymin), (xmax, ymax), color=(255, 255, 255))

        plt.imshow(img)
        plt.show()


def find_faces(img: np.ndarray) -> List[List[Tuple[Tuple, float]]]:
    """
    Returns the detected faces from the image.
    The top-level list is:
        0-4 -> the 4 guys and unknown
        5 -> any face

    """
    
    windows: List[List[Tuple[Tuple, float]]] = [[] for _ in range(6)]

    def process_window(xmin, ymin, xmax, ymax, probs):
        nonlocal windows
        for type in range(5):
            windows[type].append((
                ((xmin, ymin), (xmax, ymax)),
                probs[type]
            ))
        windows[5].append((
            ((xmin, ymin), (xmax, ymax)),
            1. - probs[5]
        ))


    window_dim = min(img.shape[0], img.shape[1])

    while window_dim >= constants.MINIMAL_WINDOWS_PIXEL_SIZE:
        stride = int(window_dim * constants.SLIDING_WINDOW_STRIDE)

        for ymin in range(0, img.shape[0] - window_dim + 1, stride):
            for xmin in range(0, img.shape[1] - window_dim + 1, stride):
                sliding_window = img[ymin:ymin+window_dim, xmin:xmin+window_dim, :]
                labels = network.recognize_image(sliding_window)[0]
                
                process_window(xmin, ymin, xmin+window_dim-1, ymin+window_dim-1, labels)

        window_dim = window_dim * constants.SLIDING_WINDOW_RESCALE_FACTOR
        window_dim = int(window_dim)

    windows = [project_utils.non_max_suppression(wind) for wind in windows]
    
    return windows