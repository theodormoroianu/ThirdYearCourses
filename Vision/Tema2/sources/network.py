"""
    Module able to recognize digits
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import *
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.utils import to_categorical
import datetime
import numpy as np
import os
import cv2
import sources.constants as constants
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import sources.generate_dataset as generate_dataset

MODEL_PATH = "model/"
MODEL_NAME = "model.bin"

# define model
# motel is taken from https://www.kaggle.com/kshitijdhama/printed-digits-dataset/version/10
def larger_model():
    # create model
	model = keras.Sequential([
        Conv2D(32, (5, 5), input_shape=(constants.SIZE_FACE_MODEL, constants.SIZE_FACE_MODEL, 3), activation='relu'),
        Conv2D(64, (5, 5), activation='relu'),
        MaxPooling2D(),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu'),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(),
        BatchNormalization(),
        Dropout(0.2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(50, activation='relu'),
        Dense(6, activation='softmax')
    ])
    
    # Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# For avoiding to train on module load
model = None

def train_model():
    global model
    print("Generating training data...")
    
    X, y = generate_dataset.load_dataset()

    # Split to validation + train
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.1, random_state= 21)

    # X_train = X_train.reshape((X_train.shape[0], 28, 28, 1)).astype('float32')
    # X_test = X_test.reshape((X_test.shape[0], 28, 28, 1)).astype('float32')

    # normalize
    X_train = X_train / 255.0
    X_test = X_test / 255.0

    # one-hot encode
    y_train = to_categorical(y_train)
    y_test_raw = y_test
    y_test = to_categorical(y_test)

    print("Training model...")
    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)
    # TODO: https://github.com/tensorflow/tensorflow/issues/29558
    model.fit(
        X_train,
        y_train,
        validation_data=(X_test, y_test),
        epochs=20,
        batch_size=50,
        
        # callbacks=[tensorboard_callback]
    )

    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)

    model.save_weights(MODEL_PATH + MODEL_NAME)

    # Final evaluation of the model
    scores = model.evaluate(X_test, y_test, verbose=0)

    predictions = np.argmax(model.predict(X_test), axis=1)
    confusion_matrix = tf.math.confusion_matrix(y_test_raw, predictions)

    print("Confusion matrix:")
    print(confusion_matrix)

    print("Validation error: %.2f%%" % (100-scores[1]*100))

def fit_model():
    """ from 0-255
        Trains model.
        If model exists already, just returns.
    """
    global model
    if model is not None:
        return

    model = larger_model()
    
    try:
        model.load_weights(MODEL_PATH + MODEL_NAME)
        print("Loaded model from disk...")
        return
        
    except:
        print("Model not found on disk.")

    train_model()

def load_and_train_model():
    global model
    model = larger_model()
    
    model.load_weights(MODEL_PATH + MODEL_NAME)
    print("Loaded model from disk...")
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

    fit_model()

    image = preprocess_image(image)

    image = image.reshape((1, constants.SIZE_FACE_MODEL, constants.SIZE_FACE_MODEL, 3))

    preds = model.predict(image)

    return preds