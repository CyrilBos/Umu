from .node import Node

class OutputNode(Node):
    _input_links = []

    def __init__(self, threshold, emotion):
        super().__init__(threshold)
        self._emotion = emotion

    def is_activated(self, image):
        node_sum = 0
        for input_link in self._input_links:
            input_node = input_link.input_node
            node_sum += input_link.weight * input_node.is_activated(image)
        #@Dorian calcul correspondant `a g() dans diapo 8
        return node_sum / 400 > self._threshold

    @property
    def input_links(self):
        return self._input_links

    @property
    def emotion(self):
        return self._emotion
