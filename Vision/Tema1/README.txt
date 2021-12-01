# Project Vision

## Dependencies

The required dependencies are the latest versions (but probably any recent one will work) of:
 * numpy
 * opencv-python
 * tensorflow
 * scikit-learn
 * pyyaml
 * h5py

## Used Resources

For this project I used:

 * https://www.kaggle.com/kshitijdhama/printed-digits-dataset/version/10 - dataset + network architecture
 * https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/ - perspective transform


## Run The Project

The steps are:
 * Place the test data in a folder somewhere in the project.
 * Open "project.ipynb" and specify the desired input path and output path.
 * Run the notbook.

This should run both tasks, and the bonus.

In more details:
    1. Create a folder "real_test" in the "evaluare" directory.
    2. Place the test files (the "clasic" and the "jigsaw" folders) in the "real_test" directory.
    3. Open "project.ipynb" in jupyter notebook. All links are relative to it, so (maybe?) the root folder of jupyter has to be this project.
    4. Change in "project.ipynb" the input path to "evaluare/real_test/"
    5. Update in "evaluare/cod_evaluare/evalueaza_solutie.py" the input and output folder.
    6. Run the notebook.

