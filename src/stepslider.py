from qtpy.QtWidgets import QSlider
from qtpy.QtCore import Qt

class StepSlider(QSlider):
    """A 'working' qslider with steps (working with steps of 2 and int values)"""
    def __init__(self, image, min_value, max_value, step, value, event_to_call):
        # image used in eval()
        # event_to_call is calling parent object in order to have synchronous event
        super().__init__()
        self.setRange(eval(min_value), eval(max_value)) 
        self.setOrientation(Qt.Horizontal)  
        
        self.event_to_call = event_to_call
        self.step = eval(step)
        self.setValue(value)
        self.old_value = 0
        
        self.valueChanged.connect(self.updateValue)  

    def updateValue(self, value):
        """Update the value when the slider move. Correct value if step not valid. Don't really know how it works but ok for step=2 at least"""
        # step
        step_value = value-self.minimum()
        step_value = int(step_value%self.step)
        value = value-step_value
        self.setValue(value)
        # alert
        if self.old_value!=self.value():
            self.old_value = self.value()
            self.event_to_call()