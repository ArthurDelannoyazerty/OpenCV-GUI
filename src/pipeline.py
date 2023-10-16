class Pipeline(list):
    """List of the PipelineItem.
        
    
        First Item  : PipelineItem = (original array, No transformation)

        Second Item : PipelineItem = (second array, first transformation)

        The PipelineItem n take the image from n-1, apply the transformation n and save the image n in itself
    """
    def __init__(self, transformer, function_to_call_error):
        self.transformer = transformer
        self.function_to_call_error = function_to_call_error

    def execute_transformation(self, index):
        """Transform the wanted index of the pipeline"""
        if index<1 or index>=len(self):
            raise Exception("Wrong index to update pipeline, index sent : " + str(index) + ". Valid index : [1, "+ str(len(self)) + "]")
        item_before = self[index-1]
        item_current = self[index]
        try:
            item_current.img_array = self.transformer.transform(item_before, item_current)
        except:
            self.function_to_call_error("An error occured in the transformation pipeline ("+ str(index-1)+ "->"+ str(index) +"). Action cancelled.")
            raise Exception("Error in the pipeline."+ str(index-2)+ "->"+ str(index-1))

    def update_from_index(self, index=1):
        """Update the images in the pipeline from the wanted index."""
        if index<1 or index>=len(self):
            raise Exception("Wrong index to update pipeline, index sent : " + str(index) + ". Valid index : [1, "+ str(len(self)) + "]")
        for index in range(index, len(self)):
            self.execute_transformation(index)