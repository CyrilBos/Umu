import sys; import pprint
pprint.pprint(sys.path)

from utils import Parser
from perceptron import Perceptron


from logging import getLogger



if __name__ == '__main__':
    logger = getLogger('perceptron')


    parser = Parser()
    training_images = parser.parse_training_images('training-data/training.txt', 'training-data/training-facit.txt')

    #TODO: make this a unit test
    for image in training_images:
        row_count = len(training_images[0].pixels)
        if  row_count != 20:
            raise Exception('Parsing problem. Image with {} rows of pixels instead of 20'.format(row_count))
        else:
            for row in training_images[0].pixels:
                row_pixels_count = len(row)
                if row_pixels_count != 20:
                    raise Exception('Parsing problem. Image with a row of {} pixels instead of 20'.format(row_pixels_count))


    perceptron = Perceptron(training_images)