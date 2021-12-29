from typing import List, Tuple
import sources.sliding_window as sliding_window
import sources.constants as constants
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def read_images(folder_path) -> List[Tuple[str, np.ndarray]]:
    # (filename, image)
    images = []
    
    # read all images from folder
    for filename in os.listdir(folder_path):
        img = plt.imread(folder_path + filename)
        images.append((filename, img))

    return images

def print_task_1(faces_detected, output_path):
    bounding_boxes = []
    filenames = []
    probabilities = []

    print(faces_detected[0])

    for filename, (box, _, _, prob) in faces_detected:
        # TODO: Check the bounding box format
        filenames.append(filename)
        probabilities.append(prob)
        bounding_boxes.append([box[0][0], box[0][1], box[1][0], box[1][1]])

    np.save(output_path + "task1/detections_all_faces.npy", bounding_boxes)
    np.save(output_path + "task1/file_names_all_faces.npy", filenames)
    np.save(output_path + "task1/scores_all_faces.npy", probabilities)


def print_task_2(faces_detected, output_path):
    # TODO:
    bounding_boxes = []
    filenames = []
    probabilities = []

    for filename, (box, _, _, prob) in faces_detected:
        # TODO: Check the bounding box format
        filenames.append(filename)
        probabilities.append(prob)
        bounding_boxes.append([box[0][0], box[0][1], box[1][0], box[1][1]])

    np.save(output_path + "task1/detections_all_faces.npy", bounding_boxes)
    np.save(output_path + "task1/file_names_all_faces.npy", filenames)
    np.save(output_path + "task1/scores_all_faces.npy", probabilities)



def solve(folder_path, output_path):
    """
    Solves the task.
        1. Reads from a given folder.
        2. Computes the found faces.
        3. Computes the guys faces.
    """

    # reset output folder
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)
    os.makedirs(output_path + "task1/")
    os.makedirs(output_path + "task2/")

    images = read_images(folder_path)

    faces_detected = []
    
    print("Processing images...", flush=True)

    for img in tqdm(images):
        windows = sliding_window.find_faces(img[1])
        for window in windows:
            if window[-1] < 0.5:
                continue
            faces_detected.append((img[0], window))

    print_task_1(faces_detected, output_path)


if __name__ == "__main__":
    solve("../validare/simpsons_validare/", "../evaluare/fisiere_solutie/Moroianu_Theodor_334/")
