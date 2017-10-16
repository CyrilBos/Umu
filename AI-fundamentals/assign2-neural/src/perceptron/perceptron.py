from logging import getLogger
from random import randrange

from .input_node import InputNode

from .link import Link
from .output_node import OutputNode
from .fixed_input_node import FixedInputNode

from utils import Emotion


class Perceptron:
    def __init__(self, images, training_proportion=0.66, learning_rate=0.1, input_nodes_count=400):
        self._output_nodes = []
        self._learning_rate = learning_rate
        training_images_len = int(training_proportion * len(images))

        #create one output node for each emotion
        for i in range(len(Emotion.emotions_list)):
            output_node = OutputNode(emotion=Emotion(i))

            #create the link between the output node and the fixed input node with a constant pixel value of 1
            fixed_input = FixedInputNode(fixed_pixel_value=1)
            output_node.input_links.append(Link(fixed_input, weight=1))

            self._output_nodes.append(output_node)

        for i in range(input_nodes_count):
            input_node = InputNode(pixel_ind=i)
            #create the link between that input node and every output node
            for output_node in self._output_nodes:
                output_node.input_links.append(Link(input_node, weight=1))

        training_images = images[:training_images_len]
        evaluation_images = images[training_images_len:]
        images_length = len(training_images)

        iteration = 0
        print(iteration)
        while self.train(images_length, training_images, evaluation_images) < 65:
            training_images = images[:training_images_len]
            evaluation_images = images[training_images_len:]
            iteration+=1
            print(iteration)

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
            if guess == evaluation_image.emotion:
                success += 1
        accuracy = success / len(evaluation_images) * 100

        print('Performance: {}.3%'.format(accuracy))
        return accuracy

    def learn(self, image):
        for output_node in self._output_nodes:
            desired_output = output_node.emotion == image.emotion
            activation_level = output_node.get_activation_level(image)
            error = desired_output - activation_level
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
            print('Image {}: {})'.format(index, emotion.value + 1))
