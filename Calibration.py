import numpy as np
import cv2
from DataHandler import DataHandler

# Calibration class features functions for determining parameters
# based on the ground truth data, which is manually labeled
class Calibration:
    
    # estimates optimum HSV thresholds (upper and lower bound) based on the manually labeled images
    def getHSVThresholds():
        imList = DataHandler.getImageList()
        
        # initialization of the bounds
        lowerHSVBound = np.array([255, 255, 255])
        upperHSVBound = np.array([0, 0, 0])

        for f in imList:
            # get image and ground truth label
            img = DataHandler.getImage(f)
            imgRef = DataHandler.getRefImage(f)
            
            # reduce image content to label area
            img[imgRef==0]=0
            
            # transform to HSV colourspace
            img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
            # for all channels (H,S,V)
            for k in range(np.shape(img)[-1]):
                data = img[:,:,k]
                data = data.ravel()
                # build histogram without 0 zero entries, as these are related to the mask and therefore, are a huge amount
                hist,bins = np.histogram(data.ravel(),255,[1,256])
                
                # 90% threshold has been found empirically
                threshold = max(hist)*.9
                threshIdx = np.where(hist>threshold)[0]
                
                # reduce histogram to boundary values
                hist = hist[threshIdx]
                bins = bins[threshIdx]

                # update boundaries
                lowerHSVBound[k] = min(bins[0],lowerHSVBound[k])
                upperHSVBound[k] = max(bins[-1],upperHSVBound[k]) 
                
        return lowerHSVBound, upperHSVBound
    
    # returns cell sizes of the manually labeled images. Calculation is based on finding contours
    def getCellSizes():
        imList = DataHandler.getImageList()
        
        cellAreas = []
        for f in imList:
            # find contours on labeled image
            imgRef = DataHandler.getRefImage(f)
            cnts = cv2.findContours(imgRef.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[1]
            for c in cnts:
                # calculate the pixel area of each contour found
                area = cv2.contourArea(c)
                
                # TODO: area is 0 sometimes. Is this a bug? Has to be investigated.
                if area > 0:
                    cellAreas.append(area)
                
        return cellAreas