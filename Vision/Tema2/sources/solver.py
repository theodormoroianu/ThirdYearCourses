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
    bounding_boxes = [[], [], [], []]
    filenames = [[], [], [], []]
    probabilities = [[], [], [], []]

    for filename, (box, type, prob_type, prob_not_a_face) in faces_detected:
        # TODO: Maybe add to other classes as well?
        if type > 3:
            continue
        filenames[type].append(filename)
        probabilities[type].append(prob_type)
        bounding_boxes[type].append([box[0][0], box[0][1], box[1][0], box[1][1]])

    for i in range(4):
        np.save(
            output_path + "task2/detections_" + constants.SIM_NAMES[i] + ".npy",
            np.array(bounding_boxes[i])
        )
        np.save(
            output_path + "task2/file_names_" + constants.SIM_NAMES[i] + ".npy",
            np.array(filenames[i])
        )
        np.save(
            output_path + "task2/scores_" + constants.SIM_NAMES[i] + ".npy",
            np.array(probabilities[i])
        )



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
            faces_detected.append((img[0], window))

    print_task_1(faces_detected, output_path)
    print_task_2(faces_detected, output_path)


if __name__ == "__main__":
    solve("../validare/simpsons_validare/", "../evaluare/fisiere_solutie/Moroianu_Theodor_334/")
