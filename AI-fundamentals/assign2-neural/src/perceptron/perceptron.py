from logging import getLogger
from random import randrange

from .input_node import InputNode

from .link import Link
from .output_node import OutputNode
from utils.emotion import emotions, Emotion

logger = getLogger('perceptron')


class Perceptron:
    _output_nodes = []

    def __init__(self, images, input_nodes_count=400, training_proportion=0.66, learning_rate=0.05):
        self._learning_rate = learning_rate
        training_images_len = int(training_proportion * len(images))

        for i in range(len(emotions)):
            self._output_nodes.append(OutputNode(threshold=0.5, emotion=Emotion(i)))

        for i in range(input_nodes_count):
            #TODO: divide image matrix in even submatrices
            input_node = InputNode(pixels_ind=[i], threshold=0.5)
            for output_node in self._output_nodes:
                output_node.input_links.append(Link(input_node, weight=1))

        training_images = images[:training_images_len]
        evaluation_images = images[training_images_len:]
        images_length = len(training_images)

        self.train(images_length, training_images, evaluation_images)#while <65: @Dorian mais c' est cassé
            #training_images = images[:training_images_len]
            #evaluation_images = images[training_images_len:]



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
            guess = self.guess_emotion(evaluation_image)
            if guess:#@Dorian ca arrive souvent que ca renvoit None parce que aucune output activee
                success += guess == evaluation_image.emotion
        accuracy = success / len(evaluation_images) * 100

        print('success = {}'.format(success))
        print('Accuracy: {}'.format(accuracy))
        return accuracy


    def learn(self, image):
        for output_node in self._output_nodes:
            desired_output = output_node.emotion == image.emotion
            error = desired_output - output_node.is_activated(image)
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
            activated = output_node.is_activated(image)
            if activated:
                return output_node.emotion
        #@Dorian aucun output activé c'est caca
