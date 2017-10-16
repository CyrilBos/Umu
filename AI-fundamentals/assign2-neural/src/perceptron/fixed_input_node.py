import math

from .input_node import InputNode


class FixedInputNode(InputNode):
    def __init__(self, fixed_pixel_value):
        super().__init__([])
        self._fixed_pixel_value = fixed_pixel_value

    def get_activation_level(self, image):
        return 1 / (1 + math.exp(-self._fixed_pixel_value))
