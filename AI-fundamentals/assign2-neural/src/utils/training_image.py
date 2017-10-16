from .image import Image
from .emotion import Emotion


class TrainingImage(Image):
    def __init__(self, pixels, emotion_value):
        super().__init__(pixels)
        self.__emotion = Emotion(emotion_value)

    def __str__(self) -> str:
        return super().__str__() + '\nEmotion: ' + self.__emotion.__str__()

    @property
    def emotion(self):
        return self.__emotion

    def get_contrasted_image(self):
        return TrainingImage(self._get_contrasted_pixels(), self.__emotion)
