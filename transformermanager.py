from pipelineitem import PipelineItem
from transformationitem import TransformationItem
from PySide6.QtWidgets import QApplication, QMessageBox


class TransformerManager():
    def __init__(self, main_window, pipeline, transformer):
        self.main_window = main_window
        self.pipeline = pipeline
        self.transformer = transformer
        self.list_function_transformation = [
            self.alert_draw_line,
            self.alert_draw_rectangle,
            self.alert_draw_circle,
            self.alert_draw_ellipse,
            self.alert_crop,
            self.alert_select_channel,
            self.alert_colorspacechange,
            self.alert_gaussian_blur
        ]

    def transformation_saver(self, key_command):
        """Add a string in "transformations" that represent the transformations of the pixmaps"""
        dict_parameters = self.get_default_transformation_parameters(key_command)
        transformation_item = TransformationItem(key_command, dict_parameters)
        new_item = PipelineItem(None, transformation_item)

        add_after = self.main_window.btn_add_after.isChecked()
        is_current_last = len(self.pipeline)-1==self.main_window.index_current_img
        if is_current_last:
            self.pipeline.append(new_item)
            self.main_window.index_current_img += 1
        elif add_after:
            self.main_window.index_current_img += 1
            self.pipeline.insert(self.main_window.index_current_img, new_item)
        elif not add_after:
            self.pipeline[self.main_window.index_current_img+1] = new_item
            self.main_window.index_current_img += 1
        try:
            self.pipeline.update_from_index(self.main_window.index_current_img)
        except:
            # TODO undo the change if error in pipeline transformation
            # Create a QMessageBox
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("An error occurred in the pipeline, please reboot the program")

            # Set the message box icon and buttons
            message_box.setIcon(QMessageBox.Critical)
            message_box.setStandardButtons(QMessageBox.Ok)

            # Show the message box
            message_box.exec()
            raise Exception("An error occured in the pipeline, reboot the program.")
        self.main_window.refresh_upper_transformation()
        self.main_window.update_image_show()
        self.main_window.update_transformation_buttons()
        self.main_window.update_transformation_parameters_frame()
    
    def get_default_transformation_parameters(self, key_command):
        dict_gui = self.transformer.commands[key_command]['gui']
        dict_default_values = dict()

        image = self.pipeline[self.main_window.index_current_img].img_array
        
        for i in range(dict_gui['slider']['number_slider']):
            current_slider = dict_gui['slider']['slider'+str(i)]
            var_name = current_slider['variable_name']
            default_value = eval(current_slider['default_value'])
            dict_default_values[var_name] = default_value
        
        for i in range(dict_gui['menu']['number_menu']):
            current_slider = dict_gui['menu']['menu'+str(i)]
            var_name = current_slider['variable_name']
            default_value = list(current_slider['menu_item'].values())[0]
            dict_default_values[var_name] = default_value
        
        return dict_default_values



    def alert_draw_line(self):
        """Send a string to "transformation_saver" that contains info about the new transformation"""
        key_command = list(self.main_window.transformer.commands.keys())[0]
        self.transformation_saver(key_command)
    
    def alert_draw_rectangle(self):
        """Send a string to "transformation_saver" that contains info about the new transformation"""
        key_command = list(self.main_window.transformer.commands.keys())[1]
        self.transformation_saver(key_command)
    
    def alert_draw_circle(self):
        """Send a string to "transformation_saver" that contains info about the new transformation"""
        key_command = list(self.main_window.transformer.commands.keys())[2]
        self.transformation_saver(key_command)
    
    def alert_draw_ellipse(self):
        """Send a string to "transformation_saver" that contains info about the new transformation"""
        key_command = list(self.main_window.transformer.commands.keys())[3]
        self.transformation_saver(key_command)
    
    def alert_crop(self):
        """Send a string to "transformation_saver" that contains info about the new transformation"""
        key_command = list(self.main_window.transformer.commands.keys())[4]
        self.transformation_saver(key_command)
    
    def alert_select_channel(self):
        """Send a string to "transformation_saver" that contains info about the new transformation"""
        key_command = list(self.main_window.transformer.commands.keys())[5]
        self.transformation_saver(key_command)

    def alert_colorspacechange(self):
        """Send a string to "transformation_saver" that contains info about the new transformation"""
        key_command = list(self.main_window.transformer.commands.keys())[6]
        self.transformation_saver(key_command)

    def alert_gaussian_blur(self):
        """Send a string to "transformation_saver" that contains info about the new transformation"""
        key_command = list(self.main_window.transformer.commands.keys())[7]
        self.transformation_saver(key_command)
