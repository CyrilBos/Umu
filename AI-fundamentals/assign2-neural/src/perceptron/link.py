class Link:
    """
    Class that contains a weight and a single reference to an instance of InputNode.
    """

    def __init__(self, input_node, weight=0.5):
        """
        Initializes a new instance of Link.
        :param input_node: instance of InputNode to store the reference to
        :type input_node: InputNode
        :param weight: initial value of link weight
        :type weight: float
        """
        self._input_node = input_node
        self._weight = weight

    @property
    def input_node(self):
        return self._input_node

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value
