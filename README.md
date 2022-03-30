# CellSegmentationAndCounting
Python implemenation for segmentation and counting of cell nuclei in histological H&amp;E stains

# Testing environment
This code has been tested on a WSL2-instance running Ubuntu 20.04 with Python 3.8.5.
Dependencies:
- opencv-pyton
- numpy
- matplotlib
- scikit-image

Execute code by running 'python3 task.py'
H&E stained images should be in the directory `data/tissue_images` and reference images for comparison in `data/mask binary`. Processed data will be saved in `data/output`.

# Outlook
Python package `squidpy` has been found that specializes in single cell analysis. Might be useful for extending this task.
