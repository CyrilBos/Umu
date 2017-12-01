from image import Image
from emotion import Emotion


class TrainingImage(Image):
    """
    Inherits from Image to add an emotion field used in training and evaluation.
    """

    def __init__(self, pixels, emotion_value):
        """
        Intializes the TrainingImage with the parsed emotion value.
        :param pixels:
        :param emotion_value: int that codes the emotion in the range [0-4)
        :type emotion_value: int
        """
        super().__init__(pixels)
        self.__emotion = Emotion(emotion_value)

    def __str__(self) -> str:
        return super().__str__() + '\nEmotion: ' + self.__emotion.__str__()

    @property
    def emotion(self):
        return self.__emotion
