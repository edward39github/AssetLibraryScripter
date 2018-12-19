

class TextureManager(object):

    def __init__(self):
        """
        This class provide functions for texture type parsing.

        property "textureSamples": <dict> containing sample names for each type of
                                    supported texture "texture_type": ["sample", ...]}
                                    ( i.e. { "albedo": [ 'Diffuse', 'diffuseColor' ] } )
        """
        super(TextureManager, self).__init__()

        self.samples = {}
        self._string = ""


    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, string):
        if not isinstance(string, str):
            raise TypeError("Expected < str >")

        self._string = string


    def typeFromString(self, mode):
        """
        Parse string and try to find texture type

        :param mode: < int > search mode
            0 - (in all types) use only texture types
            1 - (in all samples per type) use only texture samples
            2 - (in all types and after in all samples per type) try find in ALL types, if did not, try find in samples per type
            3 - (for each type and its samples) iterate by types. if not coincidence, iterate from samples of current type

        :return: < string >
        """

        if not self._string: return ""


        if mode == 0:
            for type in self.samples:
                if self._string.find(type) != -1:
                    return type
            return ""

        elif mode == 1:
            for type in self.samples:
                for sample in self.samples[type]:
                    if self._string.find(sample) != -1:
                        return type

        elif mode == 2:
            for type in self.samples:
                if self._string.find(type) != -1:
                    return type
            for type in self.samples:
                for sample in self.samples[type]:
                    if self._string.find(sample) != -1:
                        return type

        else:
            for type in self.samples:
                if self._string.find(type) != -1:
                    return type
                else:
                    for sample in self.samples[type]:
                        if self._string.find(sample) != -1:
                            return type

        return ""


