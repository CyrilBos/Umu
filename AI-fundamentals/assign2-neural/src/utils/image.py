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

    def _get_contrasted_pixels(self,contrast=0):
        contrasted_pixels = []
        factor = (259*(contrast+255))/(255*(259-contrast))
        for i in range(self.ROW_WIDTH):
            contrasted_pixels.append([])
            for j in range(self.ROW_WIDTH):
                pixel = 8*self.get_pixel_by_index((i*self.ROW_WIDTH)+j)
                contrasted = (factor*(pixel-128))+128
                if contrasted >= 255:
                    contrasted_pixels[i].append(31)
                if contrasted <= 0:
                    contrasted_pixels[i].append(0)
                else:
                    contrasted_pixels[i].append(int(contrasted/8))
        return contrasted_pixels

    def get_contrasted_image(self):
        return Image(self._get_contrasted_pixels())
