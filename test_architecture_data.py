import cv2 as cv
command_dict = {
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
                            'name': 'Choose the conversion',
                            'variable_name': 'colorspace_mode',
                            'menu_item':[
                                ('Grayscale',  cv.COLOR_BGR2GRAY),
                                ('HSV to RGB', cv.COLOR_HSV2RGB),
                                ('LAB to RGB', cv.COLOR_LAB2RGB),
                                ('BGR to RGB', cv.COLOR_BGR2RGB),
                                ('RGB to BGR', cv.COLOR_RGB2BGR),
                                ('BGR to HSV', cv.COLOR_BGR2HSV),
                                ('HSV to BGR', cv.COLOR_HSV2BGR),
                                ('BGR to LAB', cv.COLOR_BGR2LAB),
                                ('LAB to BGR', cv.COLOR_LAB2BGR),
                                ('RGB to YUV', cv.COLOR_RGB2YUV),
                                ('YUV to RGB', cv.COLOR_YUV2RGB)
                            ]
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


for i in range(1):
    exec('a=1')


print(a)


# print(list(command_dict.keys())[0])

# img = cv.imread('img_test.png')
# cv.imshow('origin', img)
# cv.waitKey()

# image = img
# print(len(image.shape)==3 and image.shape[2]==3)

# option = command_dict['Change Colorspace']['gui']['menu']['menu1']['menu_item'][0][1]
# # print(option)
# colorspace_mode = option

# command = command_dict['Change Colorspace']['command']
# # print(command)

# img_out = eval(command)
# # print(img_out)
# cv.imshow("out", img_out)
# cv.waitKey()