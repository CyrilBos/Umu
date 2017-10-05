from .Parser import Parser

parser = Parser()
training_images = parser.parse_training_images('training.txt')
