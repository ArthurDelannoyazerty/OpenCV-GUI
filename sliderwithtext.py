from PySide6.QtWidgets import QSlider, QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from stepslider import StepSlider

MAXIMUM_HEIGHT = 65

class SliderWithText(QFrame):
    def __init__(self, slider_parameters, value, event_to_call):
        super().__init__()
        self.setMaximumHeight(MAXIMUM_HEIGHT)

        self.event_to_call = event_to_call

        self.parameters = slider_parameters

        self.variable_name_to_display = slider_parameters['name'] + " : "
        self.value = value

        self.label = QLabel()
        self.update_label()

        self.slider = StepSlider(slider_parameters['min_value'], slider_parameters['max_value'], slider_parameters['step'], value, self.update_value_changed)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)

    def update_value_changed(self):
        self.value = self.slider.old_value
        self.update_label()
        self.event_to_call()

    def update_label(self):
        self.label.setText(self.variable_name_to_display + str(self.value))

