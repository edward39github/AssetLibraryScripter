
import os
import common_functionality
import zipfile as ZF
import shutil
import tempfile



class QuixelParser(common_functionality.CommonFunctionality):

    def __init__(self):
        super(QuixelParser, self).__init__()

        self.textureSamples = {
            "ao": ["AO"],
            "albedo": ["Albedo"],
            "cavity": ["Cavity"],
            "displacement": ["Displacement"],
            "glossiness": ["Gloss"],
            "normal_detail": ["NormalBump"],
            "normal": ["Normal"],
            "roughness": ["Roughness"],
            "specular": ["Specular"],
            "fuzz": ["Fuzz"],
            "sss": ["Translucency"],
            "opacity": ["Opacity"]
        }
        self.assetTypes = ["atlas", "surface", "3d", "3dplant"]

        self.asset3DConstraints = {
            "textureLODs": ["LOD0"]
        }




    def getValueFromJSONInfoDispRange(self, jsondata):
        try:
            comp = jsondata["components"]
            for d in comp:
                if d["type"] == "displacement":
                    min = d["minIntensity"]
                    max = d["maxIntensity"]
                    return min, max
        except:
            return 0, 0



    def getValueFromJSONInfoTileable(self, jsondata):
        try:
            tileable = False
            meta = jsondata["meta"]
            for d in meta:
                if d["key"] != "tileable": continue

                tileable = d["value"]
                if isinstance(tileable, str):
                    if tileable.lower() == "true":
                        tileable = True
                    else:
                        tileable = False
        except:
            tileable = False

        return tileable



    def getValueFromJSONInfoTags(self, jsondata):
        return jsondata["tags"]



    def getValueFromJSONInfoBiome(self, jsondata):
        return jsondata["environment"]["biome"].replace("-", "_")



    def getValueFromJSONInfoRegion(self, jsondata):
        return jsondata["environment"]["region"]



    def getValueFromJSONInfoAvgColor(self, jsondata):
        return jsondata["averageColor"]



    def getValueFromJSONInfoMeshes(self, jsondata):

        meshes = jsondata["meshes"]
        data = {}
        for record in meshes:
            if record["type"] != "lod": continue
            lod = self.LODFromString(record["uris"][0]["uri"])
            tris = record["tris"]
            data[lod] = tris

        return data



    def getGroupAndCategoryFromZipName(self, zip_file_name):
        sepnames = zip_file_name.split("_")
        category = [sepnames[0]]
        group = []

        if len(sepnames) > 5:
            group = [sepnames[1]]

        return category, group



    def getInfoFromZip(self, zipobj: ZF.ZipFile, classes:list, name: str):
        """
        Collect some info from Quixel asset json info file

        :param zipobj: zipfile.ZipFile() object of Quixel asset zip file
        :return: dict
        """

        if not isinstance(zipobj, ZF.ZipFile):
            raise TypeError("Expected < zipfile.ZipFile > type object")


        data = {}
        jsonfile = ""
        filename = os.path.basename(zipobj.filename)


        # search and extract inso json file

        for n in zipobj.namelist():
            if not self.isMatchedWithExtensions(n, "json"): continue
            zipobj.extract(n, tempfile.gettempdir())
            jsonfile = os.path.join(tempfile.gettempdir(), n)
            data = json.load(open(jsonfile ))

        os.remove(jsonfile)

        if not data: return data


        # extract data from json file

        category, group = self.getGroupAndCategoryFromZipName(filename)
        width, height = self.textureSizeFromString(filename)
        tags = self.getValueFromJSONInfoTags(data)
        biome = self.getValueFromJSONInfoBiome(data)
        region = self.getValueFromJSONInfoRegion(data)
        tileable = self.getValueFromJSONInfoTileable(data)
        averageColor = self.getValueFromJSONInfoAvgColor(data)
        disp_min, disp_max = self.getValueFromJSONInfoDispRange(data)



        info = {
            "id": self.uniqueID(),
            "tileable": tileable,
            "width": width,
            "height": height,
            "company": ["Quixel"],
            "name": name,
            "class": classes,
        }

        if tags: info["tags"] = tags
        if biome: info["set"] = biome,
        if region: info["region"] = region,
        if disp_min: info["displacement_min"] = disp_min
        if disp_max: info["displacement_max"] = disp_max
        if averageColor: info["average_color"] = averageColor

        return info



    def isPreview(self, string):
        """
        If string is preview for asset return True, otherwise False
        :param string: file name
        :return: bool
        """

        if self.isImage(string):
            if string.find("Preview") != -1:
                return True
        return False



    def isAlphaBrush(self, string):
        """
        Parse string to find if its alpha brush.
        :param string:
        :return: bool
        """

        return string.find("Brush") != -1



    def isHiresGeometry(self, string):
        """
        Parse string and try to find if its hires geo.
        :param string:
        :return: bool
        """

        if not self.isGeometry(string): return False
        return string.find("High") != -1



    def isBillboardTexture(self, string):
        """
        If string is billboard texture return True, otherwise False
        :param string: texture name (or file name, preferably not full name)
        :return: bool
        """

        if self.isImage(string):
            if string.find("Billboard") != -1:
                return True
        return False



    def determineQuixelAssetType(self, string):
        """
        Determine the type of Quixel asset from string
        :param string: asset name (or file name, preferably not full name)
        :return: str
        """

        for type in self.assetTypes:
            t = "_"+type
            if t in string:
                return type
        return ""



    def textureMapFromZip(self, zipobj):
        """
        Create list of tuples [(archived_file_name, texture_type), ...]
        (i.e.
        [
            ("olzmD_4K_Albedo.jpg", "albedo"),
            ("olzmD_4K_Normal.jpg", "normal"),
            ...
        ]
        :param zipobj: zipfile.ZipFile() object
        :return: list
        """
        if not isinstance(zipobj, ZF.ZipFile):
            raise TypeError("Expect zipfile.ZipFile() object")

        namesMap = []

        for name in zipobj.namelist():

            if self.isBillboardTexture(name): continue

            texture_type = self.textureTypeFromString(name, 3)

            if not texture_type: continue

            namesMap.append((name, texture_type))

        return namesMap



    def billboardMapFromZip(self, zipobj):
        """
        Create list of tuples [(archived_file_name, billboard_type), ...]
        (i.e.
        [
            ("Billboard_4K_Albedo.jpg", "albedo"),
            ("Billboard_4K_Normal.jpg", "normal"),
            ...
        ]
        :param zipobj: zipfile.ZipFile() object
        :return: list
        """
        if not isinstance(zipobj, ZF.ZipFile):
            raise TypeError("Expect zipfile.ZipFile() object")

        namesMap = []

        for name in zipobj.namelist():

            if not self.isBillboardTexture(name): continue

            texture_type = self.textureTypeFromString(name, 3)

            if not texture_type: continue

            namesMap.append((name, texture_type))

        return namesMap



    def geometryMapFromZip(self, zipobj):
        """
        Create list of tuples [(archived_file_name, billboard_type), ...]
        (i.e.
        [
            ("Billboard_4K_Albedo.jpg", "albedo"),
            ("Billboard_4K_Normal.jpg", "normal"),
            ...
        ]
        :param zipobj: zipfile.ZipFile() object
        :return: list
        """
        if not isinstance(zipobj, ZF.ZipFile):
            raise TypeError("Expect zipfile.ZipFile() object")

        namesMap = []

        for name in zipobj.namelist():

            if not self.isGeometry(name): continue
            if self.isHiresGeometry(name): continue

            var = self.variationFromString(name, caseSense=False)
            lod = self.LODFromString(name, caseSense=True)

            namesMap.append((name, lod, var))

        return namesMap




    def extractPreviewFromZip(self, zipobj: ZF.ZipFile, dstdir:str, newname:str):

        for name in zipobj.namelist():
            if self.isPreview(name):
                extension = os.path.splitext(name)[-1]
                zipobj.extract(name, dstdir)

                os.rename(
                    src=os.path.join(dstdir, name),
                    dst=os.path.join(dstdir, newname+extension)
                )
                break




    def extractSurfaceAsset(self, zippath:str, dstdir:str, classes:list, name:str):
        """
        Extract textures, preview from Quixel surface asset.
        Rename all textures by type. Rename preview to "preview".
        Extract some information from json info file in archive.

        :param zippath: path to Quixel surface zip archive
        :param dstdir: destination folder to extract
        :param classes: list of classes to which the asset belongs
        :param name: name of asset (it will be placed in the "info.json" file)
        """

        if not ZF.is_zipfile(zippath):
            raise ZF.BadZipFile(zippath + " is not a zip file")

        zobj = ZF.ZipFile(zippath, "r")
        info = self.getInfoFromZip(zobj, classes, name)
        textureMap = self.textureMapFromZip(zobj)
        folder = os.path.join(dstdir, str(info["id"]))

        if not os.path.exists(folder):
            os.makedirs(folder)

        for zname, textype in textureMap:
            extension = os.path.splitext(zname)[-1]
            zobj.extract(zname, folder)
            os.rename(
                src=os.path.join(folder, zname),
                dst=os.path.join(folder, textype+extension)
            )

        self.extractPreviewFromZip(zobj, folder, "preview")
        self.saveToJSON(
            obj=info,
            path=os.path.join(folder, "info.json")
        )



    def extractAtlasAsset(self, zippath: str, dstdir: str, classes: list, name: str):
        """
        For info check hlep of "extractSurfaceAsset" function

        :param zippath: path to Quixel surface zip archive
        :param dstdir: destination folder to extract
        :param classes: list of classes to which the asset belongs
        :param name: name of asset (it will be placed in the "info.json" file)
        """
        self.extractSurfaceAsset(zippath, dstdir, classes, name)



    def extract3DAsset(self, zippath:str, dstdir:str, classes:list, name:str):
        """
        Extract textures, preview from Quixel 3d asset.
        Rename all textures by type. Rename preview to "preview".
        Extract some information from json info file in archive.

        :param zippath: path to Quixel 3d zip archive
        :param dstdir: destination folder to extract
        :param classes: list of classes to which the asset belongs
        :param name: name of asset (it will be placed in the "info.json" file)
        """

        if not ZF.is_zipfile(zippath):
            raise ZF.BadZipFile(zippath + " is not a zip file")

        zobj = ZF.ZipFile(zippath, "r")
        info = self.getInfoFromZip(zobj, classes, name)
        textureMap = self.textureMapFromZip(zobj)
        folder = os.path.join(dstdir, str(info["id"]))

        if not os.path.exists(folder):
            os.makedirs(folder)

        for zname, textype in textureMap:
            extension = os.path.splitext(zname)[-1]
            zobj.extract(zname, folder)
            os.rename(
                src=os.path.join(folder, zname),
                dst=os.path.join(folder, textype+extension)
            )

        self.extractPreviewFromZip(zobj, folder, "preview")
        self.saveToJSON(
            obj=info,
            path=os.path.join(folder, "info.json")
        )



if __name__ == '__main__':

    import json

    storage_surface = "D:/quixel_download/Quixel Megascans/surface"
    storage_atlas = "D:/quixel_download/Quixel Megascans/atlas"
    storage_3d = "D:/quixel_download/Quixel Megascans/3d"
    storage_3dplant = "D:/quixel_download/Quixel Megascans/3dplant"

    q = QuixelParser()
    root = storage_surface
    dst = "C:/Users/edward/Desktop/Quixel"

    for i, zname in enumerate(os.listdir(root)):
        if i < 1:
            zpath = os.path.join(root, zname)
            q.extractSurfaceAsset(zpath, dst, ["nature"], "1")


