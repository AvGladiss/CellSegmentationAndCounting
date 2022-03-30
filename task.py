import sys
import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import structural_similarity

from DataHandler import DataHandler
from Calibration import Calibration
from CellSegmenter import CellSegmenter
from CellCounter import CellCounter

            
# QualityCheck features functions for comparing the segmentation and cell-counting functions implemented
class QualityCheck:
    
    # Evaluates the two cell counting functions based on connected components and contour findings
    # segmentation Method may be 'Otsu' or 'HSV'. See CellSegmenter for details
    # minimumCellSize is only used for contour-finding-based counting
    def evaluateCounting(minimumCellSize,segmentationMethod='Otsu',lowerHSVBound=None,upperHSVBound=None,thresholdBeforeOtsu=None):
        
        # initialization
        nrCells_ConnectedComponents_GroundTruth = []
        nrCells_FindingContours_GroundTruth = []
        
        nrCells_ConnectedComponents = []
        nrCells_FindingContours = []
        
        imList = DataHandler.getImageList()
        for f in imList:
            # reading image and labeled image
            img = DataHandler.getImage(f)
            imgRef = DataHandler.getRefImage(f)
            
            # segmentation
            segmentedImage = []
            if segmentationMethod=='Otsu' and thresholdBeforeOtsu is not None:
                segmentedImage = CellSegmenter.segmentByThresholdAndOtsu(img,thresholdBeforeOtsu)
            elif segmentationMethod=='HSV' and lowerHSVBound is not None and upperHSVBound is not None:
                segmentedImage = CellSegmenter.segmentByHSVTresholds(img,lowerHSVBound,upperHSVBound)
            else:
                print("Error while segmenting image. Parameters set up incompletely.")
            
            # calculating cell numbers for reference image
            nrCells_ConnectedComponents_GroundTruth.append(CellCounter.connectedComponents(imgRef))
            nrCells_FindingContours_GroundTruth.append(CellCounter.findingContours(imgRef,minimumCellSize)[0])
            
            # calculating cell numbers for segmented image
            nrCells_ConnectedComponents.append(CellCounter.connectedComponents(segmentedImage))
            nrCells_FindingContours.append(CellCounter.findingContours(segmentedImage,minimumCellSize)[0])
        
        # converting lists to arrays
        nrCells_ConnectedComponents_GroundTruth = np.array(nrCells_ConnectedComponents_GroundTruth)
        nrCells_ConnectedComponents = np.array(nrCells_ConnectedComponents)
        nrCells_FindingContours_GroundTruth = np.array(nrCells_FindingContours_GroundTruth)
        nrCells_FindingContours = np.array(nrCells_FindingContours)
        
        # calculating difference and least square errors
        diff_connectedComponents = nrCells_ConnectedComponents_GroundTruth-nrCells_ConnectedComponents
        lse_connectedComponents = np.sum(np.square(diff_connectedComponents))
        
        diff_findingContours = nrCells_FindingContours_GroundTruth-nrCells_FindingContours
        lse_findingContours = np.sum(np.square(diff_findingContours))
        
        print("Counting using connected components:")
        print("Std: {:.2f}, Least-Square-Error: {:.2f}".format(np.std(diff_connectedComponents),lse_connectedComponents))
        print("")
        print("Counting using finding contours:")
        print("Std: {:.2f}, Least-Square-Error: {:.2f}".format(np.std(diff_findingContours),lse_findingContours))
        
    # Evaluates the two segmentation functions based on HSV tresholds and Otsu
    def evaluateSegmentation(lowerHSVBound,upperHSVBound,thresholdBeforeOtsu):
        
        # initialization of lists containing metrics
        ssims_HSV = []
        ssims_Otsu = []
        dice_HSV = []
        dice_Otsu = []
        
        imList = DataHandler.getImageList()
        for f in imList:
            # reading image and labeled image
            img = DataHandler.getImage(f)
            imgRef = DataHandler.getRefImage(f)
                
            segmentation_HSV = CellSegmenter.segmentByHSVTresholds(img,lowerHSVBound,upperHSVBound)    
            segmentation_Otsu = CellSegmenter.segmentByThresholdAndOtsu(img,thresholdBeforeOtsu)

            ssims_HSV.append(QualityCheck.getSSIM(imgRef,segmentation_HSV))
            ssims_Otsu.append(QualityCheck.getSSIM(imgRef,segmentation_Otsu))

            dice_HSV.append(QualityCheck.getDiceCoefficient(imgRef,segmentation_HSV))
            dice_Otsu.append(QualityCheck.getDiceCoefficient(imgRef,segmentation_Otsu))
            
        print("Segmentation using HSV bounds:")
        print("SSIM: average of {:.2f}, std of {:.2f}".format(np.mean(ssims_HSV),np.std(ssims_HSV)))
        print("Dice: average of {:.2f}, std of {:.2f}".format(np.mean(dice_HSV),np.std(dice_HSV)))
        print("")
        print("Segmentation using Otsu's method:")
        print("SSIM: average of {:.2f}, std of {:.2f}".format(np.mean(ssims_Otsu),np.std(ssims_Otsu)))
        print("Dice: average of {:.2f}, std of {:.2f}".format(np.mean(dice_Otsu),np.std(dice_Otsu)))

        
    # Returns the Structure Similarity Index of two images
    def getSSIM(imageA, imageB):
        score = structural_similarity(imageA, imageB, full=True)[0]
        return score
    
    # Returns the Dice similiarity coefficient of two images
    def getDiceCoefficient(imageA, imageB):
        score = np.sum(imageA.ravel()==imageB.ravel())*2. / (len(imageA.ravel()) + len(imageB.ravel()))
        return score        

    
## Setting parameters
# getting lower and upper HSV bound
lowerThreshHSV, upperThreshHSV = Calibration.getHSVThresholds()

# has been found empirically
thresholdBeforeOtsu = 80
# has been found empirically
minimumCellSize = 50

# output directory for images showing the comparison of ground truth and segmented data
outputDir = "data/output/"

## evaulate segmentation methods
QualityCheck.evaluateSegmentation(lowerThreshHSV,upperThreshHSV,thresholdBeforeOtsu)
print("")
print("Based on these findings, Otsu's method (and an upper boundary) will be used.")
print("")

## evaluate cell counting methods
QualityCheck.evaluateCounting(minimumCellSize,segmentationMethod='Otsu',thresholdBeforeOtsu=thresholdBeforeOtsu)
print("")
print("Based on these findings, contour-finding-based cell counting will be used.")
print("")

## finally do the work
imList = DataHandler.getImageList()
for f in imList:
    
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