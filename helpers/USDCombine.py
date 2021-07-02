import glob
import os
from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade
import json

from ApplyUSDTextures import QUSD_ApplyMaterial


class USDCombine:

    def __init__(self,BaseFolder):
        self.BaseFolder = BaseFolder
        self.USDConfigPath = os.path.join(BaseFolder, "usdconfig.json")
        self.References = []
        self.USDConfig = {"Objects": []}
        
    def GetUSDAFiles(self):
        self.USDFiles = glob.glob(self.BaseFolder+'/**/*.usda')
        self.USDConfigJSONs = [os.path.dirname( configs) + '/usdconfig.json'  for configs in self.USDFiles]

    def CreateBaseUSDFile(self, filename):
        combinee = os.path.join(self.BaseFolder, filename)
        self.stage = Usd.Stage.CreateNew(combinee)

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
            print("UPDATED CLEAN : ", self.USDConfig['Objects'][i]['MaterialSlots'])
                    
        self.USDConfig['MaterialSlots'] = currentmaterials
            


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
            self.AddReferenceToStage(relname,cleanedpath)
            print("primpath", matchedobj['Path'])
            print("relname", relname)
            print("cleanedpath", cleanedpath)

def Test():
    usdCombine = USDCombine("C:/temp/usd/t4")
    usdCombine.GetUSDAFiles()
    usdCombine.ReadJSONConfigs()
    usdCombine.CreateBaseUSDFile("BuildingA.usda")
    usdCombine.PopulateStage()
    usdCombine.CleanMaterialSlots()
    
    print("Cleaned Materials ", usdCombine.USDConfig['MaterialSlots'])
    usdCombine.SaveJSONConfig()
    usdCombine.SaveUSDStage()
    
if __name__ == '__main__':
    Test()