import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QFileDialog, QWidget, QScrollArea
from PySide6.QtGui import QPixmap, Qt, QImage
from PySide6.QtCore import Qt, QSize
import cv2 as cv

from transformermanager import TransformerManager
from transformer import Transformer
from clickableframe import ClickableFrame
from pipelineitem import PipelineItem
from pipeline import Pipeline

WIDTH_RIGHT_FRAME = 200
HEIGHT_UPPER_FRAME = 150
HEIGHT_TILES = HEIGHT_UPPER_FRAME - 50
WIDTH_TILES = 150

# TODO actions transformers

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
        frame2_layout = QHBoxLayout(lower_frame)
        
        # ----- Left frame  --------------------------------------------------------------
        self.image_frame = QFrame()
        image_frame_layout = QVBoxLayout(self.image_frame)
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMinimumSize(1, 1)
        image_frame_layout.addWidget(self.image)
        self.image_frame.hide()

        self.image_shape_label = QLabel()
        self.image_shape_label.setFixedHeight(15)
        image_frame_layout.addWidget(self.image_shape_label)
        
        self.import_button = QPushButton("Import Image")
        self.import_button.clicked.connect(self.open_image_dialog)

        # ----- Middle frame  --------------------------------------------------------------
        pipeline_manage_frame = QFrame()
        pipeline_manage_frame.setFrameShape(QFrame.StyledPanel)
        pipeline_manage_frame.setFixedWidth(WIDTH_RIGHT_FRAME)
        self.pipeline_manage_layout = QVBoxLayout(pipeline_manage_frame)

        # ------|------ Mode manage ---------------------------------------------------------
        btn_change_current = QRadioButton("Change After")
        btn_change_current.setChecked(True)
        self.btn_add_current = QRadioButton("Add")
        self.frame_mode_manage = QFrame()
        self.frame_mode_manage.setFixedHeight(40)
        mode_manage_layout = QHBoxLayout(self.frame_mode_manage)
        mode_manage_layout.addWidget(btn_change_current)
        mode_manage_layout.addWidget(self.btn_add_current)

        self.frame_mode_manage.hide()
        self.pipeline_manage_layout.addWidget(self.frame_mode_manage)

        # ------|------ Buttons transformations available -----------------------------------
        scroll_area_transformation_pipeline = QScrollArea()
        scroll_area_transformation_pipeline.setWidgetResizable(True)
        self.pipeline_manage_layout.addWidget(scroll_area_transformation_pipeline)

        self.container_transformation_buttons_widget = QWidget(scroll_area_transformation_pipeline)
        self.pipeline_manage_layout = QVBoxLayout(self.container_transformation_buttons_widget)
        scroll_area_transformation_pipeline.setWidget(self.container_transformation_buttons_widget)
        
        # ----- Right frame  --------------------------------------------------------------
        transformation_manage_frame = QFrame()
        transformation_manage_frame.setFrameShape(QFrame.StyledPanel)
        transformation_manage_frame.setFixedWidth(WIDTH_RIGHT_FRAME)
        self.transformation_manage_layout = QVBoxLayout(transformation_manage_frame)


        frame2_layout.addWidget(self.image_frame)
        frame2_layout.addWidget(self.import_button)
        frame2_layout.addWidget(pipeline_manage_frame)
        frame2_layout.addWidget(transformation_manage_frame)

        # Main Frame --------------------------------------------------------------------
        central_widget = QFrame()
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(upper_frame)
        main_layout.addWidget(lower_frame)

        self.setCentralWidget(central_widget)

    def refresh_upper_transformation(self):
        """Update the pipeline of image at the top of the window"""
        # Find and delete the initial buttons
        for i in reversed(range(self.container_upper_layout.count())):
            item = self.container_upper_layout.itemAt(i)
            if isinstance(item.widget(), ClickableFrame):
                button = item.widget()
                self.container_upper_layout.removeWidget(button)
                button.deleteLater()

        for i in range(len(self.pipeline)):
            pixmap = self.pipeline[i].get_pixmap()
            frame = ClickableFrame(i)
            frame.setFixedSize(QSize(WIDTH_TILES, HEIGHT_TILES))
            frame.setFrameShape(QFrame.Box)
            frame.clicked.connect(self.frame_clicked)
            if i==self.index_current_img : frame.setStyleSheet("background-color: green;")

            layout = QVBoxLayout(frame)

            pixmap_label = QLabel()
            pixmap_label.setPixmap(pixmap.scaled(WIDTH_TILES, HEIGHT_TILES, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(pixmap_label)

            index_label = QLabel(f"Index: {i}")
            index_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(index_label)

            self.container_upper_layout.addWidget(frame)

    def frame_clicked(self, index):
        """Print a message (index) when clicking on the pipeline of images"""
        print(f"Frame clicked: {index}")

    def open_image_dialog(self):
        """Open a Choose File dialog box to choose the image"""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

        if file_name:
            img_array = cv.imread(file_name, cv.IMREAD_COLOR)
            img_array = cv.cvtColor(img_array, cv.COLOR_BGR2RGB)
            self.index_current_img = 0
            self.pipeline.append(PipelineItem(img_array))
            self.update_image_show()

            self.import_button.hide()
            self.image_frame.setHidden(False)
            self.resize_main_image_event(None)

            self.refresh_upper_transformation()
            self.frame_mode_manage.setHidden(False)
            self.update_transformation_buttons()  
            self.index_current_img = 0

    def resize_main_image_event(self, event):
        """Change the size of the main image we the main window is resized"""
        if self.index_current_img == -1:
            return

        frame_height = self.image_frame.height() - 20   # magic number because of the margin of the parent QFrame
        frame_width = self.image_frame.width() - 20

        pixmap = self.get_current_pixmap()
        pixmap_ratio = pixmap.width() / pixmap.height()
        frame_ratio = frame_width / frame_height
    
        if pixmap_ratio > frame_ratio:
            scaled_pixmap = pixmap.scaledToWidth(frame_width, Qt.SmoothTransformation)
        else:
            scaled_pixmap = pixmap.scaledToHeight(frame_height, Qt.SmoothTransformation)

        self.image.setPixmap(scaled_pixmap)
        self.image.setAlignment(Qt.AlignCenter)

        super().resizeEvent(event)
    
    def get_current_pixmap(self):
        return self.pipeline[self.index_current_img].get_pixmap()

    def update_image_show(self):
        """Show the main image based on the "index_current_img" """
        if self.index_current_img<0 or self.index_current_img>=len(self.pipeline):
            raise Exception("Wrong index to update pipeline, index sent : " + str(self.index_current_img) + ". Valid index : [0, "+ str(len(self.pipeline)) + "]")
        pixmap = self.get_current_pixmap()
        self.image.setPixmap(pixmap.scaledToWidth(self.image_frame.width(), Qt.SmoothTransformation))
        self.image.setAlignment(Qt.AlignCenter)

        text_dimension = str(self.pipeline[self.index_current_img].img_array.shape).replace("(","").replace(")","").split(", ")
        text_dimension = "h : " + text_dimension[0] + ", w : " + text_dimension[1] + ", c : " + text_dimension[2]
        self.image_shape_label.setText(text_dimension)
    
    def update_transformation_buttons(self):
        # Find and delete the initial buttons
        for i in reversed(range(self.pipeline_manage_layout.count())):
            item = self.pipeline_manage_layout.itemAt(i)
            if isinstance(item.widget(), QPushButton):
                button = item.widget()
                self.pipeline_manage_layout.removeWidget(button)
                button.deleteLater()

        list_transformation = list(self.transformer.commands.keys())
        for index, transformation in enumerate(list_transformation):
            condition_str = self.transformer.commands[transformation]['condition']
            image = self.pipeline[self.index_current_img].img_array             # used for eval(condition)
            if eval(condition_str):
                button = QPushButton(transformation)
                button.clicked.connect(self.transformer_manager.list_function_transformation[index])
                self.pipeline_manage_layout.addWidget(button)
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
