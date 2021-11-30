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
import src.data_generator as data_gen

MODEL_PATH = "model/"
MODEL_NAME = "model.bin"

def extract_from_dir(dir: str):
    X = []
    y = []
    for i in range(10):
        for d in os.listdir(dir + "{}".format(i)):
            t_img = cv2.imread(dir + "{}".format(i)+"/"+d)
            t_img = cv2.cvtColor(t_img,cv2.COLOR_BGR2GRAY)
            X.append(t_img)
            y.append(i)

    X = np.array(X)
    y = np.array(y)

    return X, y

# define model
# motel is taken from https://www.kaggle.com/kshitijdhama/printed-digits-dataset/version/10
def larger_model():
    # create model
	model = keras.Sequential([
        Conv2D(30, (5, 5), input_shape=(28, 28, 1), activation='relu'),
        MaxPooling2D(),
        Conv2D(15, (3, 3), activation='relu'),
        MaxPooling2D(),
        Dropout(0.2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(50, activation='relu'),
        Dense(10, activation='softmax')
    ])
    

    # Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# For avoiding to train on module load
model = None

# # For tensordoard. Don't really need this but oh well
# log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

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

    print("Generating training data...")
    data_gen.generate_train_data()


    X1, y1 = extract_from_dir("assets/")
    X2, y2 = extract_from_dir("data/")

    # take from both dataset from kaggle and dataset from found digits.
    X = np.concatenate([X1, X2])
    y = np.concatenate([y1, y2])

    # Split to validation + train
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.20, random_state= 21)

    X_train = X_train.reshape((X_train.shape[0], 28, 28, 1)).astype('float32')
    X_test = X_test.reshape((X_test.shape[0], 28, 28, 1)).astype('float32')

    # normalize
    X_train = X_train / 255.0
    X_test = X_test / 255.0

    # one-hot encode
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    print("Training model...")
    model.fit(
        X_train,
        y_train,
        validation_data=(X_test, y_test),
        epochs=20,
        batch_size=10,
        # callbacks=[tensorboard_callback]
    )

    # Final evaluation of the model
    scores = model.evaluate(X_test, y_test, verbose=0)

    print("Validation error: %.2f%%" % (100-scores[1]*100))

    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)

    model.save_weights(MODEL_PATH + MODEL_NAME)



def preprocess_digit(digit: np.ndarray) -> np.ndarray:
    """
        Converts a single digit to grayscale, scales it to (28x28), turns white to black.
    """
    image = cv.cvtColor(digit, cv.COLOR_BGR2GRAY)
    # _, image = cv.threshold(image, 100, 255, cv.THRESH_BINARY)

    image = 255 - image
    image = cv.resize(image, (28, 28))

    return image

def recognize_digit(digit: np.ndarray) -> int:
    """
        Returns the class (0-9) of a single digit
    """
    global model

    fit_model()

    image = preprocess_digit(digit)
    # plt.imshow(image)
    # plt.show()

    image = image.reshape((1, 28, 28, 1))
    image = image.astype(np.float32) / 255

    preds = model.predict(image)

    # print(preds)

    if constants.DEBUG_DIGITS:
        constants.show_image(str(np.argmax(preds)), image[0])

    return np.argmax(preds[0])