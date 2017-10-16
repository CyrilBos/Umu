import logging

import sys
from utils import Parser
from perceptron import Perceptron

logger = logging.getLogger('perceptron')
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    training_path = sys.argv[1]
    facit_path = sys.argv[2]

    test_path = sys.argv[3]

    parser = Parser()
    logger.info('Parsing images')
    training_images = parser.parse_training_images(training_path, facit_path)

    # TODO: make this a unit test
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

    perceptron = Perceptron(training_images)

    test_images = parser.parse_test_images(test_path)

    perceptron.classify_images(test_images)
