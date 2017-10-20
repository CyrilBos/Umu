IMAGE_ROW_WIDTH = 20


class Image:
    def __init__(self, pixels):
        self._pixels = pixels

    def __str__(self):
        return '<Image>\n Pixels:\n' + self._pixels.__str__()

    @property
    def pixels(self):
        return self._pixels

    @pixels.setter
    def pixels(self, value):
        self._pixels = value

    def get_pixel_by_index(self, index):
        return self._pixels[int(index / IMAGE_ROW_WIDTH)][index % IMAGE_ROW_WIDTH]
