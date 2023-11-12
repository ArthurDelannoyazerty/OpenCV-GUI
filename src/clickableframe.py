from qtpy.QtWidgets import QFrame
from qtpy.QtCore import Signal

class ClickableFrame(QFrame):
    """qframe that call an event when the user click on it"""
    clicked = Signal(int)

    def __init__(self, index):
        super().__init__()
        self.index = index

    def mousePressEvent(self, event):
        self.clicked.emit(self.index)