class Pipeline(list):
    def __init__(self, transformer):
        self.transformer = transformer

    def execute_transformation(self, index):
        if index<1 or index>=len(self):
            raise Exception("Wrong index to update pipeline, index sent : " + str(index) + ". Valid index : [1, "+ str(len(self)) + "]")
        item_before = self[index-1]
        item_current = self[index]
        item_current.img_array = self.transformer.transform(item_before, item_current)

    def update_from_index(self, index=1):
        if index<1 or index>=len(self):
            raise Exception("Wrong index to update pipeline, index sent : " + str(index) + ". Valid index : [1, "+ str(len(self)) + "]")
        for index in range(index, len(self)):
            self.execute_transformation(index)