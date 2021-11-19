# Proiect Vision

## Dependinte

Proiectul are urmatoarele dependinte:

    TODO: Add version
 * numpy
 * opencv-python
 * tensorflow
 * scikit-learn
 * pyyaml
 * h5py

## Resurse folosite

Am folosit multe resurse pentru acest proiect.

Resursele folosite sunt:

 * https://www.kaggle.com/kshitijdhama/printed-digits-dataset/version/10 - am luat datele de antrenare si structura retelei.
 * https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/ - am luat codul folosit pentru schimbarea de perspectiva.


## Cum se ruleaza proiectul

Pasii pentru a executa proiectul sunt:
 * Sa ne asiguram ca datele de antrenare se gasesc in folderul `antrenare`.
 * Sa deschidem `project.ipynb` si sa modificam corect path-ul cu datele de testare si output-path.
 * Sa executam celulele.
 
## Ce date de antrenare folosesc in retea

Pentru a obtine mai multe date de antrenare, am "reciclat" o mare parte (15/20 respectiv 30/40) din cifrele din datele date.
In plus de acestea, am mai folosit si datele obtinute de pe Kaggle.

## Mentinui

 * Am facut proiectul pe linux. Este posibil ca path-urile sa nu mearga corect pe Windows.








 * https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/

Your project should include a README file containing the following information:

1. the libraries required to run the project including the full version of each library

Example:

numpy==1.15.4
opencv_python==4.1.1.26
scikit_image==0.15.0
tensorflow_gpu==1.12.0
Pillow==7.0.0
scikit_learn==0.22.1
skimage==0.0
tensorflow==2.1.0


Module folosite:
opencv-python==4.5.4.58
numpy
tesseract (pytesseract + tesseract on Linux)


2. how to run each task and where to look for the output file.

Example:

Task 1: 
script: task_1.py
function: run_task1(input_folder_name), where input_folder_name is the path to the folder containing the images for task1
output: the output file is results/task1.txt

Task 2: ...