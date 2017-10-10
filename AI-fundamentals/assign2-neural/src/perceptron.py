from math import sqrt

from .output_node import OutputNode
from .input_node import InputNode

from .link import Link

from utils.image import ROW_WIDTH

from utils.emotion import emotions, Emotion

from random import randrange

from logging import getLogger

logger = getLogger('perceptron')


class Perceptron:
    _output_nodes = []

    def __init__(self, images, input_nodes_count=400, training_proportion=0.66, learning_rate=0.05):
        self._learning_rate = learning_rate
        training_images = images[:training_proportion]
        evaluation_images = images[training_proportion + 1:]

        for emotion_str in emotions:
            self._output_nodes.append(OutputNode(threshold=0.5, emotion=emotion_str))

        for i in range(input_nodes_count):
            #TODO: divide image matrix in even submatrices
            input_node = InputNode(pixels_ind=[i], threshold=0.5)
            for output_node in self._output_nodes:
                output_node.input_links.append(Link(input_node))

        images_length = len(training_images)

        # Learning
        while images_length > 0:
            i = randrange(images_length)
            image = training_images[i]

            self.learn(image)

            training_images.remove(i)
            images_length -= 1

        # Performance evaluation
        success = 0

        for evaluation_image in evaluation_images:
            success += (self.guess_emotion(evaluation_image) == evaluation_image.emotion)

        logger.info('Accuracy: {}%'.format(success / len(evaluation_images)) * 100)

    def learn(self, image):
        for output_node in self._output_nodes:
            desired_output = output_node.emotion == image.emotion
            error = desired_output - output_node.is_activated()
            if error:
                for link in output_node.input_links:
                    delta = self._learning_rate * error * link.input_node.output(image)
                    link.weight += delta

    def guess_emotion(self, image):
        """
        :param image: new image to test
        :return:
        """
        for output_node in self._output_nodes:
            if output_node.is_activated(image):
                return emotions[output_node.emotion]
