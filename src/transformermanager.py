from pipelineitem import PipelineItem
from transformationitem import TransformationItem
from PySide6.QtWidgets import QApplication, QMessageBox


class TransformerManager():
    """Manage the events and modify the transformation in pipeline"""
    def __init__(self, main_window, pipeline, transformer):
        self.main_window = main_window
        self.pipeline = pipeline
        self.transformer = transformer
        self.list_function_transformation = [   # Used from main.py to connect to the transformation button to the right function below
            self.alert_draw_line,
            self.alert_draw_rectangle,
            self.alert_draw_circle,
            self.alert_draw_ellipse,
            self.alert_crop,
            self.alert_rotation_zoom,
            self.alert_select_channel,
            self.alert_colorspacechange,
            self.alert_simple_blur,
            self.alert_gaussian_blur,
            self.alert_median_blur,
            self.alert_bilateral_filtering,
            self.alert_luminosity_contrast,
            self.alert_gaussian_noise,
            self.alert_salt_pepper_noise,
            self.alert_poisson_noise,
            self.alert_speckle_noise,
            self.alert_filter2d,
            self.alert_threshold1d,
            self.alert_adaptive_threshold1d,
            self.alert_gradient_laplacian,
            self.alert_gradient_sobel,
            self.alert_gradient_canny,
            self.alert_morph
        ]
        
    def transformation_saver(self, key_command):
        """Modify the transformation in pipeline"""
        dict_parameters = self.get_default_transformation_parameters(key_command)
        transformation_item = TransformationItem(key_command, dict_parameters)
        new_item = PipelineItem(None, transformation_item)

        add_after = self.main_window.btn_add_after.isChecked()
        is_current_last = len(self.pipeline)-1==self.main_window.index_current_img
        self.main_window.index_current_img += 1
        if is_current_last:
            self.pipeline.append(new_item)
        elif add_after:
            self.pipeline.insert(self.main_window.index_current_img, new_item)
        elif not add_after:
            save_old_item = self.pipeline[self.main_window.index_current_img]
            self.pipeline[self.main_window.index_current_img] = new_item

        try:
            self.pipeline.update_from_index(self.main_window.index_current_img)
        except:
            if is_current_last:
                self.pipeline.pop()
            elif add_after:
                self.pipeline.pop(self.main_window.index_current_img)
            elif not add_after:
                self.pipeline[self.main_window.index_current_img] = save_old_item
            
            self.main_window.index_current_img -= 1
            self.pipeline.update_from_index()
        self.main_window.update_all_qframes()
    
    def get_default_transformation_parameters(self, key_command):
        """Return a dict with default transformation values"""
        dict_gui = self.transformer.commands[key_command]['gui']
        dict_default_values = dict()

        image = self.pipeline[self.main_window.index_current_img].img_array     #used in eval()
        
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

# All these functions takes the main name of the commands file and send it to the 'transformation_saver' method

    def alert_draw_line(self):
        key_command = list(self.main_window.transformer.commands.keys())[0]
        self.transformation_saver(key_command)
    
    def alert_draw_rectangle(self):
        key_command = list(self.main_window.transformer.commands.keys())[1]
        self.transformation_saver(key_command)
    
    def alert_draw_circle(self):
        key_command = list(self.main_window.transformer.commands.keys())[2]
        self.transformation_saver(key_command)
    
    def alert_draw_ellipse(self):
        key_command = list(self.main_window.transformer.commands.keys())[3]
        self.transformation_saver(key_command)
    
    def alert_crop(self):
        key_command = list(self.main_window.transformer.commands.keys())[4]
        self.transformation_saver(key_command)
    
    def alert_rotation_zoom(self):
        key_command = list(self.main_window.transformer.commands.keys())[5]
        self.transformation_saver(key_command)
    
    def alert_select_channel(self):
        key_command = list(self.main_window.transformer.commands.keys())[6]
        self.transformation_saver(key_command)

    def alert_colorspacechange(self):
        key_command = list(self.main_window.transformer.commands.keys())[7]
        self.transformation_saver(key_command)

    def alert_simple_blur(self):
        key_command = list(self.main_window.transformer.commands.keys())[8]
        self.transformation_saver(key_command)

    def alert_gaussian_blur(self):
        key_command = list(self.main_window.transformer.commands.keys())[9]
        self.transformation_saver(key_command)

    def alert_median_blur(self):
        key_command = list(self.main_window.transformer.commands.keys())[10]
        self.transformation_saver(key_command)

    def alert_bilateral_filtering(self):
        key_command = list(self.main_window.transformer.commands.keys())[11]
        self.transformation_saver(key_command)

    def alert_luminosity_contrast(self):
        key_command = list(self.main_window.transformer.commands.keys())[12]
        self.transformation_saver(key_command)

    def alert_gaussian_noise(self):
        key_command = list(self.main_window.transformer.commands.keys())[13]
        self.transformation_saver(key_command)

    def alert_salt_pepper_noise(self):
        key_command = list(self.main_window.transformer.commands.keys())[14]
        self.transformation_saver(key_command)

    def alert_poisson_noise(self):
        key_command = list(self.main_window.transformer.commands.keys())[15]
        self.transformation_saver(key_command)

    def alert_speckle_noise(self):
        key_command = list(self.main_window.transformer.commands.keys())[16]
        self.transformation_saver(key_command)

    def alert_filter2d(self):
        key_command = list(self.main_window.transformer.commands.keys())[17]
        self.transformation_saver(key_command)

    def alert_threshold1d(self):
        key_command = list(self.main_window.transformer.commands.keys())[18]
        self.transformation_saver(key_command)

    def alert_adaptive_threshold1d(self):
        key_command = list(self.main_window.transformer.commands.keys())[19]
        self.transformation_saver(key_command)

    def alert_gradient_laplacian(self):
        key_command = list(self.main_window.transformer.commands.keys())[20]
        self.transformation_saver(key_command)

    def alert_gradient_sobel(self):
        key_command = list(self.main_window.transformer.commands.keys())[21]
        self.transformation_saver(key_command)

    def alert_gradient_canny(self):
        key_command = list(self.main_window.transformer.commands.keys())[22]
        self.transformation_saver(key_command)

    def alert_morph(self):
        key_command = list(self.main_window.transformer.commands.keys())[23]
        self.transformation_saver(key_command)
