"""
Takes data from the "antrenare" folder and breaks it down into faces.
"""

import os
from typing import List, Tuple
import matplotlib.pyplot as plt
from scipy.sparse import data
import sources.constants as constants
import numpy as np
import cv2 as cv
from collections import defaultdict
from tqdm import tqdm
import shutil
import sources.project_utils as project_utils
import random

# squares taken by faces in each image. The string of the image
# is given in full path.
_image_path_rectangles = defaultdict(lambda: [])

def _extract_face_subimage(imgpath: str, xmin, ymin, xmax, ymax, name: str) -> np.ndarray:
    """
    name is none if we are processing an empty patch
    """
    
    img = plt.imread(imgpath)
    dx = xmax - xmin
    dy = ymax - ymin

    # im2 = img.copy()
    # cv.rectangle(im2, (xmin, ymin), (xmax, ymax), color=(255, 0, 0), thickness=3)
    # plt.imshow(im2)
    # plt.show()

    if name is not None:
        constants.face_heigth_width_ratio[name].append(dx / dy)

    Y_MAX, X_MAX, _ = img.shape

    c = False
    nr_pasi_nemodif = 0
    while dx != dy:
        c = not c
        if dx < dy and xmin > 0 and c:
            xmin -= 1
            nr_pasi_nemodif = 0
        elif dx < dy and xmax + 1 < X_MAX and not c:
            xmax += 1
            nr_pasi_nemodif = 0
        elif dy < dx and ymin > 0 and c:
            ymin -= 1
            nr_pasi_nemodif = 0
        elif dy < dx and ymax + 1 < Y_MAX and not c:
            ymax += 1
            nr_pasi_nemodif = 0
        else:
            nr_pasi_nemodif += 1
        
        # take care of rectangles too wide. Make ends shorter
        if nr_pasi_nemodif > 2:
            if constants.DEBUG:
                print("Found rectangle too big to turn into square!")
            if dx < dy:
                if c:
                    ymin += 1
                else:
                    ymax -= 1
            else:
                if c:
                    xmin += 1
                else:
                    xmax -= 1

        dx = xmax - xmin
        dy = ymax - ymin
    
    face = img[ymin:ymax+1, xmin:xmax+1, :]

    return cv.resize(
        face,
        dsize=(constants.SIZE_FACE_MODEL, constants.SIZE_FACE_MODEL)
    )

def _save_dataset(dataset: List[List[np.ndarray]]):
    if os.path.exists("network_dataset"):
        shutil.rmtree("network_dataset")

    os.makedirs("network_dataset")


    for id, images in enumerate(tqdm(dataset)):
        images = np.unique(np.stack(images), axis=0)
        os.makedirs("network_dataset/" + str(id))
        for nr, img in enumerate(images):
            plt.imsave(f"network_dataset/{str(id)}/im_{str(nr)}.jpg", img)

def _generate_negative_samples() -> List[np.ndarray]:
    """
    Generates images NOT containing a face.
    _image_path_rectangles needs to be populated for this
    function to work properly
    """
    negative_samples = []

    # loop over all the saved images
    print("Generating negative samples...", flush=True)
    for image_path in tqdm(_image_path_rectangles):
        rectangles = _image_path_rectangles[image_path]
        
        # load image to get the shape
        img = plt.imread(image_path)
        Y_MAX, X_MAX, _ = img.shape

        # generate NR_NEGATIVE_SAMPLES_PER_IMAGE negative samples
        # from that image, which have a reunion over intersection
        # with any rectangle smaller than MAXIMAL_INTERSECTION_OVER_REUNION_NEGATIVE_SAMPLE
        nr_samples_retrieved = 0
        while nr_samples_retrieved < constants.NR_NEGATIVE_SAMPLES_PER_IMAGE:
            dim_sample = random.randint(constants.MINIMAL_WINDOWS_PIXEL_SIZE, min(X_MAX, Y_MAX))
            xmin = random.randint(0, X_MAX - dim_sample)
            ymin = random.randint(0, Y_MAX - dim_sample)
            xmax = xmin + dim_sample - 1
            ymax = ymin + dim_sample - 1

            # check intersection over reunion with the rectangles
            ok = True
            for rect in rectangles:
                inter_over_reun = project_utils.intersection_over_reunion(
                    rect,
                    ((xmin, ymin), (xmax, ymax))
                )
                ok &= inter_over_reun <= constants.MAXIMAL_INTERSECTION_OVER_REUNION_NEGATIVE_SAMPLE
            
            # can consider sample, add it to our list
            if ok:
                nr_samples_retrieved += 1
                sample = img[ymin:ymax+1, xmin:xmax+1, :]
                sample = cv.resize(sample, (constants.SIZE_FACE_MODEL, constants.SIZE_FACE_MODEL))
                negative_samples.append(sample)

    return negative_samples

def generate_dataset() -> List[np.ndarray]:
    """
    Generates a dataset in the "data" folder
    
    @returns a list of the dataset
    """
    global _image_path_rectangles

    dataset = [[] for _ in constants.SIM_LABEL_ORDER]

    print("Loading dataset...")

    # generate samples for each guy and the random class
    for id, name in enumerate(constants.SIM_NAMES):
        print(f"Processing {id+1}/{len(constants.SIM_NAMES)} - {name}", flush=True)
        images = open("antrenare/" + name + ".txt", "r").read().splitlines()

        for line in tqdm(images):
            filename, xmin, ymin, xmax, ymax, face_name = line.split()
            xmin = int(xmin)
            xmax = int(xmax)
            ymin = int(ymin)
            ymax = int(ymax)
            filename = "antrenare/" + name + "/" + filename

            dx = xmax - xmin
            dy = ymax - ymin

            if (dx < dy and dx / dy < 0.5) or (dy < dx and dy / dx < 0.5):
                continue

            face_subimage = _extract_face_subimage(filename, xmin, ymin, xmax, ymax, name)
            dataset[constants.SIM_LABEL_ORDER[face_name]].append(face_subimage)
            _image_path_rectangles[filename].append(((xmin, ymin), (xmax, ymax)))

    # generate negative samples
    assert(len(dataset[-1]) == 0)
    dataset[-1] = _generate_negative_samples()

    print("Saving dataset...")
    _save_dataset(dataset)

    dataset = [np.stack(i) if len(i) != 0 else [] for i in dataset]

    _image_path_rectangles = defaultdict(lambda: [])
    return dataset

def _data_augment(img):
    return [img, img[:, ::-1, :]]

def load_dataset() -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns the data in a standard format: Images on X, labels on Y 
    """
    x = []
    y = []

    def add_img(type, filename):
        im = plt.imread(filename)
        if im.shape[0] != constants.SIZE_FACE_MODEL:
            im = cv.resize(im, (constants.SIZE_FACE_MODEL, constants.SIZE_FACE_MODEL))
        
        images = _data_augment(im)
        for img in images:
            x.append(np.array(img))
            y.append(type)

    for type in tqdm(range(6)):
        for filename in os.listdir("network_dataset/" + str(type) + "/"):
            add_img(type, "network_dataset/" + str(type) + "/" + filename)

        for filename in os.listdir("outsider_dataset/" + str(type) + "/"):
            add_img(type, "outsider_dataset/" + str(type) + "/" + filename)

    x = np.stack(x)
    y = np.array(y)

    print("Finished loading dataset...")
    return x, y
