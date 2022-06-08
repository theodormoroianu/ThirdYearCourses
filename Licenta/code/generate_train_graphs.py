#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

INPUT_FOLDER = "../data/"

train_loss = np.load(INPUT_FOLDER + "train_loss.npy")
val_loss = np.load(INPUT_FOLDER + "val_loss.npy")

train_raw_acc = np.load(INPUT_FOLDER + "train_raw_accuracy.npy")
val_raw_acc = np.load(INPUT_FOLDER + "val_raw_accuracy.npy")

train_class_acc = np.load(INPUT_FOLDER + "train_class_accuracy.npy")
val_class_acc = np.load(INPUT_FOLDER + "val_class_accuracy.npy")

# %%
def smooth_vector(v):
    return gaussian_filter(v, sigma=1)
    return [sum(v[i:i + 100]) / 101 for i in range(len(v) - 100)]

plt.figure(figsize=(6, 2))
plt.title("Loss")
val_loss_space = np.linspace(0, 1, len(val_loss))
plt.plot(val_loss_space, val_loss, label="Validation")
train_loss_space = np.linspace(0, 1, len(train_loss))
plt.plot(train_loss_space, train_loss, label="Train")
plt.legend()
plt.ylabel("Cross-entropy loss")
plt.xlabel("Training completed")
plt.grid()
plt.savefig("loss.png", dpi=300)
plt.show()

# %%

plt.figure(figsize=(6, 4))
plt.title("Accuracy")
val_acc_space = np.linspace(0, 1, len(val_raw_acc))
plt.plot(val_acc_space, smooth_vector(val_raw_acc) * 100, label="Validation Raw Accuracy")
plt.plot(val_acc_space, smooth_vector(val_class_acc) * 100, label="Validation Per-Class Accuracy")
train_acc_space = np.linspace(0, 1, len(train_raw_acc))
plt.plot(train_acc_space, smooth_vector(train_raw_acc) * 100, label="Train Raw Accuracy")
plt.plot(train_acc_space, smooth_vector(train_class_acc) * 100, label="Train Per-Class Accuracy")
plt.legend()
plt.ylabel("Accuracy (percentage)")
plt.xlabel("Training completed")
plt.ylim(bottom=10, top=100)
plt.grid()
plt.savefig("accuracy.png", dpi=300)
plt.show()

# %%
