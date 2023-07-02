import sys
from PySide6.QtWidgets import QApplication, QCheckBox, QMainWindow, QRadioButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QFileDialog, QWidget, QScrollArea
from PySide6.QtGui import Qt
from PySide6.QtCore import Qt, QSize
import cv2 as cv
from pathlib import Path
import numpy as np

from transformermanager import TransformerManager
from transformer import Transformer
from clickableframe import ClickableFrame
from pipelineitem import PipelineItem
from pipeline import Pipeline
from sliderwithtext import SliderWithText
from menuwithtext import MenuWithText

WIDTH_RIGHT_FRAME = 200
HEIGHT_UPPER_FRAME = 170
HEIGHT_TILES = HEIGHT_UPPER_FRAME - 60
WIDTH_TILES = 150
PADDING_HEIGHT_MAIN_IMAGE = 60
PADDING_WIDTH_MAIN_IMAGE = 20

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_parameters_widget = []

        self.transformer = Transformer()
        self.pipeline = Pipeline(self.transformer)
        self.transformer_manager = TransformerManager(self, self.pipeline, self.transformer)
        self.index_current_img = -1

        self.setGeometry(100, 100, 700, 700)
        self.initiate_frames()
        self.resizeEvent = self.resize_main_image_event

    def initiate_frames(self):
        """Create the main QFrame"""

        # Upper Frame --------------------------------------------------------------------
        upper_frame = QFrame()
        upper_frame.setFrameShape(QFrame.StyledPanel)
        upper_frame.setFixedHeight(HEIGHT_UPPER_FRAME)

        upper_layout = QVBoxLayout(upper_frame)

        scroll_area_pipeline = QScrollArea()
        scroll_area_pipeline.setWidgetResizable(True)
        upper_layout.addWidget(scroll_area_pipeline)

        container_upper_widget = QWidget(scroll_area_pipeline)
        self.container_upper_layout = QHBoxLayout(container_upper_widget)
        scroll_area_pipeline.setWidget(container_upper_widget)

        # Lower Frame --------------------------------------------------------------------
        lower_frame = QFrame()
        lower_frame.setFrameShape(QFrame.StyledPanel)
        lower_layout = QHBoxLayout(lower_frame)
        
        # ----- Left frame  --------------------------------------------------------------
        self.image_frame = QFrame()
        image_frame_layout = QVBoxLayout(self.image_frame)
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMinimumSize(1, 1)
        image_frame_layout.addWidget(self.image)
        self.image_frame.hide()

        self.import_button = QPushButton("Import Image")
        self.import_button.clicked.connect(self.open_image_dialog)

        # -----|-------- Description image frame------------------------------------------
        self.description_image_frame = QFrame()
        self.description_image_frame.setMaximumHeight(35)
        self.description_image_layout = QHBoxLayout(self.description_image_frame)
        self.description_image_layout.setAlignment(Qt.AlignRight)
        image_frame_layout.addWidget(self.description_image_frame)

        label_checkbox_show_last = QLabel()
        label_checkbox_show_last.setText("Show last")
        label_checkbox_show_last.setFixedWidth(50)
        self.description_image_layout.addWidget(label_checkbox_show_last)

        self.button_show_last_image = QCheckBox()
        self.button_show_last_image.hide()
        self.button_show_last_image.setFixedWidth(30)
        self.button_show_last_image.clicked.connect(self.update_image_show)
        self.description_image_layout.addWidget(self.button_show_last_image)

        self.image_shape_label = QLabel()
        # self.image_shape_label.setFixedHeight(15)
        self.description_image_layout.addWidget(self.image_shape_label)
        

        # ----- Middle frame  --------------------------------------------------------------
        pipeline_manage_frame = QFrame()
        pipeline_manage_frame.setFrameShape(QFrame.StyledPanel)
        pipeline_manage_frame.setFixedWidth(WIDTH_RIGHT_FRAME)
        self.pipeline_manage_layout = QVBoxLayout(pipeline_manage_frame)

        # ------|------ Mode manage ---------------------------------------------------------
        self.btn_delete_current_transformation = QPushButton(text="Delete transformation")
        self.btn_delete_current_transformation.clicked.connect(self.action_delete_current_transformation)
        self.btn_delete_current_transformation.hide()
        self.pipeline_manage_layout.addWidget(self.btn_delete_current_transformation)
        
        btn_change_current = QRadioButton("Change next")
        self.btn_add_after = QRadioButton("Add")
        self.btn_add_after.setChecked(True)
        self.frame_mode_manage = QFrame()
        self.frame_mode_manage.setFixedHeight(40)
        mode_manage_layout = QHBoxLayout(self.frame_mode_manage)
        mode_manage_layout.addWidget(btn_change_current)
        mode_manage_layout.addWidget(self.btn_add_after)

        self.frame_mode_manage.hide()
        self.pipeline_manage_layout.addWidget(self.frame_mode_manage)

        # ------|------ Buttons transformations available -----------------------------------
        scroll_area_transformation_pipeline = QScrollArea()
        scroll_area_transformation_pipeline.setWidgetResizable(True)
        self.pipeline_manage_layout.addWidget(scroll_area_transformation_pipeline)

        self.container_transformation_buttons_widget = QWidget(scroll_area_transformation_pipeline)
        self.container_transformation_buttons_layout = QVBoxLayout(self.container_transformation_buttons_widget)
        scroll_area_transformation_pipeline.setWidget(self.container_transformation_buttons_widget)
        
        # ----- Right frame  --------------------------------------------------------------
        transformation_parameters_frame = QFrame()
        transformation_parameters_frame.setFrameShape(QFrame.StyledPanel)
        transformation_parameters_frame.setFixedWidth(WIDTH_RIGHT_FRAME)
        self.transformation_parameters_layout = QVBoxLayout(transformation_parameters_frame)
        
        scroll_area_transformation_parameters = QScrollArea()
        scroll_area_transformation_parameters.setWidgetResizable(True)
        self.transformation_parameters_layout.addWidget(scroll_area_transformation_parameters)

        self.container_transformation_parameters = QWidget(scroll_area_transformation_parameters)
        self.container_transformation_parameters_layout = QVBoxLayout(self.container_transformation_parameters)
        scroll_area_transformation_parameters.setWidget(self.container_transformation_parameters)

        # ----
        lower_layout.addWidget(self.image_frame)
        lower_layout.addWidget(self.import_button)
        lower_layout.addWidget(pipeline_manage_frame)
        lower_layout.addWidget(transformation_parameters_frame)

        # Main Frame --------------------------------------------------------------------
        central_widget = QFrame()
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(upper_frame)
        main_layout.addWidget(lower_frame)

        self.setCentralWidget(central_widget)

    def delete_all_from_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            layout.removeWidget(widget)
            widget.deleteLater()

    def update_transformation_parameters_frame(self):
        self.delete_all_from_layout(self.container_transformation_parameters_layout)

        if self.index_current_img==0:
            btn = QPushButton()
            btn.setText("Change Image")
            btn.clicked.connect(self.change_original_image)
            self.container_transformation_parameters_layout.addWidget(btn)
        else:
            self.current_parameters_widget = []

            name_current_transformation = self.pipeline[self.index_current_img].transformation_item.name
            command = self.transformer.commands[name_current_transformation]
            image = self.pipeline[self.index_current_img-1].img_array

            for i in range(command['gui']['slider']['number_slider']):
                slider_parameters = command['gui']['slider']['slider'+str(i)]
                slider_value = self.pipeline[self.index_current_img].transformation_item.parameters[slider_parameters['variable_name']]
                frame_slider = SliderWithText(image, slider_parameters, slider_value, self.value_changed_parameters)
                self.container_transformation_parameters_layout.addWidget(frame_slider)
                self.current_parameters_widget.append(frame_slider)
        
            for i in range(command['gui']['menu']['number_menu']):
                menu_parameters = command['gui']['menu']['menu'+str(i)]
                value_in_pipeline = self.pipeline[self.index_current_img].transformation_item.parameters[menu_parameters['variable_name']]
                list_values_menu = list(menu_parameters['menu_item'].values())
                index_in_menu = list_values_menu.index(value_in_pipeline)
                frame_menu = MenuWithText(menu_parameters, index_in_menu, self.value_changed_parameters)
                self.container_transformation_parameters_layout.addWidget(frame_menu)
                self.current_parameters_widget.append(frame_menu)
    
    def action_delete_current_transformation(self):
        self.pipeline.pop(self.index_current_img)
        self.index_current_img = min(self.index_current_img, len(self.pipeline)-1)
        if self.index_current_img!=0:
            self.pipeline.update_from_index(self.index_current_img)
        self.refresh_upper_transformation()
        self.update_image_show()
        self.update_transformation_buttons()
        self.update_transformation_parameters_frame()

            
    def value_changed_parameters(self):
        new_parameters = dict()
        for widget in self.current_parameters_widget:
            variable_name = widget.parameters['variable_name']
            value = widget.value
            new_parameters[variable_name] = value
        self.pipeline[self.index_current_img].transformation_item.parameters = new_parameters
        self.pipeline.update_from_index(self.index_current_img)
        self.refresh_upper_transformation()
        self.update_image_show()
        self.update_transformation_buttons()

    def change_original_image(self):
        img_array = self.open_image()
        self.pipeline[0].img_array = img_array
        if len(self.pipeline)>1:
            self.pipeline.update_from_index(1)
        self.refresh_upper_transformation()
        self.update_image_show()
        self.update_transformation_buttons()
        self.update_transformation_parameters_frame()



    def refresh_upper_transformation(self):
        """Update the pipeline of image at the top of the window"""
        self.delete_all_from_layout(self.container_upper_layout)

        for i in range(len(self.pipeline)):
            pixmap = self.pipeline[i].get_pixmap()
            frame = ClickableFrame(i)
            frame.setFixedSize(QSize(WIDTH_TILES, HEIGHT_TILES))
            frame.setFrameShape(QFrame.Box)
            frame.clicked.connect(self.frame_clicked)
            if i==self.index_current_img: 
                frame.setStyleSheet("background-color: green;")

            layout = QVBoxLayout(frame)

            pixmap_label = QLabel()
            pixmap_label.setPixmap(pixmap.scaled(WIDTH_TILES, HEIGHT_TILES, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(pixmap_label)

            transformation_item = self.pipeline[i].transformation_item
            text = str(i) + " : "
            if transformation_item==None:
                text += "Original Image"
            else:
                text += transformation_item.name
            index_label = QLabel(text)
            index_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(index_label)

            self.container_upper_layout.addWidget(frame)

    def frame_clicked(self, index):
        """Print a message (index) when clicking on the pipeline of images"""
        self.index_current_img = index
        self.refresh_upper_transformation()
        self.update_image_show()
        self.update_transformation_buttons()
        self.update_transformation_parameters_frame()

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        str_path, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

        if str_path:
            img_array = cv.imdecode(np.fromfile(str_path, dtype=np.uint8), cv.IMREAD_UNCHANGED)
            img_array = cv.cvtColor(img_array, cv.COLOR_BGR2RGB)
        return img_array

    def open_image_dialog(self):
        img_array = self.open_image()
        self.index_current_img = 0
        self.pipeline.append(PipelineItem(img_array))

        self.import_button.hide()
        self.image_frame.setHidden(False)
        self.button_show_last_image.setHidden(False)
        self.update_image_show()

        self.refresh_upper_transformation()
        self.frame_mode_manage.setHidden(False)
        self.update_transformation_buttons()  
        self.index_current_img = 0
        self.update_transformation_parameters_frame()

    def resize_main_image_event(self, event):
        """Change the size of the main image we the main window is resized"""
        if self.index_current_img == -1:
            return

        frame_height = self.image_frame.height() - PADDING_HEIGHT_MAIN_IMAGE   # magic number because of the margin of the parent QFrame
        frame_width = self.image_frame.width() - PADDING_WIDTH_MAIN_IMAGE

        if self.button_show_last_image.isChecked():
            index_image_to_show = len(self.pipeline)-1
        else:
            index_image_to_show = self.index_current_img
        pixmap = self.pipeline[index_image_to_show].get_pixmap()
        pixmap_ratio = pixmap.width() / pixmap.height()
        frame_ratio = frame_width / frame_height
    
        if pixmap_ratio > frame_ratio:
            scaled_pixmap = pixmap.scaledToWidth(frame_width, Qt.SmoothTransformation)
        else:
            scaled_pixmap = pixmap.scaledToHeight(frame_height, Qt.SmoothTransformation)

        self.image.setPixmap(scaled_pixmap)
        self.image.setAlignment(Qt.AlignCenter)

        super().resizeEvent(event)

    def update_image_show(self):
        """Show the main image based on the "index_current_img" """
        if self.index_current_img<0 or self.index_current_img>=len(self.pipeline):
            raise Exception("Wrong index to update pipeline, index sent : " + str(self.index_current_img) + ". Valid index : [0, "+ str(len(self.pipeline)) + "]")
        
        if self.button_show_last_image.isChecked():
            index_image_to_show = len(self.pipeline)-1
        else:
            index_image_to_show = self.index_current_img
        shape = self.pipeline[index_image_to_show].img_array.shape
        split_shape_values = str(shape).replace("(","").replace(")","").split(", ")
        text_dimension = "h : " + split_shape_values[0] + ", w : " + split_shape_values[1]
        if len(split_shape_values)==3:
            text_dimension += ", c : " + split_shape_values[2]
        self.image_shape_label.setText(text_dimension)

        self.resize_main_image_event(None)
    
    def update_transformation_buttons(self):
        self.delete_all_from_layout(self.container_transformation_buttons_layout)

        self.btn_delete_current_transformation.setHidden(self.index_current_img==0)

        list_transformation = list(self.transformer.commands.keys())
        for index, transformation in enumerate(list_transformation):
            condition_str = self.transformer.commands[transformation]['condition']
            image = self.pipeline[self.index_current_img].img_array             # used for eval(condition)
            if eval(condition_str):
                button = QPushButton(transformation)
                button.clicked.connect(self.transformer_manager.list_function_transformation[index])
                self.container_transformation_buttons_layout.addWidget(button)
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
