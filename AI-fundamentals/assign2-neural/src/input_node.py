from numpy import average

from .node import Node

class InputNode(Node):
    def __init__(self, pixels_ind, threshold=0.5):
        super().__init__(threshold)
        self._pixels_ind = pixels_ind

    def output(self, image):
        #TODO: opti without copy
        pixels = []
        for ind in self._pixels_ind:
            pixels.append(image.get_pixel(ind))
        return average(pixels) / 32.0
