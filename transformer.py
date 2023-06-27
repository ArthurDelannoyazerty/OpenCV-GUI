import cv2 as cv

class Transformer():
    """An objet that transform a given image with the specified transforamtion with opencv"""
    def __init__(self):
        self.dict_func_opencv = {
                "gaussianblur" : cv.GaussianBlur,
                "colorchange" : cv.cvtColor
            }
    
    def get_parameters(self, transform_string):
        list = transform_string.split("_")
        for index, element in enumerate(list):
            list[index] = int(element) if element.isnumeric() else element
        return list

    def transform(self, item_before, item_current):
        print("transform")
        img_array_to_transform = item_before.img_array
        transform_string = item_current.str_transformation

        cv.COLOR_RGB2GRAY

        parameters = self.get_parameters(transform_string)
        img_arrays_transformed =  self.dict_func_opencv.get(parameters[0], lambda: 'Invalid')(img_array_to_transform, *parameters[1:])
        return img_arrays_transformed