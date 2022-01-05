import os
import torch as th
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader, random_split
import pytorch_lightning as pl
import sources.constants as constants
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import sources.generate_dataset as generate_dataset
import torchvision.models as models
from tqdm import tqdm
from torch.utils.data import TensorDataset

model_path = "model/model.th"

dev = torch.device('cpu')
if th.cuda.is_available():
    dev = torch.device('cuda')

train_transform = transforms.Compose([
    transforms.RandomRotation(degrees=5),
    transforms.RandomAutocontrast(),
    # transforms.RandomAdjustSharpness(0.95),
    transforms.RandomResizedCrop(constants.SIZE_FACE_MODEL, scale=(0.9, 1)),
    # transforms.RandomEqualize(),
    # PEnc(),
    # transforms.RandomErasing(scale=(0.02, 0.2)),
    # transforms.GaussianBlur(3, sigma=(0.01, 0.01)),
    # transforms.RandomHorizontalFlip(),
    # transforms.RandomVerticalFlip()
])


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(2),

            # nn.BatchNorm2d(32),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            # nn.BatchNorm2d(128),

            nn.Flatten(),
            nn.Dropout(0.2),

            nn.Linear(128 * (constants.SIZE_FACE_MODEL // 8)**2, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            nn.Linear(128, 50),
            nn.ReLU(),
            nn.Linear(50, 6)
        )

    def forward(self, x):
        x = x.permute(0, 3, 1, 2).to(dev)
        return self.net(x).cpu()


# class Model(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.net = models.resnet18(pretrained=True)
#         self.fc = nn.Sequential(
#             nn.Dropout(0.4),
#             nn.Linear(1000, 6)
#         )

#     def forward(self, x):
#         x = x.permute(0, 3, 1, 2).to(dev)
#         return self.fc(self.net(x)).cpu()

model = None
criterion = nn.CrossEntropyLoss()

def compute_model_acc_loss(input, ground_truth):
    input = train_transform(input.permute(0, 3, 1, 2)).permute(0, 2, 3, 1)

    output = model(input)

    loss = criterion(output, ground_truth)
    accuracy = th.sum(th.argmax(output, dim=1) == ground_truth) / len(ground_truth)

    return accuracy, loss

def save_model():
    global model
    th.save(model.state_dict(), model_path)

def train_model(lr=1e-4, NR_EPOCHS=20, x=None, y=None):
    global model

    if model is None:
        model = Model().to(dev)
        print("Loading model to", dev)

        try:
            state = th.load(model_path)
            model.load_state_dict(state)
            model.eval()
            print("Model loaded from memory!", flush=True)
        except:
            print("Model could not be loaded! Training it...", flush=True)

    optimizer = torch.optim.Adam(
        model.parameters(), lr=lr
    )

    if x is None:
        x, y = generate_dataset.load_dataset()
    x = x.astype(np.float32)
    x /= 255.

    # Split to validation + train
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state= 21)
    x, y = [], []

    X_train = th.from_numpy(X_train).type(th.FloatTensor)
    X_test = th.from_numpy(X_test).type(th.FloatTensor)

    train_dataset = TensorDataset(X_train, th.from_numpy(y_train))
    test_dataset = TensorDataset(X_test, th.from_numpy(y_test))

    kwargs = {"num_workers": 5, "pin_memory": True}
    train_loader = th.utils.data.DataLoader(
        train_dataset, batch_size=128, shuffle=True #, **kwargs
    )
    test_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=128, shuffle=False# , **kwargs
    )

    model.train()

    for epoch in range(NR_EPOCHS):
        print(f"Epoch #{epoch+1}/{NR_EPOCHS}:", flush=True)

        batch_loss = []
        batch_acc = []

        print("Train...", flush=True)
        for input, gt in tqdm(train_loader):
            # input = input.to(dev)
            # gt = gt.to(dev)

            optimizer.zero_grad()
            acc, loss = compute_model_acc_loss(input, gt)

            batch_loss.append(loss.item())
            batch_acc.append(acc.item())

            loss.backward()
            optimizer.step()

        print(f"Average train loss: {np.mean(batch_loss)}, average train accuracy: {np.mean(batch_acc)}")

        batch_loss = []
        batch_acc = []

        model.eval()
        print("Eval...", flush=True)
        for input, gt in tqdm(test_loader):
            # input = input.to(dev)
            # gt = gt.to(dev)

            acc, loss = compute_model_acc_loss(input, gt)

            batch_loss.append(loss.item())
            batch_acc.append(acc.item())
        
        print(f"Average test loss: {np.mean(batch_loss)}, average test accuracy: {np.mean(batch_acc)}")

        th.save(model.state_dict(), model_path + f"{np.mean(batch_acc)}.th")

        model.train()

    model.eval()

    th.save(model.state_dict(), model_path)

    print("Model trained and saved!")


def load_model():
    global model

    model = Model().to(dev)
    try:
        state = th.load(model_path)
        model.load_state_dict(state)
        model.eval()
        print("Model loaded from memory!")
        return
    except:
        print("Model could not be loaded! Training it...")
        train_model()


def preprocess_image(image: np.ndarray) -> np.ndarray:
    image = cv.resize(image, (constants.SIZE_FACE_MODEL, constants.SIZE_FACE_MODEL))
    image = image / 255.0

    return image

def recognize_image(image: np.ndarray) -> int:
    """
        Returns the class of an image
    """
    global model

    if model is None:
        load_model()

    image = preprocess_image(image)

    image = image.reshape((1, constants.SIZE_FACE_MODEL, constants.SIZE_FACE_MODEL, 3))

    preds = model(th.from_numpy(image).type(th.FloatTensor))
    preds = F.softmax(preds, dim=1)

    return preds.detach().numpy()