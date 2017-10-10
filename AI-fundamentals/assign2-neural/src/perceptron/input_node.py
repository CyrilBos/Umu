from numpy import average

from .node import Node

class InputNode(Node):
    def __init__(self, pixels_ind, threshold=0.5):
        super().__init__(threshold)
        self._pixels_ind = pixels_ind

    def is_activated(self, image):
        # @Dorian en gros si grey_level > 16 c' est active
        # mais generalise avec la moyenne des pixels pour plus tard
        return self.output(image) > self._threshold

    def output(self, image):
        pixels_sum = 0
        for ind in self._pixels_ind:
            pixels_sum += image.get_pixel(ind)
        #returns average / 32 to get a value between 0 and 1
        return pixels_sum / len(self._pixels_ind) / 32