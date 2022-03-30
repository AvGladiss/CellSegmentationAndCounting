# CellSegmentationAndCounting
Python implemenation for segmentation and counting of cell nuclei in histological H&amp;E stains

# Architecture

## DataHandler

Feautures functions for reading H&E stained images and binary reference images

## Calibration

Features functions for estimating optimum parameters for the task based on the reference images. Is actually not used in the final code in `task.py`.

## CellSegmenter

Features functions for segmented cells using either an upper bound and Otsu's method on a grayscale image or by applying lower and upper bounds on an image in HSV colour space.

## CellCounter

Features functions for counting cells in a binary image via either connected components or finding contours and evaluation of areas.

## evaluation.py

Script for evaluating the methods in `CellSegmenter.py` and `CellCounter.py`.

## task.py

Script that segments and counts cell nuclei in H&E stained images. Outputs images comparing the result with a reference image, e.g.

![Human_Mediastinum_03](https://user-images.githubusercontent.com/22216765/160824035-f2686b9f-fd42-4b82-aed1-68a02ecc537c.png)

# Testing environment
This code has been tested on a WSL2-instance running Ubuntu 20.04 with Python 3.8.5.
Dependencies:
- opencv-pyton
- numpy
- matplotlib
- scikit-image

Execute code by running `python3 task.py`
Evaluation of the implemented methods can be performed executing `python3 evaluation.py`.
H&E stained images should be in the directory `data/tissue_images` and reference images for comparison in `data/mask binary`. Processed data will be saved in `data/output`.

# Outlook
Python package `squidpy` has been found that specializes in single cell analysis. Might be useful for extending this task.
