import cv2
import numpy as np

# Class for counting cells within a binary image
class CellCounter:
    
    # counts the cells based on connected components within the binary image
    # returns number of cells found
    def connectedComponents(mask):
        connectivity = 8
        output = cv2.connectedComponentsWithStats(mask,connectivity)
        # Possible TODO: Cell counting estimation could be improved by
        # output area analysis splitting areas that are most probably "connected" cells
        # e. g. using median as normal cell size
        return output[0]-1 # minus 1 due to the background    
    
    # counts the cells based on finding contours
    # inspired by answer to https://stackoverflow.com/questions/58751101/count-number-of-cells-in-the-image
    # returns number of cells, cell areas (including excluded findings), image with drawn contours
    def findingContours(mask, minimumCellSize):
        
        # using an ellipse as kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        # applying erosion and dilation for denoising
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)
        # finding the contorus
        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        mask_withContours = mask.copy()
        
        # extracting the areas for further ana
        nrCells = 0
        areas = []
        cnts=cnts[0]
        for c in cnts:
            area = cv2.contourArea(c)
            areas.append(area)
            if area>minimumCellSize:
                # draw a contour in grey
                cv2.drawContours(mask_withContours, c, -1, 125, 5)
                nrCells +=1

        return nrCells, areas, mask_withContours
