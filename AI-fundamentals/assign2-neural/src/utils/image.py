from typing import List


class Image:
    ROW_WIDTH = 20

    def __init__(self, pixels):
        self._pixels = pixels

    def __str__(self) -> str:
        return '<Image>\n Pixels:\n' + self._pixels.__str__()

    @property
    def pixels(self) -> List[List[int]]:
        return self._pixels

    def get_pixel_by_index(self, index) -> int:
        return self._pixels[int(index / self.ROW_WIDTH)][index % self.ROW_WIDTH]

    def _get_contrasted_pixels(self):
        contrasted_pixels = []
        # magie du contraste
        # TU MODIFIES PAS self._pixels pd
        return contrasted_pixels

    def get_contrasted_image(self):
        return Image(self._get_contrasted_pixels())
