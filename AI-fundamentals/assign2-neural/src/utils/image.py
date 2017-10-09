from .emotion import Emotion

from typing import List


class Image:
    def __init__(self, pixels, emotion_value):
        self.__pixels = pixels
        self.__emotion = Emotion(emotion_value)

    def __str__(self) -> str:
        return '<Image>\n Pixels:\n' + self.__pixels.__str__() \
               + '\nEmotion: ' + self.__emotion.__str__()

    @property
    def pixels(self) -> List[List]:
        return self.__pixels
