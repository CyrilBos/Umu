from .node import Node

class OutputNode(Node):
    def __init__(self, threshold, emotion):
        super().__init__(threshold)
        self._emotion = emotion

    @property
    def emotion(self):
        return self._emotion
