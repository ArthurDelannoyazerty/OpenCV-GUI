# OpenCV-GUI
A graphical interface for the OpenCV functions and more. This let you create interactively a pipeline of transformation for the seleted image. 

# Getting started
Just download the latest release and execute the *.exe* file. Make sure that the *commands.txt* file is in the same directory as the *.exe* file (You can create a shortcut by right clicking).

# Want to help the project ?
You can clone or fork the repo as you wish. The pulls request still need the approval of the admin for security.

# Questions/Issue ?
Don't hesitate to ask in the github page of this project.

# GUI explanation

![GUI Explained](assets/gui_explained.jpg)

# Command file
The command file located in the same directory as the *.exe* file contains all the functions that transform the image. 

This file is made to be modified by the user if needed. For now the code still need to be modified by hand for each new transformation that the user add. The user can still modify the current transforamtions. There is a particular structure that needs to be followed. 

This file contains a series of nested python dictionnary that provide information about how the image is transformed, with which parameters and at what condition. Because of the nature of Python dictionnaries, each name must be differents from another in the same level of dictionnaries

Here is the structure :

```python
{
    (string)'Name-of-the-transformation': {
        'command': (string)'Command-to-transform-"image"(using "cv" or "np")',
        'number_parameters': (int)number-of-parameters("image" included),
        'condition': (boolean)condition-on-image-to-make-the-transformation-appear-in-the-gui,
        'gui': {
            'slider': {
                'number_slider': (int)number-of-parameter-needing-slider,
                'slider0': {
                    'name': (string)'name-of-the-parameters(user)',
                    'variable_name': (string)'name-of-the-parameters(to put in the "command")',
                    'min_value': (string)'min-value-of-the-slider(condition with "image" possible)',
                    'max_value': (string)'max-value-of-the-slider(condition with "image" possible)',
                    'step': (string)'step-of-the-slider (no tests, working for 1 and 2)',
                    'default_value': (string)'default-value-of-the-slider(condition with "image" possible)'
                },
                'slider1': {
                    'name': (string)'name-of-the-parameters(user)',
                    'variable_name': (string)'name-of-the-parameters(to put in the "command")',
                    'min_value': (string)'min-value-of-the-slider(condition with "image" possible)',
                    'max_value': (string)'max-value-of-the-slider(condition with "image" possible)',
                    'step': (string)'step-of-the-slider (no tests, working for 1 and 2)',
                    'default_value': (string)'default-value-of-the-slider(condition with "image" possible)'
                }
            },
            'menu': {
                'number_menu': (int)number-of-parameter-needing-menu,
                'menu0': {
                    'name': (string)'name-of-the-parameters(user)',
                    'variable_name': 'name-of-the-parameters(to put in the "command")',
                    'menu_item':{
                        (string)'Name-of-the-option(user)': (int)value-of-the-option,
                        (string)'Name-of-the-option(user)': (int)value-of-the-option
                    }
                }
            }
        }
    },
    # Other transformations ...
}
```