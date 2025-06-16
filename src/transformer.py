import cv2 as cv        # used in eval()
import numpy as np      # used in eval()
import json
from qtpy.QtWidgets import QMessageBox

class Transformer():
    """An objet that transform a given image with the specified transformation with opencv"""
    def __init__(self):
        #load commands
        try:
            with open('commands.json', 'r') as file:
                self.commands = json.load(file)
            # Evaluate menu item values such as cv constants
            for command in self.commands.values():
                menus = command.get('gui', {}).get('menu', {})
                for i in range(menus.get('number_menu', 0)):
                    menu = menus.get('menu'+str(i), {})
                    items = menu.get('menu_item', {})
                    for k, v in items.items():
                        if isinstance(v, str) and (v.startswith('cv.') or v.startswith('np.')):
                            items[k] = eval(v)
        except Exception:
            # Create a QMessageBox
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("Error while loading commands (commands.json), either file not found or error in parsing file. Please reboot the program")

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
        local_vars = {'image':image}
        for index, (key, value) in enumerate(transform_item.parameters.items()):
            local_vars[str(key)] = value
        
        # Execute command
        result = eval(self.commands[transform_item.name]['command'], locals=local_vars, globals=globals())

        # If command return a tuple, we take the second item (used in the threshold case shere the second item is the threshold image)
        if type(result).__name__=="tuple":
            result = result[1]
        return result.copy()
    
