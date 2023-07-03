import cv2 as cv        # used in eval()
import numpy as np      # used in eval()
from PySide6.QtWidgets import QMessageBox

class Transformer():
    """An objet that transform a given image with the specified transformation with opencv"""
    def __init__(self):
        #load commands
        try:
            with open('commands.txt', 'r') as file:
                file_content = file.read()
            file_content = file_content.replace("\n", "")
            self.commands = eval(file_content)
        except:
            # Create a QMessageBox
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("Error while loading commands (commands.txt), either file not found or error in parsing file. Please reboot the program")

            # Set the message box icon and buttons
            message_box.setIcon(QMessageBox.Critical)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
            raise SyntaxError("Error while loading commands, either file not found or error in parsing file.")
            
    def transform(self, item_before, item_current):
        """Transform the image from item_before with the transformation item of item_current"""
        img_array_to_transform = item_before.img_array
        image = img_array_to_transform.copy()
        transform_item = item_current.transformation_item

        # Creation variables for the command
        for index, (key, value) in enumerate(transform_item.parameters.items()):
            exec(str(key) +  "=" + str(value))
        
        # Execute command
        result = eval(self.commands[transform_item.name]['command'])

        # If command return a tuple, we take the second item (used in the threshold case shere the second item is the threshold image)
        if type(result).__name__=="tuple":
            result = result[1]
        return result.copy()
    
