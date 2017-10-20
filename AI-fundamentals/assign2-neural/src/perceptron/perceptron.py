from logging import getLogger
from random import randrange

from .input_node import InputNode

from .link import Link
from .output_node import OutputNode
from .fixed_input_node import FixedInputNode

from utils import Emotion

INPUT_NODES_COUNT = 400


class Perceptron:
    """
    Main class of the perceptron that ties everything together. The training is done in the initialization.
    """

    def __init__(self, images, training_proportion=0.66, learning_rate=0.1, min_iteration=15, max_iteration=100,
                 squared_error_mean_threshold=0.1):
        """
        Initializes a Perceptron with the given images and parameters.
        The training stops if max_iteration is reached or if min_iteration is reached and the mean of squared errors is
        below its threshold parameter.
        :param images: training set
        :type images: List[Image]
        :param training_proportion: proportion between 0 and 1 of images used for training
        :type training_proportion: float
        :param learning_rate: learning rate used when updating weights with the error
        :type learning_rate: float
        :param min_iteration: minimum number of training iterations
        :param max_iteration: maximum number of training iterations
        :param squared_error_mean_threshold: threshold to stop the training
        """
        self._output_nodes = []
        self._learning_rate = learning_rate
        training_images_len = int(len(images) * training_proportion)

        fixed_input = FixedInputNode(fixed_pixel_value=1)
        # create one output node for each emotion
        for i in range(len(Emotion.emotions_list)):
            output_node = OutputNode(emotion=Emotion(i))

            # create the link between the output node and the fixed input node with a constant pixel value of 1
            output_node.input_links.append(Link(fixed_input, weight=0))

            self._output_nodes.append(output_node)

        # create the 400 input nodes
        for i in range(INPUT_NODES_COUNT):
            input_node = InputNode(pixel_index=i)
            # create the link between that input node and every output node

            # create the 1600 links, 400 for each output node
            for output_node in self._output_nodes:
                output_node.input_links.append(Link(input_node, weight=0))

        # first training iteration
        training_images = images[:training_images_len]
        evaluation_images = images[training_images_len:]
        images_length = len(training_images)

        iteration = 0
        squared_error_mean, precision_score = self.train_step(training_images, evaluation_images, iteration)

        # Training loop until performance threshold or max number of iterations
        while iteration < min_iteration or (
                        squared_error_mean > squared_error_mean_threshold and iteration < max_iteration):
            # training_images and evaluation_images are randomly ordered by the train() method
            ##hence they get reset to their original state every iteration
            training_images = images[:training_images_len]
            evaluation_images = images[training_images_len:]
            squared_error_mean, precision_score = self.train_step(training_images, evaluation_images, iteration)
            iteration += 1

    def train_step(self, training_images, evaluation_images, iteration):
        """
        :param training_images: training set
        :param evaluation_images: performance evaluation set
        :param iteration: current iteration number
        :return: returns a tuple (sum of squared errors, percentage of correct classifications)
        """
        self.train(training_images)

        precision_score = self.evaluate_precision(evaluation_images)
        error_sum = self.check_error_performance(evaluation_images)

        print("# Iteration {}".format(iteration))
        print('# Percentage of correct classifications on evaluation set: {0:.3f}%'.format(precision_score))
        print('# error sum: {0:.3f}'.format(error_sum))
        return error_sum, precision_score

    def train(self, training_images):
        """
        Train on the image set, randomly picking one image then removing it from the set.
        :param training_images: images to train on
        :type training_images: List
        """
        # Learning
        images_length = len(training_images)
        while images_length > 0:
            i = randrange(images_length)
            image = training_images[i]

            self.learn(image)

            del training_images[i]
            images_length -= 1

    def learn(self, image):
        """
        Train on the image set, randomly picking one image then removing it from the set.
        :param image: image to learn from
        :type image: Image
        """
        for output_node in self._output_nodes:
            desired_output = output_node.emotion == image.emotion
            activation_level = output_node.get_activation_level(image)
            error = desired_output - activation_level
            for link in output_node.input_links:
                delta = self._learning_rate * error * link.input_node.get_activation_level(image)
                link.weight += delta

    def evaluate_precision(self, evaluation_images):
        """
        Computes and returns the percentage of correct classifications on the evaluation subset.
        :param evaluation_images: evaluation images set
        :return: returns the percentage of correct classifcations
        :rtype: float
        """
        #Calculate the mean of successful predictions
        success = 0
        for evaluation_image in evaluation_images:
            activated_output = self.predict(evaluation_image)
            if activated_output.emotion == evaluation_image.emotion:
                success += 1

        accuracy = success / len(evaluation_images) * 100
        return accuracy

    def check_error_performance(self, evaluation_images):
        """
        Computes and returns the mean of squared errors
        :param evaluation_images: evaluation subset
        :return: returns the mean of squared errors
        :rtype: float
        """
        error_sum = 0
        for image in evaluation_images:
            activated_output_node = self.predict(image)
            desired_output = activated_output_node.emotion == image.emotion
            error_sum += pow(desired_output - activated_output_node.get_activation_level(image), 2)

        return error_sum / len(evaluation_images)

    def predict(self, image):
        """
        Predicts the classification of an unknown image and returns the activated output node.
        :param image: new image to test
        :type image: Image
        :return: returns the activated output node
        :rtype: OutputNode
        """
        #Consider the first output node as the one with the biggest activation level
        max = self._output_nodes[0].get_activation_level(image)
        max_index = 0

        #check if there is another "more" activated output node
        for i in range(1, len(self._output_nodes)):
            activation_level = self._output_nodes[i].get_activation_level(image)
            if activation_level > max:
                max = activation_level
                max_index = i

        return self._output_nodes[max_index]

    def classify_images(self, images):
        """
        Classifies every image of the images set parameter and prints the result using the facit format.
        :param images: images set to classify
        """
        index = 1
        for image in images:
            emotion = self.predict(image).emotion
            print('Image{} {}'.format(index, emotion.value + 1))
