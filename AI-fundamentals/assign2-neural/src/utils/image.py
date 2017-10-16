from typing import List

ROW_WIDTH = 20

class Image:
    def __init__(self, pixels):
        self._pixels = pixels

    def __str__(self) -> str:
        return '<Image>\n Pixels:\n' + self._pixels.__str__()


    @property
    def pixels(self) -> List[List[int]]:
        return self._pixels

    def get_pixel_by_index(self, index) -> int:
        try:
            return self._pixels[int(index / ROW_WIDTH)][index % ROW_WIDTH]
        except IndexError as e:
            print(index / ROW_WIDTH, ' ', index % ROW_WIDTH)