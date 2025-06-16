from qtpy.QtWidgets import QComboBox, QLabel, QFrame, QVBoxLayout

MAXIMUM_HEIGHT = 65

class MenuWithText(QFrame):
    """A qframe with text on top of a QCombobox"""
    def __init__(self, menu_parameters, index, event_to_call):
        # event_to_call is calling parent object in order to have synchronous event
        super().__init__()
        self.setMaximumHeight(MAXIMUM_HEIGHT)

        self.parameters = menu_parameters

        self.menu = QComboBox()
        self.menu.addItems(menu_parameters['menu_item'].keys())
        self.menu.setCurrentIndex(index)
        self.menu.currentIndexChanged.connect(self.update_value_changed)
        self.menu.currentIndexChanged.connect(event_to_call)

        first_val = list(menu_parameters['menu_item'].values())[0]
        if isinstance(first_val, str):
            first_val = eval(first_val)
        self.value = first_val

        self.variable_name = self.parameters['variable_name']


        self.label = QLabel()
        self.label.setText(menu_parameters['name'])

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.menu)


    def update_value_changed(self):
        current_index_menu = self.menu.currentIndex()
        val = list(self.parameters['menu_item'].values())[current_index_menu]
        if isinstance(val, str):
            val = eval(val)
        self.value = val
