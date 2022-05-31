#%%
import numpy as np
import matplotlib.pyplot as plt

INPUT_FOLDER = "../data/"

train_loss = np.load(INPUT_FOLDER + "train_loss.npy")
val_loss = np.load(INPUT_FOLDER + "val_loss.npy")

train_raw_acc = np.load(INPUT_FOLDER + "train_raw_accuracy.npy")
val_raw_acc = np.load(INPUT_FOLDER + "val_raw_accuracy.npy")

train_class_acc = np.load(INPUT_FOLDER + "train_class_accuracy.npy")
val_class_acc = np.load(INPUT_FOLDER + "val_class_accuracy.npy")

# %%
def smooth_vector(v):
    return [sum(v[i:i + 100]) / 101 for i in range(len(v) - 100)]

plt.figure(figsize=(10, 10))
val_loss_space = np.linspace(0, 1, len(val_loss) - 100)
plt.plot(val_loss_space, smooth_vector(val_loss), label="Validare")
train_loss_space = np.linspace(0, 1, len(train_loss) - 100)
plt.plot(train_loss_space, smooth_vector(train_loss), label="Antrenare")
plt.legend()
plt.show()

# %%

plt.figure(figsize=(8, 4))
val_acc_space = np.linspace(0, 1, len(val_raw_acc) - 100)
plt.plot(val_acc_space, smooth_vector(val_raw_acc), label="Validation Raw Accuracy")
plt.plot(val_acc_space, smooth_vector(val_class_acc), label="Validation Per-Class Accuracy")
train_acc_space = np.linspace(0, 1, len(train_raw_acc) - 100)
plt.plot(train_acc_space, smooth_vector(train_raw_acc), label="Train Raw Accuracy")
plt.plot(train_acc_space, smooth_vector(train_class_acc), label="Train Per-Class Accuracy")
plt.legend()
plt.grid()
plt.savefig("../accuracy.png", dpi=300)
plt.show()

# %%
