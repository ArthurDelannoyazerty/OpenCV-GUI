from PySide6.QtGui import QPixmap, QImage

class PipelineItem():
    def __init__(self, img_array=None, str_transformation=""):
        self.img_array = img_array
        self.str_transformation = str_transformation
    
    def get_pixmap(self):
        height, width, channel = self.img_array.shape
        bytes_per_line = channel * width
        qimage = QImage(self.img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap