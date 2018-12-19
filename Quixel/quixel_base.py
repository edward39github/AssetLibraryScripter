from __future__ import print_function


from Core.CommonFunctionality import CommonFunctions
from Core.StringParser import StringParser
from Core.TextureManagement import TextureManager
from Core.ArchivesManager import ArchiveFileManager
from Core.InfoFileManagement import InfoRecord, InfoRecordGroup
from Core.ImageProcessing import ImageProcessor
from Core.NameConvention import NamesConventionTextures as NCTextures
from Core.NameConvention import NamesConventionInfo as NCInfo

import tempfile
import sys
import os



class QuiexelAssetTypes(object):
    Atlas = "atlas"
    Model3D = "3d"
    Plant3D = "3dplant"
    Surface = "surface"



class QuixelBase(object):

    def __init__(self):
        super(QuixelBase, self).__init__()

        # asset attributes

        self._assetFileName     = ""                            # name of asset parsed from asset path
        self._assetFileArchive  = ""                            # path to asset archive
        self._assetType         = ""                            # type if quixel asset ( 3dplant, surface ... )
        self._assetVendorData   = None                          # data from asset .json info file
        self._quixelAssetTypes = [
            QuiexelAssetTypes.Surface,
            QuiexelAssetTypes.Model3D,
            QuiexelAssetTypes.Plant3D,
            QuiexelAssetTypes.Atlas
        ]

        # info groups

        self._infoGroupGlobal       = InfoRecordGroup()             # main info group for info.json file
        self._infoGroupColor        = InfoRecordGroup()             # color info group for info.json file
        self._infoGroupRegion       = InfoRecordGroup()             # region info group for info.json file
        self._infoGroupTextures     = InfoRecordGroup()             # texture info group for info.json file
        self._infoGroupMesh         = InfoRecordGroup()             # geometry info group for info.json file
        self._infoGroups            = []                            # list of all info groups

        self._infoGroupGlobal.name      = NCInfo.GroupGlobal
        self._infoGroupRegion.name      = NCInfo.GroupRegion
        self._infoGroupColor.name       = NCInfo.GroupColor
        self._infoGroupTextures.name    = NCInfo.GroupTextures
        self._infoGroupMesh.name        = NCInfo.GroupMesh


        # managers

        self._commonFunc        = CommonFunctions()
        self._textureManager    = TextureManager()
        self._archiveManager    = ArchiveFileManager()
        self._imageProcessor    = ImageProcessor()
        self._stringParser      = StringParser()

        self._textureManager.samples = {
            NCTextures.Displacement:   ["Displacement"],
            NCTextures.NormalDetail:   ["NormalBump"],
            NCTextures.Glossiness:     ["Gloss"],
            NCTextures.Roughness:      ["Roughness"],
            NCTextures.Specular:       ["Specular"],
            NCTextures.Opacity:        ["Opacity"],
            NCTextures.Normal:         ["Normal"],
            NCTextures.Albedo:         ["Albedo"],
            NCTextures.Cavity:         ["Cavity"],
            NCTextures.Mask:           ["Fuzz"],
            NCTextures.SSS:            ["Translucency"],
            NCTextures.AO:             ["AO"]
        }




    # **************** SETTERS / GETTERS *****************#

    @property
    def assetArchive(self):
        return self._assetFileArchive


    @property
    def assetType(self):
        return self._assetType


    @assetArchive.setter
    def assetArchive(self, path):
        if not isinstance(path, str):
            raise TypeError("Expected < str >")

        if not self._archiveManager.isArchive(path):
            raise StandardError(path + " is not archive")

        self._initAsset(path)




    # **************** PRIVATE METHODS *****************#

    def _collecVendorInfo(self):
        try:
            info = self._assetVendorData["tags"]
            record = InfoRecord(NCInfo.GlobalTags)
            record.setValueStringList([info])
            self._infoGroupGlobal.addRecord(record)
        except:
            pass

        try:
            info = self._assetVendorData["environment"]["biome"].replace("-", " ")
            record = InfoRecord(NCInfo.GlobalSet)
            record.setValueStringList([info])
            self._infoGroupGlobal.addRecord(record)
        except:
            pass

        try:
            info = self._assetVendorData["averageColor"]
            record = InfoRecord(NCInfo.ColorAvg)
            record.setValueColor(info)
            self._infoGroupColor.addRecord(record)
        except:
            pass

        try:
            info = self._assetVendorData["environment"]["region"]
            record = InfoRecord(NCInfo.RegionLocation)
            record.setValueString(info)
            self._infoGroupRegion.addRecord(record)
        except:
            pass


        if self._assetType == QuiexelAssetTypes.Surface:
            for item in self._assetVendorData["meta"]:
                if item["key"] == "tileable":
                    try:
                        record = InfoRecord(NCInfo.TexturesTileable)
                        record.setValueBool(item["value"])
                        self._infoGroupTextures.addRecord(record)
                        break
                    except:
                        break

            for item in self._assetVendorData["components"]:
                if item["type"] == "displacement":
                    try:
                        record = InfoRecord(NCInfo.TexturesDispRange)
                        min = item["minIntensity"] / 256
                        max = item["maxIntensity"] / 256
                        record.setValueRangeFloat((min, max))
                        self._infoGroupTextures.addRecord(record)
                        break
                    except:
                        break





    def _initAsset(self, path):

        # setup default parameters

        self._assetFileArchive = path
        self._assetFileName = os.path.basename(path)
        self._assetFileName = os.path.splitext(self._assetFileName)[0]
        self._archiveManager.archiveFile = path



        # load asset .json info file

        self._archiveManager.open()

        try:
            name = self._archiveManager.content(["json"])[0]
            self._archiveManager.extractMember(
                directory=tempfile.gettempdir(),
                name=name
            )

            filepath = os.path.join(tempfile.gettempdir(), name)

            self._assetVendorData = self._commonFunc.loadFromJSON(filepath)
            os.remove(filepath)

            self._archiveManager.close()
            self._collecVendorInfo()
        except:
            print(
                self.__class__.__name__ + ": Asset" + path + "has not .json info file",
                file=sys.stderr
            )

        self._archiveManager.close()



        # parse categories and group info from asset name

        sepnames = self._assetFileName.split("_")

        record = InfoRecord(NCInfo.GlobalCategory)
        record.setValueStringList([sepnames[0]])
        self._infoGroupGlobal.addRecord(record)

        if len(sepnames) > 5:
            record = InfoRecord(NCInfo.GlobalGroup)
            record.setValueStringList([sepnames[1]])
            self._infoGroupGlobal.addRecord(record)

        record = InfoRecord(NCInfo.GlobalName)
        record.setValueString("")
        self._infoGroupGlobal.addRecord(record)


        # parse asset type

        for asset_type in self._quixelAssetTypes:
            t = "_"+asset_type
            if t in self._assetFileName:
                self._assetType = asset_type
                break


    def _saveInfoData(self, directory):
        self._infoGroups.insert(0, self._infoGroupGlobal)
        self._infoGroups.insert(1, self._infoGroupRegion)
        self._infoGroups.insert(2, self._infoGroupColor)

        data = []

        for group in self._infoGroups:
            data.append(group.toDict())

        self._commonFunc.saveToJSON(
            obj=data,
            path=os.path.join(directory, "info.json")
        )


    def _extractPreview(self, directory, newname="preview"):
        for name in self._archiveManager.content():
            if name.find("Preview") != -1:
                self._archiveManager.extract(directory, {name: newname})
                break



    #**************** PUBLIC METHODS *******************#

    def clearAssetArchive(self):
        self._archiveManager.clear()

        self._assetFileName = ""
        self._assetFileArchive = ""
        self._assetType = ""
        self._assetVendorData = None
        self._infoGroupGlobal = InfoRecordGroup()


    def setCategories(self, categories=[""]):
        record = InfoRecord(NCInfo.GlobalCategory)
        record.setValueStringList(categories)
        self._infoGroupGlobal.changeRecord(NCInfo.GlobalCategory, record)


    def setGroups(self, groups=[""]):
        record = InfoRecord(NCInfo.GlobalGroup)
        record.setValueStringList(groups)
        self._infoGroupGlobal.changeRecord(NCInfo.GlobalGroup, record)


    def setSets(self, sets=[""]):
        record = InfoRecord(NCInfo.GlobalSet)
        record.setValueStringList(sets)
        self._infoGroupGlobal.changeRecord(NCInfo.GlobalSet, record)


    def setName(self, name=""):
        record = InfoRecord(NCInfo.GlobalName)
        record.setValueString(name)
        self._infoGroupGlobal.changeRecord(NCInfo.GlobalName, record)




