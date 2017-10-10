emotions = ['Happy', 'Sad', 'Mischievous', 'Mad']

class Emotion:
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return emotions[self.__value]

    def __eq__(self, other):
        return self.__value == other.__value

    @property
    def value(self):
        return self.__value
