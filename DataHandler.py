import os
import cv2

# DataHandler class features functions for reading the images and
# reference images (manually labeled)
class DataHandler:
    
    # directory containing the images of H&E stains
    imDir = "data/tissue_images"
    # directory containing the manually labeled images
    refImDir = "data/mask binary"
    
    # suffix for H&E stained images
    imageSuffix = ".tif"
    # suffix for labeled images
    maskSuffix = ".png"
    
    # searches a directory for all files with a filename suffix, returns list of found files
    def getImageList():        
        
        imageList = []
        for file in os.listdir(DataHandler.imDir):
            if file.endswith(DataHandler.imageSuffix):
                imageList.append(file)
            
        return imageList
    
    # returns the H&E stained image
    def getImage(filename):
        img = cv2.imread(DataHandler.imDir+"/"+filename)
        return img
    
    # returns the manually labeled image for a H&E stained image
    def getRefImage(image_filename):
        mask_Filename = image_filename[:-len(DataHandler.imageSuffix)]+DataHandler.maskSuffix
        img = cv2.imread(DataHandler.refImDir+"/"+mask_Filename)
        
        contentEqual = True
        for k in range(img.shape[-1]-1):
            contentEqual &= (img[:,:,k]==img[:,:,k+1]).all()
        
        if contentEqual:
            img = img[:,:,0]
        else:
            print("Warning. Reference image has channels of different content.")
            
        return img
    
    