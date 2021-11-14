"""
    Module able to recognize digits
"""

from tensorflow import keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.utils import to_categorical
import datetime
import numpy as np
import os
import cv2
import src.constants as constants
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

X = []
y = []
for i in range(10):
    for d in os.listdir("assets/{}".format(i)):
        t_img = cv2.imread("assets/{}".format(i)+"/"+d)
        t_img = cv2.cvtColor(t_img,cv2.COLOR_BGR2GRAY)
        X.append(t_img)
        y.append(i)

X = np.array(X)
y = np.array(y)

X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.20, random_state= 21)

X_train = X_train.reshape((X_train.shape[0], 28, 28, 1)).astype('float32')
X_test = X_test.reshape((X_test.shape[0], 28, 28, 1)).astype('float32')
# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255
# one hot encode outputs
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
num_classes = y_test.shape[1]


def larger_model():
    # create model
	model = keras.Sequential(
    [
        Conv2D(30, (5, 5), input_shape=(28, 28, 1), activation='relu'),
        MaxPooling2D(),
        Conv2D(15, (3, 3), activation='relu'),
        MaxPooling2D(),
        Dropout(0.2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(50, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    

    # Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

model = None
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)


def fit_model():
    global model
    if model is not None:
        return

    model = larger_model()
    print("Training model...")
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=10,callbacks=[tensorboard_callback])
    # Final evaluation of the model
    scores = model.evaluate(X_test, y_test, verbose=0)

    print("Large CNN Error: %.2f%%" % (100-scores[1]*100))


def recognize_digit(digit: np.ndarray) -> int:
    """
        Initialize the digit recognition
    """
    global model

    fit_model()

    image = cv.cvtColor(digit, cv.COLOR_BGR2GRAY)
    _, image = cv.threshold(image, 100, 255, cv.THRESH_BINARY)

    image = 255 - image
    image = cv.resize(image, (28, 28))

    image = image.reshape((1, 28, 28, 1))

    preds = model.predict(image)

    if constants.DEBUG_DIGITS:
        constants.show_image(str(np.argmax(preds)), image[0])

    return np.argmax(preds[0])