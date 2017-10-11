from typing import List

from .emotion import Emotion

ROW_WIDTH = 20

class Image:
    def __init__(self, pixels, emotion_value):
        self.__pixels = pixels
        self.__emotion = Emotion(emotion_value)

    def __str__(self) -> str:
        return '<Image>\n Pixels:\n' + self.__pixels.__str__() \
               + '\nEmotion: ' + self.__emotion.__str__()

    @property
    def emotion(self):
        return self.__emotion

    @property
    def pixels(self) -> List[List[int]]:
        return self.__pixels

    def get_pixel(self, index) -> int:

        return self.__pixels[int(index / ROW_WIDTH)][index % ROW_WIDTH]

    #TODO: magic formula with better computational complexity?
    def pixels_from(self, start_row, start_col) -> List[int]:
        pixels = []
        for i in range(start_row, ROW_WIDTH):
            for j in range(start_col, ROW_WIDTH):
                pixels.append(self.__pixels[i,j])
        return pixels