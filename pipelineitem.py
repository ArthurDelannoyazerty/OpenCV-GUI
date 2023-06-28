from PySide6.QtGui import QPixmap, QImage

class PipelineItem():
    def __init__(self, img_array=None, transformation_item=None):
        self.img_array = img_array
        self.transformation_item = transformation_item
    
    def get_pixmap(self):
        height, width, channel = self.img_array.shape #FIXME
        bytes_per_line = channel * width
        qimage = QImage(self.img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap