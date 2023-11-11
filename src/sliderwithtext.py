from qtpy.QtWidgets import QLabel, QFrame, QVBoxLayout
from stepslider import StepSlider

MAXIMUM_HEIGHT = 65

class SliderWithText(QFrame):
    """A qframe with text on top of a qslider(with steps)"""
    def __init__(self, image, slider_parameters, value, event_to_call):
        # event_to_call is calling parent object in order to have synchronous event
        super().__init__()
        self.setMaximumHeight(MAXIMUM_HEIGHT)

        self.event_to_call = event_to_call

        self.parameters = slider_parameters

        self.variable_name_to_display = slider_parameters['name'] + " : "
        self.value = value

        self.label = QLabel()
        self.update_label()

        self.slider = StepSlider(image, slider_parameters['min_value'], slider_parameters['max_value'], slider_parameters['step'], value, self.update_value_changed)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)

    def update_value_changed(self):
        """Update the parameters and call the event of parent object"""
        self.value = self.slider.old_value
        self.update_label()
        self.event_to_call()

    def update_label(self):
        """Update the text of the label"""
        self.label.setText(self.variable_name_to_display + str(self.value))

