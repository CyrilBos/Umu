MAX_GREY_LEVEL = 31


class InputNode:
    """
    Node that processes the input, being a single pixel which only the index in the image is stored.
    The same InputNode always look at the same pixel location.
    """

    def __init__(self, pixel_index):
        """
        Initializes a new instance of InputNode.
        :param pixel_index: Index of targeted pixel in the image matrix
        :type pixel_index: int
        """
        self.__pixel_index = pixel_index

    def get_activation_level(self, image):
        """
        Returns the activation level of this InputNode, being the pixel of stored index divided by 31.
        :param image: image to get the pixel value from using the stored index
        :type image: Image
        """
        pixel_value = image.get_pixel_by_index(self.__pixel_index)
        return pixel_value / MAX_GREY_LEVEL
