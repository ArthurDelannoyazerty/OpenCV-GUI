class TransformationItem():
    """Contains the name of the transformation and a dict of the name of the parameters and their values"""
    def __init__(self, transformation_name, parameters):
        self.name = transformation_name
        self.parameters = parameters # in a dict {var_name: value}