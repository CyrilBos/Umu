from input_node import InputNode, MAX_GREY_LEVEL


class FixedInputNode(InputNode):
    """
    Specific InputNode that is assigned a fixed pixel value. Inherits from InputNode for polymorphism benefits.
    """

    def __init__(self, fixed_pixel_value):
        """
        Initializes a new instance of FixedInputNode.
        :param fixed_pixel_value: value between 0 and 31 of fixed grey level
        :type fixed_pixel_value: int
        """
        super().__init__(None)
        self._fixed_pixel_value = fixed_pixel_value

    def get_activation_level(self, image):
        """
        Returns the activation level of this FixedInputNode, being its fixed grey level value divided by 31.
        Uses image as a parameter to override InputNode.get_activation_level(image) for polymorphism benefits.
        :param image: unused instance of Image
        :type image: Image
        """
        return self._fixed_pixel_value / MAX_GREY_LEVEL
