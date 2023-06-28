class TransformationItem():
    def __init__(self, transformation_name, parameters):
        self.name = transformation_name
        self.parameters = parameters # in a dict {var_name: value}