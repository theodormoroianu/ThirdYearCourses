"""
Goes through a sliding window to check each pixel independently.

TODO:
 * Decide when a PIXEL is viable to being part of a guy's face.
 * Do partial sums on those pixels.
 * Find a criteria to ignore windows with not enough yellow pixels.
"""

from typing import List, Tuple
import numpy as np
import sources.network as network
import sources.constants as constants
import cv2 as cv
import matplotlib.pyplot as plt

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