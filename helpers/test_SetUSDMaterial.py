# python "D:/Projects/Apps/QuickUSDToolset/Code/Blender/addon/helpers/test_SetUSDMaterial.py" --Source "BuildingB_Window_Cartoon.usda" --NewMaterialPath "/Looks/WindowMaterial" --ShaderName PBRShader --PrimitivePath "/WindowFrameCartoon/WindowFrameCartoon2" --Diffuse "tex/Building_B_S.jpg" --Roughness "tex/Building_B_Roughness.jpg" --Normal "tex/Building_B_Normal.jpg" --Metallic ""
#python "D:/Projects/Apps/QuickUSDToolset/Code/Blender/addon/helpers/test_SetUSDMaterial.py" --Source "D:/QuickCode/usd/Training/BuildingB_Window_Cartoon.usda" --NewMaterialPath "/Looks/WindowMaterial" --ShaderName PBRShader --PrimitivePath "/WindowFrameCartoon/WindowFrameCartoon2" --Diffuse "tex/Building_B_S.jpg" --Roughness "tex/Building_B_Roughness.jpg" --Normal "tex/Building_B_Normal.jpg" --Metallic ""
from pxr import Usd

import USDHelper
# import helpers.USDHelper

import json
import argparse

import os
import sys

# Create the parser
my_parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
my_parser.add_argument('--Source', metavar='--source',  type=str, default="", help='The USD to be edited.')
my_parser.add_argument('--NewMaterialPath', metavar='--newmaterialpath',  type=str, default="/Looks/UntitledMat", help='the new Material path, keep it /Looks/...')
my_parser.add_argument('--ShaderName', metavar='--shadername',  type=str, default="PBRShader", help='ShaderName')
my_parser.add_argument('--PrimitivePath', metavar='--primitivepath',  type=str, help='The path to the Primitive to set the new material to.')
# my_parser.add_argument('--Diffuse', metavar='--diffuse',  type=str, default="", help='Relative path to the Diffuse texture to apply.')
# my_parser.add_argument('--Roughness', metavar='--roughness',  type=str, default="", help='Relative path to the Roughness texture to apply.')
# my_parser.add_argument('--Normal', metavar='--normal',  type=str, default="", help='Relative path to the Normal texture to apply.')
# my_parser.add_argument('--Metallic', metavar='--metallic',  type=str, default="", help='Relative path to the Metallic texture to apply.')

my_parser.add_argument('--MaterialConfig', metavar='--materialconfig',  type=str, default="", help='Material.json to use')

# Execute the parse_args() method
args = my_parser.parse_args()
sourceUSD = args.Source
NewMaterialPath = args.NewMaterialPath
ShaderName = args.ShaderName
PrimitivePath = args.PrimitivePath
MaterialConfig = {}
if args.MaterialConfig != "":
    with open(args.MaterialConfig) as json_file:
        MaterialConfig = json.load(json_file)   
    Diffuse = args.Diffuse
    Roughness = args.Roughness
    Normal = args.Normal
    Metallic = args.Metallic
else:
    Diffuse = args.Diffuse
    Roughness = args.Roughness
    Normal = args.Normal
    Metallic = args.Metallic


os.chdir(os.path.dirname(os.path.abspath(sourceUSD)))

print("---------------------------------------------------------------------")
print("---------------------------------------------------------------------")
print("---------------------------------------------------------------------")
print("---------------------------------------------------------------------")
print("args",args)



print("---------------------------------------------------------------------")
print("---------------------------------------------------------------------")
print("---------------------------------------------------------------------")

def hardTest():
    
    usdHelper = USDHelper.USDHelper()
    usdHelper.LoadUSDFile("BuildingB_Window_Cartoon.usda")
    usdHelper.SelectPrimitive("/WindowFrameCartoon/WindowFrameCartoon")
    
    usdHelper.CreateNewMaterial("/Looks/WindowMaterial","/Looks/WindowMaterial/PBRShader")
    usdHelper.SetDiffuseTexture("tex\Building_B_S.jpg")
    usdHelper.SetRoughnessTexture("tex\Building_B_Roughness.jpg")
    usdHelper.SetNormalTexture("tex\Building_B_Normal.jpg")
    usdHelper.SetMetallicTexture("")
    usdHelper.ApplyCurrentMaterialAndPrimitive()
    # usdHelper.QuickCreateNewMaterial("/Looks/WindowMaterial","/Looks/WindowMaterial/PBRShader", os.path.abspath("tex\Building_B_S.jpg"),os.path.abspath("tex\Building_B_Roughness.jpg"),"",os.path.abspath("tex\Building_B_Normal.jpg"))
    usdHelper.Save()
    
   
def ArgTest():
    
    usdHelper = USDHelper.USDHelper()
    usdHelper.LoadUSDFile(sourceUSD)
    usdHelper.SelectPrimitive(PrimitivePath)
    
    usdHelper.CreateNewMaterial(NewMaterialPath,NewMaterialPath+'/'+ShaderName)
    usdHelper.SetDiffuseTexture(Diffuse)
    usdHelper.SetRoughnessTexture(Roughness)
    usdHelper.SetNormalTexture(Normal)
    usdHelper.SetMetallicTexture(Metallic)
    usdHelper.ApplyCurrentMaterialAndPrimitive()
    # usdHelper.QuickCreateNewMaterial("/Looks/WindowMaterial","/Looks/WindowMaterial/PBRShader", os.path.abspath("tex\Building_B_S.jpg"),os.path.abspath("tex\Building_B_Roughness.jpg"),"",os.path.abspath("tex\Building_B_Normal.jpg"))
    usdHelper.Save()
    
    
    
if __name__ == '__main__':
    print("1")
    ArgTest()
    print("Ys")
    
    