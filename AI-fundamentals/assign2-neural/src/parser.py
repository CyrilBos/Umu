import re

from training_image import TrainingImage
from image import Image


class Parser:
    def __init__(self):
        pass

    def __parse_pixels(self, pixels_filepath):
        """
        Parses pixels, method common to parsing the training images and parsing the unclassified images.
        """
        pixels_file = open(pixels_filepath, 'r')

        cur_index = -1
        pixels = []
        cur_pixels = []

        for line in pixels_file:
            if not re.match('[#\n]', line):  # ignore if line is empty or a comment
                if re.match('Image\d*', line):  # match a new image
                    cur_index += 1
                    if cur_index > 0:
                        pixels.append(cur_pixels)
                        cur_pixels = []
                else:
                    matches = re.findall('\d{1,2}\s+', line)  # parses one row of pixels
                    if matches:
                        row = []
                        for val in matches:
                            row.append(int(val.strip()))
                        cur_pixels.append(row)

        pixels.append(cur_pixels)  # add last image

        pixels_file.close()

        return pixels

    def parse_training_images(self, training_filepath, facit_filepath):
        """
        Parses pixels and emotions and returns a list of TrainingImage instances.
        """
        images = []

        # parse the pixels into an array
        pixels = self.__parse_pixels(training_filepath)

        cur_index = -1

        facit_file = open(facit_filepath, 'r')
        for line in facit_file:
            if not re.match('[#\n]', line):
                matches = re.match('Image\d* (\d)', line)  # matches a new image and the corresponding emotion value
                if matches:
                    cur_index += 1
                    val = matches.groups()[0]
                    images.append(TrainingImage(pixels[cur_index], int(val) - 1))  # value-1 to use the emotions list

        return images

    def parse_test_images(self, test_images_path):
        """
        Parses the training images into a list of Image instances.
        """
        test_images = []
        images_pixels = self.__parse_pixels(test_images_path)
        for image_pixels in images_pixels:
            test_images.append(Image(image_pixels))
        return test_images
