import glob
import os
import sys
from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade
import json
import argparse
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from ApplyUSDTextures import QUSD_ApplyMaterial
import USDHelper


class USDCombine:

    def __init__(self, BaseFolder):
        self.usdHelper = USDHelper.USDHelper()
        self.usdHelper.Check()
        self.BaseFolder = BaseFolder
        self.USDConfigPath = os.path.join(self.BaseFolder, "usdconfig.json")
        self.References = []
        self.Materials = []
        self.USDConfig = {"Objects": []}
        
    def GetUSDAFiles(self):
        self.USDFiles = glob.glob(self.BaseFolder+'/**/*.usda')
        self.USDConfigJSONs = [os.path.dirname( configs) + '/usdconfig.json'  for configs in self.USDFiles]
    
    def CreateMaterial(self, MaterialPath, ShaderPath):
        self.Materials.append(self.usdHelper.CreateNewMaterial(MaterialPath,ShaderPath))
        
    def CreateBaseUSDFile(self, filename):
        combinee = os.path.join(self.BaseFolder, filename)
        self.stage = Usd.Stage.CreateNew(combinee)
        self.usdHelper.LoadUSDStage(self.stage)
    # def CleanMaterialSlots(self):
    #     currentmaterials = []
    #     currentmaterialsNames = []
    #     for obj in self.USDConfig['Objects']:
    #         for mat in obj['MaterialSlots']:
    #             currentmaterialsNames = []
                
    #             if mat['Name'] not in currentmaterialsNames:
    #                 currentmaterialsNames.append(mat['Name'])
    #                 currentmaterials.append(mat)
    #     self.USDConfig['MaterialSlots'] = currentmaterials
    
    def GetObjectsContainingMaterial(self, MaterialName):
        matchingobjects = []
        for obj in self.USDConfig['Objects']:
            for mat in obj["MaterialSlots"]:
                if MaterialName in mat['Name']:
                    matchingobjects.append( obj)
        return matchingobjects
    
    def ApplyMaterialSlots(self):
        for mat in self.USDConfig['MaterialSlots']:
            materialslott = mat
            self.materialslott = mat
            print("Material Slot :", materialslott)
            # self.usdHelper.CreateNewMaterial(materialslott["MaterialPath"],materialslott["ShaderPath"])
            self.CreateMaterial(self.materialslott["MaterialPath"],self.materialslott["ShaderPath"])
            # Apply Textures
            self.ApplyPBRTextures()
            for meshh in self.materialslott['Meshes']:
            
                currentmesh = self.usdHelper.FindMatchingMeshInScene(meshh)
                print(currentmesh)
                
                self.usdHelper.HardApplyMaterialToPrimitive(self.materialslott["MaterialPath"],currentmesh)

        
        
    def ApplyPBRTextures(self):
        if os.path.exists(os.path.abspath(self.materialslott["Diffuse"]) ) or self.materialslott["Diffuse"] != "tex":
            self.usdHelper.SetDiffuseTexture(self.materialslott["Diffuse"],True)
        if os.path.exists(os.path.abspath(self.materialslott["Roughness"])) or self.materialslott["Diffuse"] != "tex":
            
            self.usdHelper.SetRoughnessTexture(self.materialslott["Roughness"],True)
        if os.path.exists(os.path.abspath(self.materialslott["Normal"])) or self.materialslott["Diffuse"] != "tex":
            
            self.usdHelper.SetNormalTexture(self.materialslott["Normal"],True)
        if os.path.exists(os.path.abspath(self.materialslott["Metal"])) or self.materialslott["Diffuse"] != "tex":
            
            self.usdHelper.SetMetallicTexture(self.materialslott["Metal"],True)
                

    def CleanMaterialSlots(self):
        currentmaterials = []
        currentmaterialsNames = []
        
        # Get Material Names
        for obj in self.USDConfig['Objects']:
            for mat in obj['MaterialSlots']:
                
                if mat['Name'] not in currentmaterialsNames:
                    currentmaterialsNames.append(mat['Name'])
                    currentmaterials.append(mat)
                    
        # Set Material Slots inside of each object to the cleane dup material slot
        for i in range(0,len(self.USDConfig['Objects']) - 1 ):
            self.USDConfig['Objects'][i]['MaterialSlots'] = currentmaterials  
            # print("UPDATED CLEAN : ", self.USDConfig['Objects'][i]['MaterialSlots'])
                    
        self.USDConfig['MaterialSlots'] = currentmaterials
        for i in range(0,len(self.USDConfig['MaterialSlots']) ):
            objss = [n['Path'].replace(".","_") for n in self.GetObjectsContainingMaterial(self.USDConfig['MaterialSlots'][i]['Name'])]
            self.USDConfig['MaterialSlots'][i]['Meshes'] = objss
        self.ApplyMaterialSlots()
        print("yo")
            


    def ReadJSONConfigs(self):
        if not os.path.exists(os.path.join(self.BaseFolder, "usdconfig.json")):
            for i in range(0, len(self.USDConfigJSONs)):
                with open(self.USDConfigJSONs[i]) as f:
                    self.USDConfig['Objects'].append(json.load(f))
            self.CleanMaterialSlots()
        else:
            with open(os.path.join(self.BaseFolder, "usdconfig.json")) as f:
                self.USDConfig= json.load(f)
        
    def SaveUSDStage(self):
        self.stage.GetRootLayer().Save()
        
    
    def SaveJSONConfig(self):
        with open(self.USDConfigPath, 'w') as json_file:
            json.dump(self.USDConfig, json_file, indent = 4)
    
    def AddReferenceToStage(self,ReferenceUSDFile, PrimitivePath):
        NewReference = self.stage.OverridePrim(PrimitivePath)
        NewReference.GetReferences().AddReference(ReferenceUSDFile)
        self.References.append(NewReference)
        
    def GetMatchingObject(self, NameToMatch):
        for obj in self.USDConfig['Objects']:
            if NameToMatch in obj['USDFile']:
                return obj
                    
            
        
    def PopulateStage(self):
        for i in range(0, len(self.USDFiles)):
            matchedobj = self.GetMatchingObject(os.path.basename(self.USDFiles[i]))
            relname = './'+os.path.relpath(self.USDFiles[i], self.BaseFolder).replace("\\", "/")
            splitt = matchedobj['Path'].split("/")[len(matchedobj['Path'].split("/")) - 1]
            cleanedpath = matchedobj['Path'].replace(splitt, "")[:-1]
            cleanedpath = '/'+matchedobj['Path'].split("/")[1]
            print(matchedobj["MaterialSlots"])
            self.AddReferenceToStage(relname,cleanedpath)
            # print("primpath", matchedobj['Path'])
            # print("relname", cleanedpath)
            # print("cleanedpath", cleanedpath)

def Test():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="Directory to Process into one USD file.",
                        type=str, default="",required=False)
    parser.add_argument("--out", help="The USDa filename to create and write the references to.",
                        type=str, default="",required=False)
    args = parser.parse_args()
    
    
    usdCombine = USDCombine(args.directory)
    usdCombine.GetUSDAFiles()
    usdCombine.ReadJSONConfigs()
    usdCombine.CreateBaseUSDFile(args.out)
    usdCombine.PopulateStage()
    usdCombine.CleanMaterialSlots()
    usdCombine.SaveJSONConfig()
    usdCombine.SaveUSDStage()
    
if __name__ == '__main__':
    Test()