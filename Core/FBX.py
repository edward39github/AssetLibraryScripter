
import fbx

fbx.FbxNodeAttribute

class FBXWrapper(object):

    def __init__(self):
        super(FBXWrapper, self).__init__()

        self._manager = fbx.FbxManager.Create()
        self._scene = fbx.FbxScene.Create(self._manager, "")
        self._importer = fbx.FbxImporter.Create(self._manager, "")
        self._exporter = fbx.FbxExporter.Create(self._manager, "")


    def importFile(self, file_path):
        self._importer.Initialize(file_path, -1)
        self._importer.Import(self._scene)


    def exportFile(self, file_path):
        self._exporter.Initialize(file_path, -1)
        self._exporter.Export(self._scene)


    def sceneUnits(self):
        units = self._scene.GetGlobalSettings().GetSystemUnit()

        if units == fbx.FbxSystemUnit.mm: return "mm"
        elif units == fbx.FbxSystemUnit.cm: return "cm"
        elif units == fbx.FbxSystemUnit.dm: return "dm"
        elif units == fbx.FbxSystemUnit.m: return "m"
        elif units == fbx.FbxSystemUnit.km: return "km"
        elif units == fbx.FbxSystemUnit.Inch: return "inch"
        elif units == fbx.FbxSystemUnit.Foot: return "foot"
        elif units == fbx.FbxSystemUnit.Mile: return "mile"
        elif units == fbx.FbxSystemUnit.Yard: return "yard"
        else: return ""


    def sceneBounds(self, precision=3):

        min = fbx.FbxVector4()
        max = fbx.FbxVector4()
        center = fbx.FbxVector4()

        self._scene.ComputeBoundingBoxMinMaxCenter(min, max, center)

        x = round(max[0] - min[0], precision)
        y = round(max[1] - min[1], precision)
        z = round(max[2] - min[2], precision)

        return x, y, z


    def scenePointsCount(self):
        pass


    def LODs(self):

        root = self._scene.GetRootNode()

        for i in range(root.GetChildCount()):
            node = root.GetChild(i)
            lod = root.GetChild(i).GetNodeAttribute()

            for j in range(node.GetChildCount()):
                print node.GetChild(j).GetName()





if __name__ == '__main__':

    fbxpath = "C:/users/edward/Desktop/out.fbx"

    w = FBXWrapper()

    w.importFile(fbxpath)

    w.LODs()
