import json
from datetime import datetime




class CommonFunctions(object):

    def __init__(self):
        """
        This class provide common functions.

        """
        super(CommonFunctions, self).__init__()


    def uniqueID(self):
        return datetime.now().strftime('%Y%m%d%H%M%S%f')


    def saveToJSON(self, obj, path):
        f = open(path, "w")
        json.dump(obj, f, indent=4)
        f.close()


    def loadFromJSON(self, path):
        f = open(path, "r")
        data = json.load(f)
        f.close()
        return data
