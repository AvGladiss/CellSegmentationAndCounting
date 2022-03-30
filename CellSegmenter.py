import cv2

# class for cell segmenting featuring different functions to do the job
class CellSegmenter:
    
    # segments an image by first using an upper bound and then using Otsu's method
    def segmentByThresholdAndOtsu(image, threshold):
        imageCopy = image.copy()
        # convert image to grayscale if still RGB
        if (len(imageCopy.shape)>2):
            imageCopy = cv2.cvtColor(imageCopy,cv2.COLOR_BGR2GRAY)
        
        # using the upper bound, kind of windowing but only for high values
        imageCopy[imageCopy>threshold]=threshold
        # using Otsu's method and inverting for being congruent with the manually labeled images
        mask = cv2.threshold(imageCopy, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)[1]
        return mask
    
    # segments an image by using lower and upper bounds in HSV colour space
    def segmentByHSVTresholds(image,lowerThresholdHSV,upperThresholdHSV):
        # convert image from RGB to HSV
        img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        # applying upper and lower bound
        mask = cv2.inRange(img,lowerThresholdHSV,upperThresholdHSV)
        return mask   