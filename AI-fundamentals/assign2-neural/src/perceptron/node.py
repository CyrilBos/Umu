class Node:
    _input_links = []
    _weight = 0.5

    def __init__(self, threshold):
        self._threshold = threshold

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

    def getPixel(self, imageSet, pixel):
        """

        :param imageSet: matrix of values
        :param pixel: tuple of integer for position of the pixel
        :return:
        """
        pass

    def updateWeights(self, trainingSet, facitSet):
        """

        :param trainingSet:
        :param facitSet:
        :return:
        """
        pass

    def computeValue(self, testSet):
        """

        :param testSet:
        :return: value of the node
        """
        pass