# OpenCV-GUI [![Downloads](https://img.shields.io/github/downloads/ArthurDelannoyazerty/OpenCV-GUI/total.svg)](https://github.com/ArthurDelannoyazerty/OpenCV-GUI/releases)
A graphical interface for the OpenCV functions and more. This let you create an interactive pipeline of transformation for the selected image. 

Do you want to rapidly apply transformations to an image ? This program is made for that ! 

You can test in all functions given by OpenCV and more with an instant refresh of the result image. All the parameters of each transformations can be easily and rapidly changed with user friendly UI. You can even change previous transformations while observing the change for the result image !

**You can export the pipeline of transformation to python code or download the selected image by just pressing a button !**

# Getting started
Just download the latest release and execute the *.exe* file. Make sure that the *commands.json* file is in the same directory as the *.exe* file.



# GUI explanation


https://github.com/ArthurDelannoyazerty/OpenCV-GUI/assets/28599212/4f96dabf-a022-48bc-90cf-75c474df6a60


![GUI Explained](assets/gui_explained.jpg)

# Transformations Available
_You can add yours easily if needed (see the section 'Command file')._

- Drawing
  - Line
  - Rectangle
  - Circle
  - Ellipse
- Crop
- Rotation & Zoom
- Countours
- Color
  - Select Channel (R/G/B)
  - Change Colorspace (Grayscale/BRG/HSV...)
  - Luminosity & Contrast
- Noise
  - Gaussian
  - Salt & Pepper (*)
  - Poisson (*)
  - Speckle (*)
- Blur
  - Simple
  - Gaussian
  - Median
  - Bilateral Filtering
- Custom 3x3 Convolution
- Thresh (*)
  - Simple (*)
  - Adaptative (*)
- Gradient (*)
  - Laplacian (*)
  - Sobel (*)
  - Canny (*)
- Morph (Dilate/Erosion...) (*)

_`(*)` means that this transformation is only available when the image have 1 depth (i.e the image is in grayscale). For that, you need to activate the transformation "Color - Colorspace(grayscale)" or "Color - Channel"._



# Want to help the project ?
You can clone or fork the repo as you wish. The pulls request still need the approval of the admin for security.



# Create the environment : 
This project now use the `uv` python virtual environment manager. When you clone the project you just need to have `uv` installed and execute the command :
```
uv sync
```


# Command file
The command file located in the same directory as the *.exe* file contains all the functions that transform the image. 

This file is made to be modified by the user if needed. There is a particular structure that needs to be followed. 

This file contains a series of nested python dictionnary that provide information about how the image is transformed, with which parameters and at what condition. Because of the nature of Python dictionnaries, each name must be differents from another in the same level of dictionnaries

The `'command'` field contains the function. This must be in 1 line of code. You have access to all python/numpy/opencv functions. The input is the previous image stored in the variable named `image`. The field must return an image in the type of a numpy array. This function line also receive the variables in the the `gui` fields; they have the name of the `variable_name` field and the value of the menu/slider in the gui.



Here is the structure :

```json
{
    "Name of the transformation": {
        "command": "<string>Command to transform the image",
        "number_parameters": "<int>Number of parameters ('image' included)",
        "condition": "<boolean>Condition on image to make the transformation appear in the GUI",
        "gui": {
            "slider": {
                "number_slider": "<int>number of parameter needing slider",
                "slider0": {
                    "name": "<string>name of the parameters diplayed on the GUI",
                    "variable_name": "<string>name of the parameters used in the 'command' field",
                    "min_value": "<string>min value of the slider (condition with 'image' possible)",
                    "max_value": "<string>max value of the slider (condition with 'image' possible)",
                    "step": "<string>step of the slider (no tests, working for 1 and 2)",
                    "default_value": "<string>default value of the slider (condition with 'image' possible)"
                },
                "slider1": {
                    "name": "<string>name of the parameters diplayed on the GUI",
                    "variable_name": "<string>name of the parameters (to put in the 'command')",
                    "min_value": "<string>min value of the slider (condition with 'image' possible)",
                    "max_value": "<string>max value of the slider (condition with 'image' possible)",
                    "step": "<string>step of the slider (no tests, working for 1 and 2)",
                    "default_value": "<string>default value of the slider (condition with 'image' possible)"
                }
            },
            "menu": {
                "number_menu": "<int>number of parameter needing menu",
                "menu0": {
                    "name": "<string>name of the parameters diplayed on the GUI",
                    "variable_name": "<string>name of the parameters (to put in the 'command')",
                    "menu_item":{
                        "Name of the option diplayed on the GUI": "<string>value of the option",
                        "Name of the option diplayed on the GUI": "<string>value of the option"
                    }
                }
            }
        }
    },
    # Other transformations ...
}
```

And here is an example :

```json
{
    "THRESH - Simple": {
        "command": "cv.threshold(image, thresh_value, max_value, thresh_type)",
        "number_parameters" : 4,            # 4 parameters : 1 image, 2 sliders, 1 menu 
        "condition": "len(image.shape)==2", # Only displayed if image in 1 dimension
        "gui":{
            "slider":{
                "number_slider": 2,
                "slider0": {
                    "name": "Thresh Value",             # visual name
                    "variable_name": "thresh_value",    # name used in "command"
                    "min_value": "0",
                    "max_value": "255",
                    "step":"1",
                    "default_value": "128"
                },
                "slider1": {
                    "name": "Max Value",
                    "variable_name": "max_value",
                    "min_value": "0",
                    "max_value": "255",
                    "step":"1",
                    "default_value": "255"
                }
            },
            "menu":{
                "number_menu": 1,
                "menu0": {
                    "name": "Threshold Type",
                    "variable_name": "thresh_type",
                    "menu_item":{
                        "Binary" : "cv.THRESH_BINARY",
                        "Binary Inverted": "cv.THRESH_BINARY_INV",
                        "Truncate": "cv.THRESH_TRUNC",
                        "To Zero": "cv.THRESH_TOZERO",
                        "To Zero Inverted": "cv.THRESH_TOZERO_INV",
                        "Otsu": "cv.THRESH_OTSU"
                    }
                }
            }
        }
    }, ...# Other transformations ...
}
```



# Questions/Issue ?
Don't hesitate to ask in the github page of this project.
