import json
from maths import Vector
from maths import Quaternion


class Path:
    def __init__(self, filename):
        # Load the path from a file and convert it into a list of coordinates
        self.loadPath(filename)
        self.vecPath = self.positionPath(dict=True)

    def loadPath(self, file_name):
        with open(file_name) as path_file:
            data = json.load(path_file)

        self.path = data

    def positionPath(self, dict=False):
        if dict:
            return [{'X': p['Pose']['Position']['X'],
                     'Y': p['Pose']['Position']['Y'],
                     'Z': p['Pose']['Position']['Z']}
                    for p in self.path]
        else:
            return [Vector.from_dict(p['Pose']['Position'])
                    for p in self.path]

    def orientationPath(self, dict=False):
        if dict:
            return [{'W': p['Pose']['Orientation']['W'],
                     'X': p['Pose']['Orientation']['X'],
                     'Y': p['Pose']['Orientation']['Y'],
                     'Z': p['Pose']['Orientation']['Z']} for p in self.path]
        else:
            return [Quaternion(p['Pose']['Orientation']['W'],
                               Vector(p['Pose']['Orientation']['X'],
                                      p['Pose']['Orientation']['Y'],
                                      p['Pose']['Orientation']['Z']))
                    for p in self.path]
