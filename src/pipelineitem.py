from qtpy.QtGui import QPixmap, QImage, qRgb
from numpy import uint8, require

class PipelineItem():
    """Object that contains the image in an array and the corresponding transformation item"""
    def __init__(self, img_array=None, transformation_item=None):
        self.img_array = img_array
        self.transformation_item = transformation_item
    
    def get_pixmap(self):
        qimage = self.to_q_image(self.img_array)
        qpixmap = QPixmap.fromImage(qimage)
        return qpixmap

    # from https://gist.github.com/fepegar/c85e1c64c36934628507588037dba41b
    def to_q_image(self, im, copy=False):
        """array in uint8 to a QImage"""
        gray_color_table = [qRgb(i, i, i) for i in range(256)]
        
        if im is None:
            return QImage()

        if im.dtype == uint8:
            im = require(im, uint8, 'C')
            if len(im.shape) == 2:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                qim.setColorTable(gray_color_table)
                return qim.copy() if copy else qim

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888);
                    return qim.copy() if copy else qim
                elif im.shape[2] == 4:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
                    return qim.copy() if copy else qim
                
        raise Exception("Array to Qimage not implemented")