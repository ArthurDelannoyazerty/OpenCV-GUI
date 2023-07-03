import cv2 as cv

def controller(img, brightness=255, contrast=127):
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
  
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
  
    if brightness != 0:
  
        (shadow, max) = (brightness, 255) if brightness>0 else (0, 255+brightness)
  
        cal = cv.addWeighted(img, (max - shadow) / 255, img, 0, shadow)
  
    else:
        cal = img
  
    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)
  
        cal = cv.addWeighted(cal, Alpha, cal, 0, Gamma)
  
  
    return cal

