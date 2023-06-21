import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QFileDialog, QWidget, QScrollArea
from PySide6.QtGui import QPixmap, Qt, QImage
from PySide6.QtCore import Qt, QSize, Signal
import cv2 as cv

WIDTH_RIGHT_FRAME = 200
HEIGHT_UPPER_FRAME = 150
HEIGHT_TILES = HEIGHT_UPPER_FRAME - 50
WIDTH_TILES = 150

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.transformer = Transformer()

        self.transformations = []
        self.img_arrays = []
        self.index_current_img = -1

        self.setGeometry(100, 100, 700, 700)

        self.initiate_frames()

        self.resizeEvent = self.customResizeEvent

    def initiate_frames(self):
        """Create the main QFrame"""
        central_widget = QFrame()
        layout = QVBoxLayout(central_widget)

        self.initiate_upper_frame()
        self.initiate_lower_frame()

        layout.addWidget(self.upper_frame)
        layout.addWidget(self.lower_frame)

        self.setCentralWidget(central_widget)
    
    def initiate_upper_frame(self):
        """Create the upper frame with its child"""
        self.upper_frame = QFrame()
        self.upper_frame.setFrameShape(QFrame.StyledPanel)
        self.upper_frame.setFixedHeight(HEIGHT_UPPER_FRAME)

        layout_frame1 = QHBoxLayout(self.upper_frame)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout_frame1.addWidget(self.scroll_area)

        container_upper_widget = QWidget(self.scroll_area)
        self.container_upper_layout = QVBoxLayout(container_upper_widget)
        self.scroll_area.setWidget(container_upper_widget)
    
    def initiate_lower_frame(self):
        """Create the lower frame with its child"""
        self.lower_frame = QFrame()
        self.lower_frame.setFrameShape(QFrame.StyledPanel)
        frame2_layout = QHBoxLayout(self.lower_frame)
        
        self.image_frame = QFrame()
        image_frame_layout = QVBoxLayout(self.image_frame)
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMinimumSize(1, 1)
        image_frame_layout.addWidget(self.image)
        self.image_frame.hide()
        
        self.import_button = QPushButton("Importer une image")
        self.import_button.clicked.connect(self.open_image_dialog)

        self.right_transform_parameters_frame = QFrame()
        self.right_transform_parameters_frame.setFrameShape(QFrame.StyledPanel)
        self.right_transform_parameters_frame.setFixedWidth(WIDTH_RIGHT_FRAME)
        self.layout_transform_parameters = QVBoxLayout(self.right_transform_parameters_frame)
        
        self.right_transform_manage_frame = QFrame()
        self.right_transform_manage_frame.setFrameShape(QFrame.StyledPanel)
        self.right_transform_manage_frame.setFixedWidth(WIDTH_RIGHT_FRAME)

        frame2_layout.addWidget(self.image_frame)
        frame2_layout.addWidget(self.import_button)
        frame2_layout.addWidget(self.right_transform_parameters_frame)
        frame2_layout.addWidget(self.right_transform_manage_frame)

    def refresh_upper_transformation(self):
        """Update the pipeline of image at the top of the window"""
        for index, img in enumerate(self.img_arrays):
            pixmap = self.numpy_array_to_pixmap(img)
            frame = ClickableFrame(index)
            frame.setFixedSize(QSize(WIDTH_TILES, HEIGHT_TILES))
            frame.setFrameShape(QFrame.Box)
            frame.clicked.connect(self.frame_clicked)

            layout = QVBoxLayout(frame)

            pixmap_label = QLabel()
            pixmap_label.setPixmap(pixmap.scaled(WIDTH_TILES, HEIGHT_TILES, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(pixmap_label)

            index_label = QLabel(f"Index: {index}")
            index_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(index_label)

            self.container_upper_layout.addWidget(frame)

        # self.container_upper.update()

    def numpy_array_to_pixmap(self, numpy_array):
        height, width, channel = numpy_array.shape
        bytes_per_line = channel * width
        qimage = QImage(numpy_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap

    def frame_clicked(self, index):
        """Print a message (index) when clicking on the pipeline of images"""
        print(f"Frame clicked: {index}")

    def open_image_dialog(self):
        """Open a Choose File dialog box to choose the image"""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

        if file_name:
            img_arrays = cv.imread(file_name, cv.IMREAD_COLOR)
            img_arrays = cv.cvtColor(img_arrays, cv.COLOR_BGR2RGB)
            self.index_current_img = 0
            self.img_arrays.append(img_arrays)
            self.update_image_show()

            self.import_button.hide()
            self.image_frame.setHidden(False)
            self.customResizeEvent(None)

            self.refresh_upper_transformation()
            self.add_insert_add_transformation()
            self.add_transform_buttons()  
            self.index_current_img = 0
        # TODO menu déroulantpour choisir autre image + update from 0

    def customResizeEvent(self, event):
        """Change the size of the main image we the main window is resized"""
        if self.index_current_img == -1:
            return

        frame_height = self.image_frame.height() - 20   # magic number because of the margin of the parent QFrame
        frame_width = self.image_frame.width() - 20

        pixmap = self.numpy_array_to_pixmap(self.img_arrays[self.index_current_img])
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
        """Show the image based on the "index_current_img" """
        if 0 <= self.index_current_img < len(self.img_arrays):
            current_img_arrays = self.img_arrays[self.index_current_img]
            pixmap = self.numpy_array_to_pixmap(current_img_arrays)
            self.image.setPixmap(pixmap.scaledToWidth(self.image_frame.width(), Qt.SmoothTransformation))
            self.image.setAlignment(Qt.AlignCenter)

            text_dimension = str(current_img_arrays.shape).replace("(","").replace(")","").split(", ")
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
        self.layout_transform_parameters.addWidget(frame)

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
        
        self.layout_transform_parameters.addWidget(frame)


    def update_pipeline(self, index_start=1):
        if 1 <= index_start <= len(self.img_arrays):
            for index in range(index_start, len(self.img_arrays)):
                img_before = self.img_arrays[index-1]
                transformed_img = self.transformer.transform(img_before, self.transformations[index-1])
                if index<len(self.img_arrays):
                    self.img_arrays[index] = transformed_img
                else:
                    self.img_arrays.append(transformed_img)
                    # increment current_index done in "alert_custom()"


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
