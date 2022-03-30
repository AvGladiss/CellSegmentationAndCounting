import matplotlib.pyplot as plt
import numpy as np

from DataHandler import DataHandler
from Calibration import Calibration
from CellSegmenter import CellSegmenter
from CellCounter import CellCounter

## Setting parameters
# has been found empirically
thresholdBeforeOtsu = 80
# has been found empirically
minimumCellSize = 50

# output directory for images showing the comparison of ground truth and segmented data
outputDir = "data/output/"

# based on the findings of `evaluation.py`, Otsu is used for segmentation and contour-finding based cell counting
imList = DataHandler.getImageList()
for f in imList:
    print("Evaluating file "+f)
    
    # reading in the data
    img = DataHandler.getImage(f)
    imgRef = DataHandler.getRefImage(f)
    
    # segmentation
    segmentedImg = CellSegmenter.segmentByThresholdAndOtsu(img,thresholdBeforeOtsu)
    
    # cell counting for segmented image
    output = CellCounter.findingContours(segmentedImg,minimumCellSize)
    nrCells_segmentedImg = output[0]
    segmentedImg_withContours = output[2]
    
    # cell counting for reference image
    output = CellCounter.findingContours(imgRef,minimumCellSize)
    nrCells_imgRef = output[0]
    imgRef_withContours = output[2]
    
    print(str(nrCells_segmentedImg)+" cell nuclei found. "+str(nrCells_imgRef)+" cell nuclei found in reference image.")
    
    # plotting and saving the findings in comparison to the manually labeled data
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(imgRef_withContours,cmap="gray")
    ax[0].axis('off')
    ax[0].set_title("Reference: "+str(nrCells_imgRef)+" cell nuclei")
    ax[1].imshow(segmentedImg_withContours,cmap="gray")
    ax[1].axis('off')
    ax[1].set_title("Segmented: "+str(nrCells_segmentedImg)+" cell nuclei")

    plotFilename = f[:-4]+".png"
    plt.savefig(outputDir+plotFilename)
    # plt.show()
    plt.close()
    
    print("")