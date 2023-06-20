import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QFileDialog, QWidget, QScrollArea
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtCore import Qt, QSize, Signal

WIDTH_RIGHT_FRAME = 200
HEIGHT_UPPER_FRAME = 150

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

        self.transformations = []
        self.pixmaps = []
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

        layout_frame1 = QVBoxLayout(self.upper_frame)

        scroll_area = QScrollArea()

        container_widget = QWidget(scroll_area)
        self.container_upper = QVBoxLayout(container_widget)

        scroll_area.setWidget(container_widget)

        layout_frame1.addWidget(scroll_area)
    
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
        while self.container_upper.count():
            item = self.container_upper.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for index, pixmap in enumerate(self.pixmaps):
            frame = ClickableFrame(index)
            frame.setFixedSize(QSize(100, 150))
            frame.setFrameShape(QFrame.Box)
            frame.clicked.connect(self.frame_clicked)

            layout = QHBoxLayout(frame)

            pixmap_label = QLabel()
            pixmap_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(pixmap_label)

            index_label = QLabel(f"Index: {index}")
            index_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(index_label)

            self.container_upper.addWidget(frame)

        self.container_upper.update()

    def frame_clicked(self, index):
        """Print a message (index) when clicking on the pipeline of images"""
        print(f"Frame clicked: {index}")

    def open_image_dialog(self):
        """Open a Choose File dialog box to choose the image"""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

        if file_name:
            pixmap = QPixmap(file_name)
            self.index_current_img = 0
            self.pixmaps.append(pixmap)
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

        pixmap = self.pixmaps[self.index_current_img]
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
        if 0 <= self.index_current_img < len(self.pixmaps):
            pixmap = self.pixmaps[self.index_current_img]
            self.image.setPixmap(pixmap.scaledToWidth(self.image_frame.width(), Qt.SmoothTransformation))
            self.image.setAlignment(Qt.AlignCenter)
    
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
            self.alert_grayscale: "Grayscale",
            self.alert_gaussian_blur: "Gaussian Blur"
        }

        for index, (transform_func, string) in enumerate(alert_transform_functions.items()):
            button = QPushButton(string)
            button.clicked.connect(transform_func)
            layout.addWidget(button)
        
        self.layout_transform_parameters.addWidget(frame)

    def is_transformation_index_free(self):
        """Return True if an image can be inserted at the "index_current_img" index. False if we need to append"""
        return len(self.transformations)<=self.index_current_img

    def alert_custom(self, string_transformation):
        """Add a string in "transformations" that represent the transformations of the pixmaps"""
        insert = self.b2.isChecked()
        if self.is_transformation_index_free():
            self.transformations.append(string_transformation)
            self.index_current_img += 1
        elif insert:
            self.transformations.insert(self.index_current_img, string_transformation)
        elif not insert:
            self.transformations[self.index_current_img] = string_transformation
            self.index_current_img += 1
        print(string_transformation)

    def alert_grayscale(self):
        """Send a string to "alert_custom" that contains info about the new transformation"""
        self.alert_custom("grayscale_default")

    def alert_gaussian_blur(self):
        """Send a string to "alert_custom" that contains info about the new transformation"""
        self.alert_custom("gaussianblur_default")

    def update_img_from_index(self, index=None):
        """Update the pixmaps from a specified index (auto=index_current_img-1) and fire a graphical update"""
        current_index = self.index_current_img-1 if self.index_current_img-1<0 else 0
        current_index = index if index!=None else current_index
        #TODO

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
