import sys

import image_preprocessing
from perceptron import Perceptron
from parser import Parser

if __name__ == '__main__':
    training_path = sys.argv[1]
    facit_path = sys.argv[2]

    test_path = sys.argv[3]

    parser = Parser()
    training_images = parser.parse_training_images(training_path, facit_path)

    image_preprocessing.blur_images(training_images)
    image_preprocessing.rotate_images(training_images)

    perceptron = Perceptron(training_images)

    test_images = parser.parse_test_images(test_path)

    image_preprocessing.blur_images(test_images)
    image_preprocessing.rotate_images(test_images)

    perceptron.classify_images(test_images)
