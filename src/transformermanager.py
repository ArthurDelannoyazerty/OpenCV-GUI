from pipelineitem import PipelineItem
from transformationitem import TransformationItem


class TransformerManager():
    """Manage the events and modify the transformation in pipeline"""
    def __init__(self, main_window, pipeline, transformer):
        self.main_window = main_window
        self.pipeline = pipeline
        self.transformer = transformer
        
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
            if isinstance(default_value, str):
                default_value = eval(default_value)
            dict_default_values[var_name] = default_value
        
        return dict_default_values