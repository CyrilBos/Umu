import re

from .training_image import TrainingImage
from .image import Image


class Parser:
    def __init__(self):
        pass

    def parse_pixels(self, pixels_filepath):
        pixels_file = open(pixels_filepath, 'r')

        cur_index = -1
        pixels = []
        cur_pixels = []

        for line in pixels_file:
            if not re.match('[#\n]', line):#ignore if line is empty or a comment
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

        pixels.append(cur_pixels)  # add last image

        pixels_file.close()

        return pixels

    def parse_training_images(self, training_filepath, facit_filepath):
        images = []

        # parse the pixels into an array
        pixels = self.parse_pixels(training_filepath)

        cur_index = -1

        facit_file = open(facit_filepath, 'r')
        for line in facit_file:
            if not re.match('[#\n]', line):
                matches = re.match('Image\d* (\d)', line)
                if matches:
                    cur_index += 1
                    val = matches.groups()[0]
                    images.append(TrainingImage(pixels[cur_index], int(val) - 1))

        return images

    def parse_test_images(self, test_images_path):
        test_images = []
        images_pixels = self.parse_pixels(test_images_path)
        for image_pixels in images_pixels:
            test_images.append(Image(image_pixels))
        return test_images
