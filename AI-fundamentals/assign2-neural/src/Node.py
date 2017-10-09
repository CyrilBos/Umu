class Node:
    def __init__(self,pixels,weights):
        """

        :param pixels: list of tuples for pixels positions
        :param weights: initial values for weights on this node
        """
        self.__weights = weights
        self.__pixels = pixels

    def getPixel(self,imageSet,pixel):
        """

        :param imageSet: matrix of values
        :param pixel: tuple of integer for position of the pixel
        :return:
        """
        pass

    def updateWeights(self,trainingSet,facitSet):
        """

        :param trainingSet:
        :param facitSet:
        :return:
        """
        pass

    def computeValue(self,testSet):
        """

        :param testSet:
        :return: value of the node
        """
        pass
