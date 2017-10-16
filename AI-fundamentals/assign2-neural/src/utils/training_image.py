from .image import Image
from .emotion import Emotion

class TrainingImage(Image):
    def __init__(self, pixels, emotion_value):
        super().__init__(pixels)
        self.__emotion = Emotion(emotion_value)

    def __str__(self):
        return super(TrainingImage, self).__str__() + 'Emotion: ' + self.__emotion.__str__()

    @property
    def emotion(self):
        return self.__emotion