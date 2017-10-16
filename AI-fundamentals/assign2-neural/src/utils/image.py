from typing import List

from .emotion import Emotion

ROW_WIDTH = 20

class Image:
    def __init__(self, pixels):
        self.__pixels = pixels

    def __str__(self) -> str:
        return '<Image>\n Pixels:\n' + self.__pixels.__str__()


    @property
    def pixels(self) -> List[List[int]]:
        return self.__pixels

    def get_pixel_by_index(self, index) -> int:
        try:
            return self.__pixels[int(index / ROW_WIDTH)][index % ROW_WIDTH]
        except IndexError as e:
            print(index / ROW_WIDTH, ' ', index % ROW_WIDTH)