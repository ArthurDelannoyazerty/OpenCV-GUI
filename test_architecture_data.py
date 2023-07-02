import cv2 as cv

test = {
    'DRAWING - Line': {
        'command': 'cv.line(image, (x_begin, y_begin), (x_end, y_end), (red, green, blue), thickness)',
        'number_parameters': 9,
        'condition': 'len(image.shape)==3 and image.shape[2]==3',
        'gui': {
            'slider': {
                'number_slider': 8,
                'slider0': {
                    'name': 'X Begin',
                    'variable_name': 'x_begin',
                    'min_value': '0',
                    'max_value': 'len(image[0])-1',
                    'step':'1',
                    'default_value': '0'
                },
                'slider1': {
                    'name': 'Y Begin',
                    'variable_name': 'y_begin',
                    'min_value': '0',
                    'max_value': 'len(image)-1',
                    'step':'1',
                    'default_value': '0'
                },
                'slider2': {
                    'name': 'X End',
                    'variable_name': 'x_end',
                    'min_value': '0',
                    'max_value': 'len(image[0])-1',
                    'step':'1',
                    'default_value': 'len(image[0])-1'
                },
                'slider3': {
                    'name': 'Y End',
                    'variable_name': 'y_end',
                    'min_value': '0',
                    'max_value': 'len(image)-1',
                    'step':'1',
                    'default_value': 'len(image)-1'
                },
                'slider4': {
                    'name': 'Red',
                    'variable_name': 'red',
                    'min_value': '0',
                    'max_value': '255',
                    'step':'1',
                    'default_value': '127'
                },
                'slider5': {
                    'name': 'Green',
                    'variable_name': 'green',
                    'min_value': '0',
                    'max_value': '255',
                    'step':'1',
                    'default_value': '0'
                },
                'slider6': {
                    'name': 'Blue',
                    'variable_name': 'blue',
                    'min_value': '0',
                    'max_value': '255',
                    'step':'1',
                    'default_value': '0'
                },
                'slider7': {
                    'name': 'Thickness',
                    'variable_name': 'thickness',
                    'min_value': '1',
                    'max_value': '25',
                    'step':'1',
                    'default_value': '3'
                }
            },
            'menu': {
                'number_menu': 0
            }
        }
    },
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
                        'RGB to BGR': cv.COLOR_RGB2BGR,
                        'RGB to HSV': cv.COLOR_RGB2HSV,
                        'RGB to YUV': cv.COLOR_RGB2YUV,
                        'RGB to LAB': cv.COLOR_RGB2LAB,
                        'BGR to RGB': cv.COLOR_BGR2RGB,
                        'BGR to HSV': cv.COLOR_BGR2HSV,
                        'BGR to YUV': cv.COLOR_BGR2YUV,
                        'BGR to LAB': cv.COLOR_BGR2LAB,
                        'HSV to RGB': cv.COLOR_HSV2RGB,
                        'HSV to BGR': cv.COLOR_HSV2BGR,
                        'HSV to BGR': cv.COLOR_HSV2BGR,
                        'YUV to RGB': cv.COLOR_YUV2RGB,
                        'YUV to BGR': cv.COLOR_YUV2BGR,
                        'LAB to RGB': cv.COLOR_LAB2RGB,
                        'LAB to BGR': cv.COLOR_LAB2BGR
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
                    'min_value': '1',
                    'max_value': 'int(min(len(image[0]), len(image))/2)',
                    'step':'2',
                    'default_value': '3'
                }
            },
            'menu': {
                'number_menu': 0
            }
        }
    }
}