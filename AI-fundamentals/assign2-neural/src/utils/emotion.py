emotions = ['Happy', 'Sad', 'Mischievous', 'Mad']

class Emotion:
    def __init__(self, parsed_value):
        self.__value = parsed_value-1

    def __str__(self):
        return emotions[self.__value]

    @property
    def value(self):
        return self.__value
