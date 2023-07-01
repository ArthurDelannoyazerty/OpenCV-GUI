from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt

class StepSlider(QSlider):
    def __init__(self, min_value, max_value, step, value, event_to_call):
        super().__init__()
        self.setRange(min_value, max_value) 
        self.setOrientation(Qt.Horizontal)  
        
        self.event_to_call = event_to_call
        self.step = step
        self.setValue(value)
        self.old_value = 0
        
        self.valueChanged.connect(self.updateValue)  

    def updateValue(self, value):
        # step
        step_value = value-self.minimum()
        step_value = int(step_value%self.step)
        value = value-step_value
        self.setValue(value)
        # alert
        if self.old_value!=self.value():
            self.old_value = self.value()
            self.event_to_call()