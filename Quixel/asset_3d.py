
import Quixel.quixel_base
import zipfile as ZF
import os


class Quixel3D(Quixel.quixel_base.QuixelBase):

    def __init__(self):
        super(Quixel3D, self).__init__()

        self.constraints = {
            "textureLODs": ["LOD0"]
        }



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



    def getValueFromJSONInfoTexelDensity(self, jsondata):
        """
        Extract texel density

        :param jsondata: data from Quixel .json file
        :return: dict
        """

        records = []

        for record in jsondata['meta']:
            if record["key"] == "texelDensity":
                value = ""
                for s in record["value"].replace(",", "."):
                    if s in "0123456789":
                        value += s
                value = int(value)

                records.append(
                    {
                        "key": "texel_density",
                        "name": "Texel density",
                        "type": "int",
                        "value": value
                    }
                )
                break

        return records



    def mapGeometryFromZip(self, zipobj):
        """
        Create list of dicts for each geometry in zip archive
        (i.e.
        [
            {
                "name": "Billboard_LOD0_ms.fbx",
                "lod": "LOD1"
                "ext": ".fbx"
            },
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

            namesMap.append(
                {
                    "name": name,
                    "lod": self.LODFromString(name, caseSense=True),
                    "ext": os.path.splitext(name)[-1]
                }
            )

        return namesMap



    def mapTexturesFromZip(self, zipobj):
        """
        Create list of dicts for each required texture in zip archive
        (i.e.
        [
            {
                "type": "albedo",
                "name": "olzmD_4K_Albedo.jpg",
                "ext": ".jpg"

            }
            ...
        ]
        :param zipobj: zipfile.ZipFile() object
        :return: list
        """
        if not isinstance(zipobj, ZF.ZipFile):
            raise TypeError("Expect zipfile.ZipFile() object")

        namesMap = []

        for name in zipobj.namelist():

            ext = os.path.splitext(name)[-1]

            texture_type = self.textureTypeFromString(name, 3)

            if self.LODFromString(name) not in ("", "LOD0"): continue

            if not texture_type: continue

            namesMap.append(
                {
                    "name": name,
                    "type": texture_type,
                    "ext": ext
                }
            )

        return namesMap



    def makeGeometryRecords(self, jsondata):
        """
        Extract meshes LOD and triangles count

        :param jsondata: data from Quixel .json file
        :return: list
        """
        meshes = jsondata["meshes"]
        records = []
        for record in meshes:
            if record["type"] != "lod": continue
            lod = self.LODFromString(record["uris"][0]["uri"])
            tris = record["tris"]
            records.append(
                {
                    "key": lod.lower(),
                    "name": lod,
                    "type": "int",
                    "value": tris
                }
            )
        return records



    def makeBoundRecords(self, jsondata):
        """
        Extract meshes LOD and triangles count

        :param jsondata: data from Quixel .json file
        :return: list
        """
        meshes = jsondata["meshes"]
        records = []
        for record in meshes:
            if record["type"] != "lod": continue
            lod = self.LODFromString(record["uris"][0]["uri"])
            tris = record["tris"]
            records.append(
                {
                    "key": lod.lower(),
                    "name": lod,
                    "type": "int",
                    "value": tris
                }
            )
        return records



    def makeTextureRecords(self, jsondata):
        """
        Extract meshes LOD and triangles count

        :param jsondata: data from Quixel .json file
        :return: list
        """
        meshes = jsondata["meshes"]
        records = []
        for record in meshes:
            if record["type"] != "lod": continue
            lod = self.LODFromString(record["uris"][0]["uri"])
            tris = record["tris"]
            records.append(
                {
                    "key": lod.lower(),
                    "name": lod,
                    "type": "int",
                    "value": tris
                }
            )
        return records



    def makeInfoFromZip(self, zipobj, uniqid, classes, name):
        """
        Collect some info from Quixel asset json info file

        :param zipobj: zipfile.ZipFile() object of Quixel asset zip file
        :return: dict
        """

        if not isinstance(zipobj, ZF.ZipFile):
            raise TypeError("Expected < zipfile.ZipFile > type object")

        jsondata = self.getJSONInfoData(zipobj)
        filename = os.path.basename(zipobj.filename)

        group_asset = {
            "group": "asset",
            "records": self.makeAssetRecords(uniqid, jsondata, filename, classes, name)
        }
        group_texture = {
            "group": "textures",
            "records": self.makeTextureRecords(jsondata)
        }
        group_geometry = {
            "group": "geometry",
            "records": self.makeGeometryRecords(jsondata)
        }
        group_bound = {
            "group": "bound",
            "records": self.makeBoundRecords(jsondata)
        }

        return [
            group_asset,
            group_bound,
            group_geometry,
            group_texture
        ]



    def extractAsset(self, zippath, dstdir, classes, name):
        """
        Extract geometry, textures and preview from Quixel 3d asset.
        Rename all textures and geometry by type (or LOD), rename preview to "preview".
        Extract some information from json info file in archive.

        :param zippath: path to Quixel 3d zip archive
        :param dstdir: destination folder to extract
        :param classes: list of classes to which the asset belongs
        :param name: name of asset (it will be placed in the "info.json" file)
        """

        if not ZF.is_zipfile(zippath):
            raise StandardError(zippath + " is not a zip file")

        zobj = ZF.ZipFile(zippath, "r")
        uniqid = self.uniqueID()
        info = self.makeInfoFromZip(zobj, uniqid, classes, name)

        folder_uniqid = os.path.join(dstdir, uniqid)
        folder_geo = os.path.join(folder_uniqid, "geometry")
        folder_txt = os.path.join(folder_uniqid, "textures")

        textureMap = self.mapTexturesFromZip(zobj)
        geometryMap = self.mapGeometryFromZip(zobj)

        if not os.path.exists(folder_uniqid): os.makedirs(folder_uniqid)
        if not os.path.exists(folder_geo): os.makedirs(folder_geo)
        if not os.path.exists(folder_txt): os.makedirs(folder_txt)

        for map in textureMap:
            zobj.extract(map["name"], folder_txt)
            os.rename(
                src=os.path.join(folder_txt, map["name"]),
                dst=os.path.join(folder_txt, map["type"]+map["ext"])
            )

        for map in geometryMap:
            zobj.extract(map["name"], folder_geo)
            os.rename(
                src=os.path.join(folder_geo, map["name"]),
                dst=os.path.join(folder_geo, map["lod"]+map["ext"])
            )

        self.extractPreviewFromZip(zobj, folder_uniqid, "preview")
        self.saveToJSON(
            obj=info,
            path=os.path.join(folder_uniqid, "info.json")
        )




if __name__ == '__main__':

    storage_surface = "D:/quixel_download/Quixel Megascans/surface"
    storage_atlas = "D:/quixel_download/Quixel Megascans/atlas"
    storage_3d = "D:/quixel_download/Quixel Megascans/3d/nature"
    storage_3dplant = "D:/quixel_download/Quixel Megascans/3dplant"

    parser = Quixel3D()
    root = storage_3d
    dst = "C:/Users/edward/Desktop/Quixel"

    for i, zname in enumerate(os.listdir(root)):
        if i < 1:
            zpath = os.path.join(root, zname)
            parser.extractAsset(zpath, dst, ["cls"], "n")