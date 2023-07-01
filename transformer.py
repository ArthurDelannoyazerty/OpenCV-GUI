import cv2 as cv

class Transformer():
    """An objet that transform a given image with the specified transforamtion with opencv"""
    def __init__(self):
        self.commands = {
            'Change Colorspace': {
                'command': 'cv.cvtColor(image, colorspace_mode)',
                'number_parameters' : 2,
                'condition': 'len(image.shape)==3 and image.shape[2]==3',
                'gui':{
                    'slider':{
                        'number_slider': 0
                    },
                    'menu':{
                        'number_menu': 1,
                        'menu0': {
                            'name': 'Color conversion',
                            'variable_name': 'colorspace_mode',
                            'menu_item':{
                                'Grayscale' : cv.COLOR_BGR2GRAY,
                                'HSV to RGB': cv.COLOR_HSV2RGB,
                                'LAB to RGB': cv.COLOR_LAB2RGB,
                                'BGR to RGB': cv.COLOR_BGR2RGB,
                                'RGB to BGR': cv.COLOR_RGB2BGR,
                                'BGR to HSV': cv.COLOR_BGR2HSV,
                                'HSV to BGR': cv.COLOR_HSV2BGR,
                                'BGR to LAB': cv.COLOR_BGR2LAB,
                                'LAB to BGR': cv.COLOR_LAB2BGR,
                                'RGB to YUV': cv.COLOR_RGB2YUV,
                                'YUV to RGB': cv.COLOR_YUV2RGB
                            }
                        }
                    }
                }
            },
            'Gaussian Blur': {
                'command': 'cv.GaussianBlur(image, (kernel_size, kernel_size), 0)',
                'number_parameters': 2,
                'condition': 'True',
                'gui': {
                    'slider': {
                        'number_slider': 1,
                        'slider0': {
                            'name': 'Kernel Size',
                            'variable_name': 'kernel_size',
                            'min_value': 1,
                            'max_value': 21,
                            'step':2,
                            'default_value': 3
                        }
                    },
                    'menu': {
                        'number_menu': 0
                    }
                }
            }
        }
    
    def get_parameters(self, transform_string):
        list = transform_string.split("_")
        for index, element in enumerate(list):
            list[index] = int(element) if element.isnumeric() else element
        return list

    def transform(self, item_before, item_current):
        img_array_to_transform = item_before.img_array
        transform_item = item_current.transformation_item

        # Creation variable for the command
        for index, (key, value) in enumerate(transform_item.parameters.items()):
            exec(str(key) +  "=" + str(value))
        
        image = img_array_to_transform
        img_arrays_transformed = eval(self.commands[transform_item.name]['command'])
        return img_arrays_transformed