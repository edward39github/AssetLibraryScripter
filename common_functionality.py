import json
import os
import numpy
import cv2 as cv
from colormap import rgb2hex
from datetime import datetime
from PySide.QtCore import QRegExp, Qt




class CommonFunctionality(object):

    def __init__(self):
        """
        This class provide common functions.

        property "textureSamples": <dict> containing sample names for each type of
                                    supported texture "texture_type": ["sample", ...]}
                                    ( i.e. { "Albedo": [ 'Diffuse', 'diffuseColor' ] } )
        """
        super(CommonFunctionality, self).__init__()

        self.textureSamples = {}

        self.textureExtensions = ["jpg", "jpeg", "tif", "tiff", "tga", "exr", "png"]

        self.geometryExtensions = ["fbx", "obj"]

        self.LODRegExpPattern = "LOD[0-9]*[0-9]"

        self.variationRegExpPattern = "VAR[0-9]*[0-9]"

        self.resolutionsMap = {
            "1K": 1024, "2K": 2048,
            "3K": 3072, "4K": 4096,
            "5K": 5120, "6K": 6144,
            "7K": 7168, "8K": 8196
        }

        self.assetClasses = ["nature", "city", ]



    def saveToJSON(self, obj, path):
        f = open(path, "w")
        json.dump(obj, f, indent=4)
        f.close()



    def uniqueID(self):
        return datetime.now().strftime('%Y%m%d%H%M%S%f')



    def isMatchedWithExtensions(self, string, extensions=[]):
        extension = string.split(".")[-1]
        return extension in extensions



    def isImage(self, string):
        return self.isMatchedWithExtensions(string, self.textureExtensions)



    def isGeometry(self, string):
        return self.isMatchedWithExtensions(string, self.geometryExtensions)



    def extensionFromString(self, string):
        """
        Parse string and try to find file extension.
        :param string:
        :return: < string > file extension or empty
        """

        suffix = string.split(".")[-1]
        return suffix



    def textureTypeFromString(self, string, mode):
        """
        Parse string and try to find texture type

        :param string:

        :param mode <int>:
        0 - (in all types) use only texture types
        1 - (in all samples per type) use only texture samples
        2 - (in all types and after in all samples per type) try find in ALL types, if did not, try find in samples per type
        3 - (for each type and its samples) iterate by types. if not coincidence, iterate from samples of current type

        :return: < string >
        """


        if mode == 0:
            for type in self.textureSamples:
                if string.find(type) != -1:
                    return type
            return ""

        elif mode == 1:
            for type in self.textureSamples:
                for sample in self.textureSamples[type]:
                    if string.find(sample) != -1:
                        return type

        elif mode == 2:
            for type in self.textureSamples:
                if string.find(type) != -1:
                    return type
            for type in self.textureSamples:
                for sample in self.textureSamples[type]:
                    if string.find(sample) != -1:
                        return type

        else:
            for type in self.textureSamples:
                if string.find(type) != -1:
                    return type
                else:
                    for sample in self.textureSamples[type]:
                        if string.find(sample) != -1:
                            return type

        return ""



    def LODFromString(self, string, caseSense=True):

        rx = QRegExp(self.LODRegExpPattern)
        rx.setMinimal(False)
        rx.setCaseSensitivity(Qt.CaseInsensitive)
        if caseSense: rx.setCaseSensitivity(Qt.CaseSensitive)

        index = rx.indexIn(string)
        length = rx.matchedLength()

        match = string[index:index+length]

        return match



    def textureSizeFromString(self, string):
        for resolution in self.resolutionsMap:
            if string.find(resolution) != -1:
                res = self.resolutionsMap[resolution]
                return res, res



    def textureSizeFromFile(self, file_path):
        if not os.path.isfile(file_path):
            raise OSError(file_path + " is not a file")

        image = cv.imread(file_path, 0)
        shape = image.shape
        h = shape[0]
        w = shape[1]

        return w, h



    def textureSizeFromAnyFile(self, files_directory, extensions=["jpeg", "jpg", "tif", "tiff"]):
        if not os.path.isdir(files_directory):
            raise OSError(files_directory + " is not a directory")

        for f in os.listdir(files_directory):
            ext = self.extensionFromString(f)
            if ext in extensions:
                file = os.path.join(files_directory, f)
                image = cv.imread(file, 0)
                shape = image.shape
                h = shape[0]
                w = shape[1]
                return w, h

        return -1, -1



    def textureAverageColor(self, filepath):
        """
        Read image and get average color
        :param filepath: path to image file
        :return <string>:  hex format color
        """

        img = cv.imread(filepath, 1)
        avg_color_per_row = numpy.average(img, axis=0)
        r, g, b = numpy.average(avg_color_per_row, axis=0)

        r, g, b = int(r), int(g), int(b)

        return rgb2hex(r, g, b)



    def variationFromString(self, string, caseSense=True):
        rx = QRegExp(self.variationRegExpPattern)
        rx.setMinimal(False)
        rx.setCaseSensitivity(Qt.CaseInsensitive)
        if caseSense: rx.setCaseSensitivity(Qt.CaseSensitive)

        index = rx.indexIn(string)
        length = rx.matchedLength()

        match = string[index:index+length]

        return match



    def makeDefaultRecords(self, uniqid, tags, classes, categories,
                           groups, sets, companies, name, avg_color):
        """
        Create default records for asset

        :return: list
        """

        return [
            {
                "key": "id",
                "name": "ID",
                "type": "string",
                "value": uniqid
            },
            {
                "key": "tags",
                "name": "Tags",
                "type": "list",
                "value": tags
            },
            {
                "key": "class",
                "name": "Class",
                "type": "list",
                "value": classes
            },
            {
                "key": "category",
                "name": "Category",
                "type": "list",
                "value": categories
            },
            {
                "key": "group",
                "name": "Group",
                "type": "list",
                "value": groups
            },
            {
                "key": "name",
                "name": "Name",
                "type": "string",
                "value": name
            },
            {
                "key": "company",
                "name": "Company",
                "type": "string",
                "value": companies
            },
            {
                "key": "set",
                "name": "Set",
                "type": "list",
                "value": sets
            },
            {
                "key": "color_avg",
                "name": "Average color",
                "type": "color",
                "value": avg_color
            },
        ]






if __name__ == '__main__':

    import zipfile

    cf = CommonFunctionality()
    root = r"D:\cg\library\materials\poliigon\surface\Rock\RockGrey008_hires\RockGrey008_COL_VAR1_HIRES.jpg"
    print(cf.textureAverageColor(root))
