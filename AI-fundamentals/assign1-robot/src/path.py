import json

class Path:

    def __init__(self):
    # Load the path from a file and convert it into a list of coordinates
        self.loadPath('Path-around-table-and-back.json')
        self.vecPath = self.vectorizePath()
    
    def loadPath(self, file_name):
    
        with open(file_name) as path_file:
            data = json.load(path_file)
    
        self.path = data
    
    def vectorizePath(self):
        vecArray = [{'X': p['Pose']['Position']['X'], \
                     'Y': p['Pose']['Position']['Y'], \
                     'Z': p['Pose']['Position']['Z']}\
                     for p in self.path]
        return vecArray
