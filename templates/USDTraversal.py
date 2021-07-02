from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade


usdStage = Usd.Stage.Open("C:/temp/usd/tex2/TopCurvedGlass.003/TopCurvedGlass.003.usda")

def FindMeshInScene(self):
    pathss = [x.GetPath().pathString for x in usdStage.Traverse()]
    chosenpath = ""
    for pathh in pathss:
        if "mesh_0" in pathh:
            return pathh
            