class QuixelSurface(QuixelBase):

    def __init__(self):
        super(QuixelSurface, self).__init__()

        record = InfoRecord(NCInfo.TexturesAtlas)
        record.setValueBool(False)

        self._infoGroupTextures = InfoRecordGroup()
        self._infoGroupTextures.name = NCInfo.GroupTextures
        self._infoGroupTextures.addRecord(record)



    def _collecVendorInfo(self):

        super(QuixelSurface, self)._collecVendorInfo()

        if not self._assetVendorData: return

        for item in self._assetVendorData["meta"]:
            if item["key"] == "tileable":
                try:
                    record = InfoRecord(NCInfo.TexturesTileable)
                    record.setValueBool(item["value"])
                    self._infoGroupTextures.addRecord(record)
                    break
                except:
                    break

        for item in self._assetVendorData["components"]:
            if item["type"] == "displacement":
                try:
                    record = InfoRecord(NCInfo.TexturesDispRange)
                    min = item["minIntensity"]/256
                    max = item["maxIntensity"]/256
                    record.setValueRangeFloat((min, max))
                    self._infoGroupTextures.addRecord(record)
                    break
                except:
                    break


    def saveInfoData(self, directory):
        self._infoGroups.append(self._infoGroupTextures)
        self._saveInfoData(directory)



    def extract(self, directory):
        namemap = {}

        self._archiveManager.open()

        for name in self._archiveManager.content(["png", "jpg", "jpeg", "exr"]):

            if name.find("Preview") != -1:
                namemap[name] = "preview"
                continue

            self._textureManager.string = str(name)
            textype = self._textureManager.typeFromString(3)

            if not textype: continue

            namemap[name] = textype

        self._archiveManager.extract(directory, namemap)
        self._archiveManager.close()



    def isBillboardTexture(self, string):
        """
        If string is billboard texture return True, otherwise False
        :param string: texture name (or file name, preferably not full name)
        :return: bool
        """

        if string.find("Billboard") != -1:
            return True
        return False


    def billboardMap(self, prefix='billboard_'):
        """
        Create list of dicts [{archived_file_name: billboard_type}, ...]
        (i.e.
        [
            {"Billboard_4K_Albedo.jpg": "albedo"},
            {"Billboard_4K_Normal.jpg": "normal"},
            ...
        ]
        :return: list
        """

        schemes = []

        is_opened = self._archiveManager.isOpened

        if not is_opened: self._archiveManager.open()

        for name in self._archiveManager.content():
            if not self.isBillboardTexture(name):
                continue

            self._textureManager.string = name
            texture_type = self._textureManager.typeFromString(3)
            schemes.append(
                { name: prefix+texture_type }
            )

        return schemes


if __name__ == '__main__':

    src = "D:/quixel_download/Quixel Megascans/surface/construction/Concrete_Damaged_Base_pjttH20_2K_surface_ms.zip"
    dst = "C:/Users/edward/Desktop/quixel"

    qsurf = QuixelSurface()
    qsurf.assetArchive = src
    qsurf.extract(dst)
    qsurf.saveInfoData(dst)
