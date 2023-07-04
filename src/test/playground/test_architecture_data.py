import numpy as np
import cv2 as cv

def controller(image, brightness=128, contrast=255):
    # brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
  
    # contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))

    cal = (cv.addWeighted(((cv.addWeighted(image, ((255 if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))>0 else 255+(int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))) - ((int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))) if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))>0 else 0)) / 255, image, 0, (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))) if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))>0 else 0) if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))) != 0 else image)), float(131 * ((int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))) + 127)) / (127 * (131 - (int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))))), ((cv.addWeighted(image, ((255 if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))>0 else 255+(int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))) - ((int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))) if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))>0 else 0)) / 255, image, 0, (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))) if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))>0 else 0) if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))) != 0 else image)), 0, 127 * (1 - float(131 * ((int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))) + 127)) / (127 * (131 - (int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127)))))))) if (int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127)))!=0 else (cv.addWeighted(image, ((255 if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))>0 else 255+(int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))) - ((int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))) if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))>0 else 0)) / 255, image, 0, (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))) if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)))>0 else 0) if (int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))) != 0 else image)
  
    # if brightness != 0:
  
    #     cal = cv.addWeighted(image, ((255 if brightness>0 else 255+brightness) - (brightness if brightness>0 else 0)) / 255, image, 0, brightness if brightness>0 else 0)
  
    # else:
    #     cal = image
  
    # if contrast != 0:
  
    #     cal = cv.addWeighted(((cv.addWeighted(image, ((255 if brightness>0 else 255+brightness) - (brightness if brightness>0 else 0)) / 255, image, 0, brightness if brightness>0 else 0) if brightness != 0 else image)), float(131 * (contrast + 127)) / (127 * (131 - contrast)), ((cv.addWeighted(image, ((255 if brightness>0 else 255+brightness) - (brightness if brightness>0 else 0)) / 255, image, 0, brightness if brightness>0 else 0) if brightness != 0 else image)), 0, 127 * (1 - float(131 * (contrast + 127)) / (127 * (131 - contrast))))
  
  
    return cal




image = cv.imread("img_test.png")
result = controller(image)
cv.imshow("t", result)
cv.waitKey()