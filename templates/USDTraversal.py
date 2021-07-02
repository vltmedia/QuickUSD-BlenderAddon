from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade


usdStage = Usd.Stage.Open("C:/temp/usd/t4/TopCurvedGlass.003/TopCurvedGlass.003.usda")

class GetUSDParent:
    def __init__(self):
        self.loaded = True
    def GetParentAtTop(self,CurrentObj):
        if CurrentObj.GetParent().GetPath().pathString != "/":
            self.GetParentAtTop(CurrentObj.GetParent())
        else:
            self.TopParent = CurrentObj.GetPath().pathString

# def FindMeshInScene():
pathss = [x for x in usdStage.Traverse()]
chosenpath = ""
for pathh in pathss:
    if "mesh_0" in pathh.GetPath().pathString:
        gg = GetUSDParent()
        gg.GetParentAtTop(pathh)
        p = gg.TopParent
        print(p)
        print(pathh.GetPath().pathString)
        # return pathh
            

# FindMeshInScene()