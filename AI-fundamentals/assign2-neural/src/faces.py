import logging

import sys
from math import atan2, cos, sin

from utils import Parser
from perceptron import Perceptron

if __name__ == '__main__':
    training_path = sys.argv[1]
    facit_path = sys.argv[2]

    test_path = sys.argv[3]

    parser = Parser()
    training_images = parser.parse_training_images(training_path, facit_path)

    """   
    for image in training_images:
        row_count = len(training_images[0].pixels)
        if row_count != 20:
            raise Exception('Parsing problem. Image with {} rows of pixels instead of 20'.format(row_count))
        else:
            for row in training_images[0].pixels:
                row_pixels_count = len(row)
                if row_pixels_count != 20:
                    raise Exception(
                        'Parsing problem. Image with a row of {} pixels instead of 20'.format(row_pixels_count))
    """

    quarters_indexes = [(0, 0), (0, 1), (1, 1), (1, 0)]

    #rotate all the images depending on the eyebrows
    for image in training_images:
        pixels = image.pixels
        maximums = []
        maximums_ind = []

        for quarter_indexes in quarters_indexes:
            a, b = quarter_indexes
            maximum = 0
            max_i = 0
            max_j = 0
            #cut the image pixels in 4 submatrices
            for i in range(a * 10 + 1, (a + 1) * 10 - 1):  # row indexes
                for j in range(b * 10 + 1, (b + 1) * 10 - 1):  # col indexes
                    #calc mask
                    sum = 0
                    sum += pixels[i - 1][j - 1]
                    sum += pixels[i][j - 1]
                    sum += pixels[i + 1][j - 1]
                    sum += pixels[i - 1][j]
                    sum += pixels[i][j]
                    sum += pixels[i + 1][j]
                    sum += pixels[i - 1][j + 1]
                    sum += pixels[i][j + 1]
                    sum += pixels[i + 1][j + 1]
                    if (sum > maximum):
                        maximum = sum
                        max_i = i
                        max_j = j
            maximums.append(maximum)
            maximums_ind.append((max_i, max_j))

        #get maximum mask center
        max1 = max(maximums)
        max_index1 = maximums.index(max1)
        #delete first maximum mask center
        maximums[max_index1] = 0

        #get second maximum mask center
        max2 = max(maximums)
        max_index2 = maximums.index(max2)

        #get the angle from first to second mask center
        point1 = maximums_ind[max_index1]
        point2 = maximums_ind[max_index2]
        alpha = atan2((20 - point2[0]) - (20 - point1[0]), point2[1] - point1[1])

        #create new pixels
        rotated_pixels = []
        for i in range(20):
            row = []
            for j in range(20):
                row.append(0)
            rotated_pixels.append(row)

        #
        for i in range(20):
            for j in range(20):
                rotated_j = int(cos(alpha) * j - sin(alpha) * (20 - i))
                rotated_i = (int(sin(alpha) * j + cos(alpha) * (20 - i)))
                #original corners are lost and become white
                if (0 <= rotated_i < 20) and (0 <= rotated_j < 20):
                    rotated_pixels[rotated_i][rotated_j] = pixels[i][j]

        image.pixels = rotated_pixels

    perceptron = Perceptron(training_images)

    test_images = parser.parse_test_images(test_path)

    perceptron.classify_images(test_images)
