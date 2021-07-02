from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade


usdStage = Usd.Stage.Open("C:/temp/usd/t4/WindowSill/WindowSillt.usda")
# usdStage = Usd.Stage.Open("C:/temp/usd/t4/WindowFrameCartoon/WindowFrameCartoon.usda")
# usdStage2 = "C:/temp/usd/t4/TopCurvedGlass.003/TopCurvedGlass.003.usda"

refSphere2 = usdStage.OverridePrim('/WindowFrameCartoon')
refSphere2.GetReferences().AddReference('../WindowFrameCartoon/WindowFrameCartoon.usda')
usdStage.GetRootLayer().Save()