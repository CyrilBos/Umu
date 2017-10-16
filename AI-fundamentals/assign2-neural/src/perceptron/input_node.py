from numpy import average, math


class InputNode:
    def __init__(self, pixel_ind):
        self._pixels_ind = pixel_ind

    def get_activation_level(self, image):
        pixel_value = image.get_pixel_by_index(self._pixels_ind)
        return 1 / (1 + math.exp(-pixel_value))