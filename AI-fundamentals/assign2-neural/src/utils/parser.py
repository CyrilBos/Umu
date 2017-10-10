import re

from .image import Image


class Parser:
    def __init__(self):
        pass

    def parse_training_images(self, training_filepath, facit_filepath):
        images = []
        training_file = open(training_filepath, 'r')

        cur_index = -1
        pixels = []
        cur_pixels = []

        for line in training_file:
            if not re.match('#|\n', line):
                if re.match('Image\d*', line):
                    cur_index += 1
                    if cur_index > 0:
                        pixels.append(cur_pixels)
                        cur_pixels = []
                else:
                    matches = re.findall('\d{1,2}\s+', line)
                    if matches:
                        row = []
                        for val in matches:
                            row.append(int(val.strip()))
                        cur_pixels.append(row)

        pixels.append(cur_pixels)#last image

        training_file.close()


        cur_index = -1

        facit_file = open(facit_filepath, 'r')
        for line in facit_file:
            if not re.match('#|\n', line):
                matches = re.match('Image\d* (\d)', line)
                if matches:
                    cur_index += 1
                    val = matches.groups()[0]
                    images.append(Image(pixels[cur_index], int(val)-1))


        return images