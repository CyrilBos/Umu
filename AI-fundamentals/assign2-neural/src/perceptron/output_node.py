import math


class OutputNode:
    """
    Output node that contains the links to its inputs and represents one of the four emotions.
    """

    def __init__(self, emotion):
        """
       Initializes a new instance of InputNode.
       :param emotion: instance of Emotion class to link this output node to
       :type emotion: Emotion
       """
        self._emotion = emotion
        self._input_links = []

    def get_activation_level(self, image):
        """
        Computes and returns the activation level of the output node.
        :param image: selected image for the input nodes to return their pixel value
        :type image: Image
        """
        node_sum = 0
        for input_link in self._input_links:
            input_node = input_link.input_node
            activation_level = input_node.get_activation_level(image)
            node_sum += input_link.weight * activation_level

        return 1 / (1 + math.exp(-node_sum))

    @property
    def input_links(self):
        return self._input_links

    @property
    def emotion(self):
        return self._emotion
