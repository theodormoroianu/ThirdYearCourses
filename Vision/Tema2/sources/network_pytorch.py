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

model_path = "model/model.th"

dev = torch.device('cpu')
if th.cuda.is_available():
    dev = torch.device('cuda')


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = models.resnet18(pretrained=True)
        self.fc = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(1000, 3)
        )

    def forward(self, x):
        return self.fc(self.resnet(x))

model = None
criterion = nn.CrossEntropyLoss()

def compute_model_acc_loss(input, ground_truth):
    output = model(input)

    loss = criterion(output, ground_truth)
    accuracy = th.sum(th.argmax(output, dim=1) == ground_truth) / len(ground_truth)

    return accuracy, loss


def train_model():
    global model

    model = Model().to(dev)
    
    try:
        state = th.load(model_path).to(dev)
        model.load_state_dict(state)
        return
    except:
        print("Model could not be loaded!")

    optimizer = torch.optim.Adam(
        model.parameters(), lr=1e-4
    )

    x, y = generate_dataset.load_dataset()
    x /= 255.

    # Split to validation + train
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state= 21)

    train_dataset = th.utils.TensorDataset(th.from_numpy(X_train), th.from_numpy(y_train))
    test_dataset = th.utils.TensorDataset(th.from_numpy(X_test), th.from_numpy(y_test))

    kwargs = {"num_workers": 5, "pin_memory": True}
    train_loader = th.utils.data.DataLoader(
        train_dataset, batch_size=32, shuffle=True, **kwargs
    )
    test_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=64, shuffle=False, **kwargs
    )

    NR_EPOCHS = 5

    model.train()

    for epoch in range(NR_EPOCHS):
        print(f"Epoch #{epoch}:", flush=True)

        batch_loss = []
        batch_acc = []

        for input, gt in tqdm(train_loader):
            input = input.to(dev)
            gt = gt.to(dev)

            optimizer.zero_grad()
            acc, loss = compute_model_acc_loss(input, gt)

            batch_loss.append(loss.item())
            batch_acc.append(acc.item())

            loss.backward()
            optimizer.step()

            print(loss)

        print(f"Average train loss: {th.mean(batch_loss)}, average train accuracy: {th.mean(batch_acc)}")

        batch_loss = []
        batch_acc = []

        model.eval()
        for input, gt in tqdm(test_loader):
            input = input.to(dev)
            gt = gt.to(dev)

            acc, loss = compute_model_acc_loss(input, gt)

            batch_loss.append(loss.item())
            batch_acc.append(acc.item())
        
        print(f"Average test loss: {th.mean(batch_loss)}, average test accuracy: {th.mean(batch_acc)}")

        model.train()

    model.eval()

    th.save(model.state_dict(), model_path)




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
        train_model()

    image = preprocess_image(image)

    image = image.reshape((1, constants.SIZE_FACE_MODEL, constants.SIZE_FACE_MODEL, 3))

    preds = model.predict(image)

    return preds