from pipelineitem import PipelineItem

class TransformerManager():
    def __init__(self, main_window, pipeline):
        self.main_window = main_window
        self.pipeline = pipeline
        self.dict = {
            self.alert_colorchange: "Color Change",
            self.alert_gaussian_blur: "Gaussian Blur"
        }

    def alert_custom(self, string_transformation):
        """Add a string in "transformations" that represent the transformations of the pixmaps"""
        insert = self.main_window.btn_add_current.isChecked()
        is_current_last = len(self.pipeline)-1==self.main_window.index_current_img
        new_item = PipelineItem(None, string_transformation)
        if is_current_last:
            self.pipeline.append(new_item)
            self.main_window.index_current_img += 1
        elif insert:
            self.pipeline.insert(self.main_window.index_current_img, new_item)
        elif not insert:
            self.pipeline[self.main_window.index_current_img] = new_item
            self.main_window.index_current_img += 1
        self.pipeline.update_from_index(self.main_window.index_current_img)
        #TODO
        # self.main_window.refresh_upper_transformation()
        # self.main_window.update_image_show()
        self.main_window.update_transformation_buttons()
        print(string_transformation)


    def alert_colorchange(self):
        """Send a string to "alert_custom" that contains info about the new transformation"""
        self.alert_custom("colorchange_RGB2GRAY")

    def alert_gaussian_blur(self):
        """Send a string to "alert_custom" that contains info about the new transformation"""
        self.alert_custom("gaussianblur_default")
