
from PySide.QtCore import QRegExp, Qt



class StringParser(object):

    def __init__(self):
        super(StringParser, self).__init__()

        self._string = ""
        self._regExp = QRegExp("LOD[0-9]*[0-9]", Qt.CaseSensitive)
        self._regExpLOD = QRegExp("LOD[0-9]*[0-9]", Qt.CaseSensitive)
        self._regExpVariation = QRegExp("VAR[0-9]*[0-9]", Qt.CaseSensitive)
        self._resolutionsMap = {
            "1K": 1024, "2K": 2048,
            "3K": 3072, "4K": 4096,
            "5K": 5120, "6K": 6144,
            "7K": 7168, "8K": 8196
        }



    @property
    def string(self):
        return self._string


    @property
    def regExpLOD(self):
        return self._regExpLOD


    @property
    def regExpVariation(self):
        return self._regExpVariation


    @property
    def regExp(self):
        return self._regExpVariation


    @string.setter
    def string(self, string):
        if not isinstance(string, str):
            raise TypeError("Expected < str >")

        self._string = string


    def clear(self):
        self._string = ""


    def resolutionFromString(self):
        for resolution in self._resolutionsMap:
            if self._string.find(resolution) != -1:
                res = self._resolutionsMap[resolution]
                return res, res


    def variation(self):
        index = self._regExpVariation.indexIn(self._string)
        length = self._regExpVariation.matchedLength()
        match = self._string[index:index + length]

        return match


    def LOD(self):
        index = self._regExpLOD.indexIn(self._string)
        length = self._regExpLOD.matchedLength()
        match = self._string[index:index + length]

        return match


    def find(self):
        """
        Find by pattern and return first
        """

        index = self._regExp.indexIn(self._string)
        length = self._regExp.matchedLength()
        match = self._string[index:index + length]

        return match


    def findAll(self):
        """
        Find by pattern and return all
        """

        index = 0
        matches = []

        while index >= 0:
            index = self._regExp.indexIn(self._string, index)
            length = self._regExp.matchedLength()
            print length
            match = self._string[index:index + length]
            index += length

            if match: matches.append(match)

        return matches


if __name__ == '__main__':
    testdir = "C:/UsersLOD12/edLOD15wardVAR3/Desktop4K/archtestLOD1"

    parser = StringParser()
    parser.string = testdir

    print parser.resolutionFromString()
    print parser.LOD()
    print parser.variation()

    print parser.findAll()


