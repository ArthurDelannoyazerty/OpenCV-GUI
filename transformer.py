import cv2 as cv
from PySide6.QtWidgets import QMessageBox

class Transformer():
    """An objet that transform a given image with the specified transforamtion with opencv"""
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