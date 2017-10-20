class Emotion:
    """
    Class that contains a static list of emotions strings, mapping the emotion value from 1-5 to 0-4.
    """

    emotions_list = ['Happy', 'Sad', 'Mischievous', 'Mad']

    def __init__(self, value):
        """
        Initializes a new Emotion instance.
        :param value: equal to parsed value - 1
        :param value: int
        """
        self.__value = value

    def __eq__(self, other):
        return self.__value == other.__value

    @property
    def value(self):
        return self.__value
