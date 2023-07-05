import numpy as np
import cv2 as cv

def controller(image):
    
    center_x = 30
    center_y = 45
    angle = 10
    scale=0.5
    
    rotated_image = cv.warpAffine(image, cv.getRotationMatrix2D((center_x, center_y), angle, scale), (image.shape[:2][1], image.shape[:2][0]))

    return rotated_image




image = cv.imread("img_test.png")
result = controller(image)
cv.imshow("t", result)
cv.waitKey()