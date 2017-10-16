from logging import getLogger
from random import randrange

from .input_node import InputNode

from .link import Link
from .output_node import OutputNode
from .fixed_input_node import FixedInputNode

from utils import Emotion

logger = getLogger('perceptron')


class Perceptron:
    _output_nodes = []

    def __init__(self, images, input_nodes_count=400, training_proportion=0.66, learning_rate=0.5):
        self._learning_rate = learning_rate
        training_images_len = int(training_proportion * len(images))

        for i in range(len(Emotion.emotions_list)):
            output_node = OutputNode(emotion=Emotion(i))
            fixed_pixel = FixedInputNode(fixed_pixel_value=1)
            output_node.input_links.append(Link(fixed_pixel, weight=0.5))

            self._output_nodes.append(output_node)

        for i in range(input_nodes_count):
            #TODO: divide image matrix in even submatrices
            input_node = InputNode(pixels_ind=[i])
            for output_node in self._output_nodes:
                output_node.input_links.append(Link(input_node, weight=0.5))

        training_images = images[:training_images_len]
        evaluation_images = images[training_images_len:]
        images_length = len(training_images)

        while self.train(images_length, training_images, evaluation_images) < 80:
            print(len(training_images))
            training_images = images[:training_images_len]
            evaluation_images = images[training_images_len:]
            print(len(training_images))


    def train(self, images_length, training_images, evaluation_images):
        # Learning
        while images_length > 0:
            i = randrange(images_length)
            image = training_images[i]

            self.learn(image)

            del training_images[i]
            images_length -= 1

        # Performance evaluation
        success = 0

        for evaluation_image in evaluation_images:
            guess = self.predict(evaluation_image)
            success += guess == evaluation_image.emotion
        accuracy = success / len(evaluation_images) * 100

        print('success = {}'.format(success))
        print('Accuracy: {}'.format(accuracy))
        return accuracy


    def learn(self, image):
        for output_node in self._output_nodes:
            desired_output = output_node.emotion == image.emotion
            error = desired_output - output_node.get_activation_level(image)
            if error:
                for link in output_node.input_links:
                    delta = self._learning_rate * error * link.input_node.get_activation_level(image)
                    link.weight += delta

    def predict(self, image):
        """
        :param image: new image to test
        :return:
        """
        max = self._output_nodes[0].get_activation_level(image)
        max_index = 0
        for i in range(1, len(self._output_nodes)):
            activation_level = self._output_nodes[i].get_activation_level(image)
            if activation_level > max:
                max = activation_level
                max_index = i
        return self._output_nodes[max_index].emotion

    def classify_images(self, images):
        index = 1
        for image in images:
            emotion = self.predict(image)
            print('Image {}: {})'.format(index, emotion.value+1))


