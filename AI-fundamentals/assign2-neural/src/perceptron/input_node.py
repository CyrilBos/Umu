from numpy import average, math


class InputNode:
    def __init__(self, pixels_ind):
        self._pixels_ind = pixels_ind

    def get_activation_level(self, image):
        pixels_sum = 0
        pixels_count = len(self._pixels_ind)
        for ind in self._pixels_ind:
            pixels_sum += image.get_pixel_by_index(ind)

        return 1 / (1 + math.exp(-pixels_sum / pixels_count))