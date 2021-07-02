# python ApplyUSDTextures.py --config "C:\temp\usd\tex2\Window_ArchWithGlass\usdconfig.json"

import pxr

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import USDHelper

import argparse



class QUSD_ApplyMaterial:

    def __init__(self):
            
        self.usdHelper = USDHelper.self.usdHelper()
        self.usdHelper.Check()

        parser = argparse.ArgumentParser()
        parser.add_argument("--config", help="Usually a usdconfig.json file with the Material Slots info",
                            type=str, default="")

        # Add the arguments

        args = parser.parse_args()

        print(args.config)

        currentdir = os.path.dirname(args.config) 
        print("currentdir", currentdir)
        os.chdir(currentdir)
        self.MaterialConfig = args.config
        self.LoadMaterialConfig()
        self.ReadMaterialData()
        self.CleanupPaths()
        self.Materials = []

    def LoadMaterialConfig(self):
        with open(self.MaterialConfig) as f:
            self.MaterialData = json.load(f)

    def CleanupPaths(self):
        
        matslots = []


        
        for i in range(0, len(self.MaterialData["MaterialSlots"])):
            js = {
    "Name" :"",
    "Diffuse": "",
    "Roughness":"",
    "Normal":"" ,
    "Metal":"" ,
    "Opacity":"",
    "ORM":"" ,
    "AO":"" ,
    "Emissive":"",
    "Discplacement":""
    
    
    
}
            materialslott = self.MaterialData["MaterialSlots"][i]
            if materialslott["Diffuse"] != "" or os.path.exists(os.path.abspath(materialslott["Diffuse"])):
                
                self.MaterialData["MaterialSlots"][i]["Diffuse"] = os.path.relpath(os.path.abspath(materialslott["Diffuse"] ), os.getcwd())
                js["Diffuse"] = os.path.relpath(os.path.abspath(materialslott["Diffuse"] ), os.getcwd())
                
        
            if self.MaterialData["MaterialSlots"][i]["Roughness"] != "" or os.path.exists(os.path.abspath(materialslott["Roughness"])):
                self.MaterialData["MaterialSlots"][i]["Roughness"] = os.path.relpath(os.path.abspath(materialslott["Roughness"]), os.getcwd())
                js["Roughness"] = os.path.relpath(os.path.abspath(materialslott["Roughness"]), os.getcwd())
        
            if self.MaterialData["MaterialSlots"][i]["Normal"] != "" or os.path.exists(os.path.abspath(materialslott["Normal"])):
                self.MaterialData["MaterialSlots"][i]["Normal"] = os.path.relpath(os.path.abspath(materialslott["Normal"]), os.getcwd())
                js["Normal"] = os.path.relpath(os.path.abspath(materialslott["Normal"]), os.getcwd())
        
            if self.MaterialData["MaterialSlots"][i]["Metal"] != "" or os.path.exists(os.path.abspath(materialslott["Metal"])):
                self.MaterialData["MaterialSlots"][i]["Metal"] = os.path.relpath(os.path.abspath(materialslott["Metal"]), os.getcwd())
                js["Metal"] = os.path.relpath(os.path.abspath(materialslott["Metal"]), os.getcwd())
                
            if self.MaterialData["MaterialSlots"][i]["Opacity"] != ""or os.path.exists(os.path.abspath(materialslott["Opacity"])):
                self.MaterialData["MaterialSlots"][i]["Opacity"] = os.path.relpath(os.path.abspath(materialslott["Opacity"]), os.getcwd())
                js["Opacity"] = os.path.relpath(os.path.abspath(materialslott["Opacity"]), os.getcwd())
                
            if self.MaterialData["MaterialSlots"][i]["ORM"] != ""or os.path.exists(os.path.abspath(materialslott["ORM"])):
                self.MaterialData["MaterialSlots"][i]["ORM"] = os.path.relpath(os.path.abspath(materialslott["ORM"]), os.getcwd())
                js["ORM"] = os.path.relpath(os.path.abspath(materialslott["ORM"]), os.getcwd())
                
            if self.MaterialData["MaterialSlots"][i]["AO"] != ""or os.path.exists(os.path.abspath(materialslott["AO"])):
                self.MaterialData["MaterialSlots"][i]["AO"] = os.path.relpath(os.path.abspath(materialslott["AO"]), os.getcwd())
                js["AO"] = os.path.relpath(os.path.abspath(materialslott["AO"]), os.getcwd())
        
            if self.MaterialData["MaterialSlots"][i]["Emissive"] != ""or os.path.exists(os.path.abspath(materialslott["Emissive"])):
                self.MaterialData["MaterialSlots"][i]["Emissive"] = os.path.relpath(os.path.abspath(materialslott["Emissive"]), os.getcwd())
                js["Emissive"] = os.path.relpath(os.path.abspath(materialslott["Emissive"]), os.getcwd())
        
            if self.MaterialData["MaterialSlots"][i]["Discplacement"] != ""or os.path.exists(os.path.abspath(materialslott["Discplacement"])):
                self.MaterialData["MaterialSlots"][i]["Discplacement"] = os.path.relpath(os.path.abspath(materialslott["Discplacement"]), os.getcwd())
                js["Discplacement"] = os.path.relpath(os.path.abspath(materialslott["Discplacement"]), os.getcwd())
            js["MaterialPath"] = self.MaterialData["MaterialSlots"][i]["MaterialPath"]
            js["ShaderPath"] = self.MaterialData["MaterialSlots"][i]["ShaderPath"]
    
            matslots.append(js)
        tempdata = {

"MaterialSlots":matslots ,   
"Object":self.MaterialData["Object"] ,   
"USDFile":self.MaterialData["USDFile"] ,   
"Path":self.MaterialData["Path"] ,   
"Parent":self.MaterialData["Parent"] ,   
"Children":self.MaterialData["Children"] ,   
"ChildrenPaths":self.MaterialData["ChildrenPaths"] ,   
                
                }       
        self.MaterialData = tempdata
        print("OUTPUT : ", self.MaterialData)
    
    
    def ReadMaterialData(self):
        diffusee = os.path.relpath(os.path.abspath(self.MaterialData["MaterialSlots"][0]["Diffuse"]), os.getcwd())
        print(diffusee)
        
    def LoadStage(self, stage):
        self.usdHelper.LoadUSDStage(stage)
    def LoadMaterialUSD(self):
        self.usdHelper.LoadUSDFile(os.path.abspath(self.MaterialData["USDFile"]))
    def ProcessUSD(self):
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("Loaded | " , self.MaterialData)
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("SelectPrimitive | " , self.MaterialData["Path"])
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        
        self.usdHelper.AddObjectConfig(self.MaterialData)
        self.usdHelper.SelectPrimitive(self.MaterialData["Path"])
        self.ApplyMaterialSlots(True)
        
        

            
    def ApplyMaterialSlots(self, ApplyToObject):
        for mat in self.MaterialData["MaterialSlots"]:
            materialslott = mat
            self.materialslott = mat
            print("Material Slot :", materialslott)
            # self.usdHelper.CreateNewMaterial(materialslott["MaterialPath"],materialslott["ShaderPath"])
            self.CreateMaterial(self.materialslott["MaterialPath"],self.materialslott["ShaderPath"])
            # Apply Textures
            self.ApplyPBRTextures()
            if ApplyToObject:
                self.self.usdHelper.ApplyCurrentMaterialAndPrimitive()
        
        
    def ApplyPBRTextures(self):
        if os.path.exists(os.path.abspath(self.materialslott["Diffuse"]) ) or self.materialslott["Diffuse"] != "tex":
            self.usdHelper.SetDiffuseTexture(self.materialslott["Diffuse"])
        if os.path.exists(os.path.abspath(self.materialslott["Roughness"])) or self.materialslott["Diffuse"] != "tex":
            
            self.usdHelper.SetRoughnessTexture(self.materialslott["Roughness"])
        if os.path.exists(os.path.abspath(self.materialslott["Normal"])) or self.materialslott["Diffuse"] != "tex":
            
            self.usdHelper.SetNormalTexture(self.materialslott["Normal"])
        if os.path.exists(os.path.abspath(self.materialslott["Metal"])) or self.materialslott["Diffuse"] != "tex":
            
            self.usdHelper.SetMetallicTexture(self.materialslott["Metal"])
    
    def CreateMaterial(self, MaterialPath, ShaderPath):
        self.Materials.append(self.usdHelper.CreateNewMaterial(MaterialPath,ShaderPath))
        
        #self.usdHelper.Save()
    def SaveUSD(self):
        self.usdHelper.Save()        
        

def ProcessMaterial():
    
   
    ApplyMaterial = QUSD_ApplyMaterial()
    # ApplyMaterial.LoadStage()
    ApplyMaterial.LoadMaterialUSD()
    ApplyMaterial.ProcessUSD()
    ApplyMaterial.SaveUSD()
    
    
if __name__ == '__main__':
    ProcessMaterial()