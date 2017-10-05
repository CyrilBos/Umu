import re


class Parser:
    def __init__(self):
        pass

    def parse_training_images(self, filepath):
        images = []
        training_file = open(filepath, 'r')

        cur_index = -1

        for line in training_file:
            if re.match('#.*', line):
                break
            elif re.match('Image\d*', line):
                images.append([])
                cur_index += 1
            elif re.match('(\d )*', line):
                for

        training_file.close()

        facit_file = open(filepath, 'r')
        for line in facit_file:
            if re.match():


        return images