import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QFileDialog, QWidget, QScrollArea
from PySide6.QtGui import QPixmap, Qt, QImage
from PySide6.QtCore import Qt, QSize, Signal
import cv2 as cv

WIDTH_RIGHT_FRAME = 200
HEIGHT_UPPER_FRAME = 150
HEIGHT_TILES = HEIGHT_UPPER_FRAME - 50
WIDTH_TILES = 150

# TODO actions transformers

class Transformer():
    """An objet that transform a given image with the specified transforamtion with opencv"""
    def __init__(self):
        self.dict_func_opencv = {
                "gaussianblur" : cv.GaussianBlur,
                "colorchange" : cv.cvtColor
            }
    
    def get_parameters(transform_string):
        list = transform_string.split("_")
        for index, element in enumerate(list):
            list[index] = int(element) if element.isnumeric() else element

    
    def transform(self, img_array, transform_string):
        print("transform")
        parameters = self.get_parameters(transform_string)
        img_arrays_transformed =  self.dict_func_opencv.get(parameters[0], lambda: 'Invalid')(img_array, *parameters[1:])
        return img_arrays_transformed

class ClickableFrame(QFrame):
    """pipeline object"""
    clicked = Signal(int)

    def __init__(self, index):
        super().__init__()
        self.index = index

    def mousePressEvent(self, event):
        self.clicked.emit(self.index)

class PipelineItem():
    def __init__(self, img_array, str_transformation=""):
        self.img_array = img_array
        self.str_transformation = str_transformation
    
    def get_pixmap(self):
        height, width, channel = self.img_array.shape
        bytes_per_line = channel * width
        qimage = QImage(self.img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap
    
    def execute_transform(self, transform_object):
        transform_object.transform(self.img_array, self.str_transformation)

class Pipeline(list):
    def __init__(self, transformer):
        self.transformer = transformer

    def update_from_index(self, index=1):
        if index<1 or index>=len(self):
            raise Exception("Wrong index to update pipeline, index sent : " + str(index) + ". Valid index : [1, "+ str(len(self)) + "]")
        for index in range(index, len(self)):
            item = self[index-1]
            self[index] = item.execute_transform(self.transformer)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.transformer = Transformer()
        self.pipeline = Pipeline(self.transformer)
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

        layout_frame1 = QHBoxLayout(upper_frame)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout_frame1.addWidget(self.scroll_area)

        container_upper_widget = QWidget(self.scroll_area)
        self.container_upper_layout = QVBoxLayout(container_upper_widget)
        self.scroll_area.setWidget(container_upper_widget)

        # Lower Frame --------------------------------------------------------------------
        lower_frame = QFrame()
        lower_frame.setFrameShape(QFrame.StyledPanel)
        frame2_layout = QHBoxLayout(lower_frame)
        
        self.image_frame = QFrame()
        image_frame_layout = QVBoxLayout(self.image_frame)
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMinimumSize(1, 1)
        image_frame_layout.addWidget(self.image)
        self.image_frame.hide()
        
        self.import_button = QPushButton("Import Image")
        self.import_button.clicked.connect(self.open_image_dialog)

        pipeline_manage_layout = QFrame()
        pipeline_manage_layout.setFrameShape(QFrame.StyledPanel)
        pipeline_manage_layout.setFixedWidth(WIDTH_RIGHT_FRAME)
        self.pipeline_manage_layout = QVBoxLayout(pipeline_manage_layout)
        
        transformation_manage_frame = QFrame()
        transformation_manage_frame.setFrameShape(QFrame.StyledPanel)
        transformation_manage_frame.setFixedWidth(WIDTH_RIGHT_FRAME)
        self.transformation_manage_layout = QVBoxLayout(transformation_manage_frame)

        frame2_layout.addWidget(self.image_frame)
        frame2_layout.addWidget(self.import_button)
        frame2_layout.addWidget(pipeline_manage_layout)
        frame2_layout.addWidget(transformation_manage_frame)

        # Main Frame --------------------------------------------------------------------
        central_widget = QFrame()
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(upper_frame)
        main_layout.addWidget(lower_frame)

        self.setCentralWidget(central_widget)


    def refresh_upper_transformation(self):
        """Update the pipeline of image at the top of the window"""
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
            self.add_insert_add_transformation()
            self.add_transform_buttons()  
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
        label_dimension = QLabel()
        label_dimension.setText(text_dimension)
        label_dimension.setFixedHeight(15)
        self.image_frame.layout().addWidget(label_dimension)
    
    def add_insert_add_transformation(self):
        """Add a QFrame that contains the choice to add of insert a transformation in the pipeline"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        self.b1 = QRadioButton("Add")
        self.b1.setChecked(True)
        layout.addWidget(self.b1)
            
        self.b2 = QRadioButton("Insert")

        layout.addWidget(self.b2)
        self.pipeline_manage_layout.addWidget(frame)

    def add_transform_buttons(self):
        """Add the buttons to transform the image (blur, grayscale, ...) in a QFrame"""
        frame = QFrame()
        layout = QVBoxLayout(frame)

        alert_transform_functions = {
            self.alert_colorchange: "Color Change",
            self.alert_gaussian_blur: "Gaussian Blur"
        }

        for index, (transform_func, string) in enumerate(alert_transform_functions.items()):
            button = QPushButton(string)
            button.clicked.connect(transform_func)
            layout.addWidget(button)
        
        self.pipeline_manage_layout.addWidget(frame)


    def alert_custom(self, string_transformation):
        """Add a string in "transformations" that represent the transformations of the pixmaps"""
        insert = self.b2.isChecked()
        if len(self.transformations)<=self.index_current_img:
            self.transformations.append(string_transformation)
            self.index_current_img += 1
        elif insert:
            self.transformations.insert(self.index_current_img, string_transformation)
        elif not insert:
            self.transformations[self.index_current_img] = string_transformation
            self.index_current_img += 1
        self.update_pipeline(self.index_current_img)
        self.update_image_show()
        print(string_transformation)


    def alert_colorchange(self):
        """Send a string to "alert_custom" that contains info about the new transformation"""
        self.alert_custom("colorchange_RGB2GRAY")

    def alert_gaussian_blur(self):
        """Send a string to "alert_custom" that contains info about the new transformation"""
        self.alert_custom("gaussianblur_default")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
