import collections
import json
import os


def loadSet(name):
    """
    :param name: name of file are containing set of samples for texture type
                 (i.e. "quixel_materials" or "poliigon" )
    """

    path = os.path.join(__file__, "../", "Sets", name+".json")
    path = os.path.normpath(path)

    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data = collections.OrderedDict(data)
        return data
