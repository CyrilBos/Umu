
class Emotion:
    emotions_list = ['Happy', 'Sad', 'Mischievous', 'Mad']

    def __init__(self, value):
        self.__value = value

    def __eq__(self, other):
        return self.__value == other.__value

    @property
    def value(self):
        return self.__value
