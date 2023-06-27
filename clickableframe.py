from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Signal

class ClickableFrame(QFrame):
    """pipeline object"""
    clicked = Signal(int)

    def __init__(self, index):
        super().__init__()
        self.index = index

    def mousePressEvent(self, event):
        self.clicked.emit(self.index)