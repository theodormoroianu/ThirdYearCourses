#%%
import numpy as np
import matplotlib.pyplot as plt

INPUT_FOLDER = "../../../SmartForms/backend/data/OCR/"

train_loss = np.load(INPUT_FOLDER + "train_loss.npy")
val_loss = np.load(INPUT_FOLDER + "val_loss.npy")

train_raw_acc = np.load(INPUT_FOLDER + "train_raw_accuracy.npy")
val_raw_acc = np.load(INPUT_FOLDER + "val_raw_accuracy.npy")

train_class_acc = np.load(INPUT_FOLDER + "train_class_accuracy.npy")
val_class_acc = np.load(INPUT_FOLDER + "val_class_accuracy.npy")

# %%

