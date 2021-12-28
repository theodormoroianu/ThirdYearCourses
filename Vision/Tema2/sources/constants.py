
DEBUG = False

SIM_NAMES = ["bart", "homer", "lisa", "marge"]
SIM_LABEL_ORDER = {
    "bart": 0,
    "homer": 1,
    "lisa": 2,
    "marge": 3,
    "unknown": 4,
    "not_a_face": 5
}

face_heigth_width_ratio = {
    "bart": [],
    "homer": [],
    "lisa": [],
    "marge": [],
    "unknown": [],
}

# size in px of the face used for recognition
SIZE_FACE_MODEL = 64

# nr of negative samples per input image
NR_NEGATIVE_SAMPLES_PER_IMAGE = 4
# maximal intersection over reunion for negative sample
MAXIMAL_INTERSECTION_OVER_REUNION_NEGATIVE_SAMPLE = 0.2

# minimal size of considered windows
MINIMAL_WINDOWS_PIXEL_SIZE = 64

# What to multiply windows by
SLIDING_WINDOW_RESCALE_FACTOR = 0.91

# stride when performing a sliding window (multiply by the window size in pixels to get actual stride)
SLIDING_WINDOW_STRIDE = 0.2