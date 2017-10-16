class Link:
    def __init__(self, input_node, weight=0.5):
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
