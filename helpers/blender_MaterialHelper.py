

import bpy
import os 
import shutil
import json
import subprocess

DiffuseArray = ["Diffuse","_dif","BaseColor","basecolor","Base_Color" ,"Color","diffuse" ]
RoughnessArray = ["Rough","Roughness" ]
NormalArray = ["Normal","_n","norm" ]
MetallicArray = ["Metallic","Metalness","Metal" ]
EmissiveArray = ["Emissive","Emission","Emit" ]
AmbientOcclusionArray = ["AmbientOcclusion","_AO","Ambient","Occlusion","Oclusion","Ambient_Occlusion" ]
DisplacementArray = ["Displacement","_height","displacement","displace","PixelOffset" ]
OpacityArray = ["opacity","transparancy","alpha" ]
ORMArray = ["orm","ORM","_ORM","OcclusionRoughnessMetallic" ]

#bpy.ops.wm.usd_export(filepath="C:/temp/usd/testArch.usda", selected_objects_only=True, visible_objects_only=False)
class MaterialHelper:

    def __init__(self):
        self.Loaded = True
        
        self.MaterialName = ""
        self.DiffuseTexture = ""
        self.RoughnessTexture = ""
        self.NormalTexture = ""
        self.MetalTexture = ""
        self.OpacityTexture = ""
        self.ORMTexture = ""
        self.AOTexture = ""
        self.EmissiveTexture = ""
        self.DiscplacementTexture = ""
        
        self.MaterialSlots = []
        self.ExportUSD_ = False
        
        
    def CreateMaterialJson(self):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        materialpathh = quickusd_tool.materialpath.replace("$OBJ", self.currentMaterialName)
        # js = {
        #     "Name" : self.currentMaterialName,
        #     "Diffuse": self.DiffuseTexture,
        #     "Roughness": self.RoughnessTexture,
        #     "Normal": self.NormalTexture,
        #     "Metal": self.MetalTexture,
        #     "Opacity": self.OpacityTexture,
        #     "ORM": self.ORMTexture,
        #     "AO": self.AOTexture,
        #     "Emissive": self.EmissiveTexture,
        #     "Discplacement": self.DiscplacementTexture
            
            
            
        # }
        js = {
            "Name" : self.currentMaterialName,
            "MaterialPath" : materialpathh ,
            "ShaderPath" : quickusd_tool.shaderpath.replace("$MATERIALPATH", materialpathh) ,
            "Diffuse": os.path.relpath(os.path.abspath(self.TextureOutputDirectory + "/" +self.DiffuseTexture), self.ObjectOutputDirectory),
            "Roughness":os.path.relpath(os.path.abspath(self.TextureOutputDirectory + "/" +self.RoughnessTexture), self.ObjectOutputDirectory),
            "Normal":os.path.relpath(os.path.abspath(self.TextureOutputDirectory + "/" +self.NormalTexture), self.ObjectOutputDirectory) ,
            "Metal":os.path.relpath(os.path.abspath(self.TextureOutputDirectory + "/" +self.MetalTexture), self.ObjectOutputDirectory) ,
            "Opacity":os.path.relpath(os.path.abspath(self.TextureOutputDirectory + "/" +self.OpacityTexture), self.ObjectOutputDirectory),
            "ORM":os.path.relpath(os.path.abspath(self.TextureOutputDirectory + "/" +self.ORMTexture), self.ObjectOutputDirectory) ,
            "AO":os.path.relpath(os.path.abspath(self.TextureOutputDirectory + "/" +self.AOTexture), self.ObjectOutputDirectory) ,
            "Emissive":os.path.relpath(os.path.abspath(self.TextureOutputDirectory + "/" +self.EmissiveTexture), self.ObjectOutputDirectory) ,
            "Discplacement":os.path.relpath(os.path.abspath(self.TextureOutputDirectory + "/" +self.DiscplacementTexture), self.ObjectOutputDirectory)
            
            
            
        }

        self.MaterialSlots.append(js)
        self.MaterialJson = {
            "Object" : self.CurrentObject.name,
            "USDFile" : self.CurrentObject.name+".usda",
            "Path" : "/"+self.CurrentObject.name + "/" + self.CurrentObject.data.name,
            "Parent" : self.CurrentObject.parent if self.CurrentObject.parent !=None else "" ,
            "Children" : [childs.name for childs in self.CurrentObject.children],
            
            
            "MaterialSlots":self.MaterialSlots                
                            
                            }
        

    def GetMaterialsFromObjects(self, ObjectsList):
        try:
            selectedobejcts = ObjectsList
            # selectedobejcts = bpy.context.selected_editable_objects
            texturepaths = []

            for f in selectedobejcts:
                
                try:
                    pathss = self.GetMaterialPaths(f)
                    temparray = texturepaths + pathss
                    texturepaths = temparray
                except:
                    print("Failed",f)
            self.texturepaths = texturepaths
            print(texturepaths)
        except:
            print("Not Loaded Yet")

    def GetMaterialsFromObject(self, SourceObject):
            # selectedobejcts = bpy.context.selected_editable_objects
            texturepaths = []

                
            try:
                pathss = self.GetMaterialPaths(SourceObject)
                temparray = texturepaths + pathss
                texturepaths = temparray
            except:
                print("Failed",SourceObject)
            self.texturepaths = texturepaths
            print(texturepaths)
          
    def GetFullTexturePath(self,imageName):
        tex = bpy.data.images[imageName]
        full_path = bpy.path.abspath(tex.filepath, library=tex.library)
    # '/project/assets/shaders/../textures/walls/WALL_1773.png'

        norm_path = os.path.normpath(full_path)
    # '/project/assets/textures/walls/WALL_1773
        return norm_path
    
    def GetMaterialPaths(self, ObjectMesh):
        texturejsons = []
        textures = []
        texturepaths = []

        for mat_slot in ObjectMesh.material_slots:
            if mat_slot.material:
                if mat_slot.material.node_tree:
                    self.currentMaterialName = mat_slot.material.name
                    self.texturepathss =  [x for x in mat_slot.material.node_tree.nodes if x.type=='TEX_IMAGE']
                    
                    for textur in self.texturepathss:
                        
                        tex = self.GetFullTexturePath(textur.image.name)
                        print(tex)
                        texturepaths.append(tex)
                        self.GetTextureType(tex)
                    self.CreateMaterialJson()
                    textures.extend([x for x in mat_slot.material.node_tree.nodes if x.type=='TEX_IMAGE'])
                    # textures.extend([x for x in mat_slot.material.node_tree.nodes if x.type=='TEX_IMAGE'])
        print("textures", textures)
        print("texturepaths", texturepaths)
        return texturepaths
    
    def ExportUSDA(self, OutputDirectoryPath, PackageTextures):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        self.ExportUSD_ = True
        self.PackageTexturesToDirectory(OutputDirectoryPath )

        # bpy.ops.wm.usd_export(filepath=OutputDirectoryPath+ "/"++".usda", selected_objects_only=True, visible_objects_only=False)
        
    def ExportPackage(self,objectt, OutputDirectoryPath):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        textureoutput =OutputDirectoryPath +  '/'.join(quickusd_tool.textureoutputdir.split('\\'))
        
        # Make Output Directory based on Object Name
        if not os.path.exists(OutputDirectoryPath):
            os.mkdir(OutputDirectoryPath)
        # Make Texture Output Directory based on Object Name
        if not os.path.exists(textureoutput):
            os.mkdir(textureoutput)

        # Output MaterialJson File
        with open(OutputDirectoryPath + '/material.json', 'w') as outfile:
            json.dump(self.MaterialJson, outfile)
            
        # Copy files to output directory
        for filee in self.texturepaths:
            shutil.copy( filee, textureoutput)
        
                
        if self.ExportUSD_ == True:
            # Output USD File
            bpy.ops.wm.usd_export(filepath= OutputDirectoryPath+ "/"+objectt.name+".usda", selected_objects_only=True, visible_objects_only=False)
            self.RunApplyTextures(OutputDirectoryPath)
            
        
    def RunApplyTextures(self, OutputDirectoryPath):
        # Run ApplyUSDTextures.py
        applyusdpython = os.path.dirname(os.path.realpath(__file__)) + "/ApplyUSDTextures.py"
        args = ["cmd.exe", "/c","python", applyusdpython, "--config",OutputDirectoryPath + '/material.json' ]
        subprocess.run(args) 
        
    def PackageTexturesToDirectory(self,OutputDirectoryPath):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        selectedobejcts = bpy.context.selected_editable_objects
        textureoutput =OutputDirectoryPath +  '/'.join(quickusd_tool.textureoutputdir.split('\\'))
        self.OutputDirectoryPath = OutputDirectoryPath
        # self.GetMaterialsFromObjects(selectedobejcts)
        for objectt in selectedobejcts:
            self.OldDataName = objectt.data.name
            objectt.data.name = "mesh_0"
            self.OldUVName = objectt.data.uv_layers[0].name
            objectt.data.uv_layers[0].name = "st"
            self.CurrentObject = objectt
            self.ObjectOutputDirectory = OutputDirectoryPath + '/' + objectt.name
            self.TextureOutputDirectory = self.ObjectOutputDirectory + '/' + '/'.join(quickusd_tool.textureoutputdir.split('\\'))
            self.GetMaterialsFromObject(objectt)
            self.ExportPackage(objectt,self.ObjectOutputDirectory )
            print("usda name : ", objectt.name)
            print("usda path : ", OutputDirectoryPath+ "/"+objectt.name+".usda")
            objectt.data.uv_layers[0].name = self.OldUVName
        # self.ExportPackage(selectedobejcts[0], OutputDirectoryPath)
        # Make directory if it doesn't exist.
        
            
            
    def GetTextureType(self, filename):
        
        try:
            print("GetTextureType A ")
            print("GetTextureType filename ", filename)
            SourceCheck = os.path.basename( filename.lower())
            print("GetTextureType SourceCheck ", SourceCheck)

            for CompareString in NormalArray:
                if CompareString.lower() in SourceCheck:
                    self.NormalTexture = os.path.basename( filename)
                    return "NORMAL";
            
            for CompareString in ORMArray:
                
                if CompareString.lower() in SourceCheck:
                    self.ORMTexture = os.path.basename( filename)
                    return "ORM";
            
            for CompareString in AmbientOcclusionArray:
                if CompareString.lower() in SourceCheck:
                    self.AOTexture = os.path.basename( filename)
                    return "AO";

            for CompareString in DiffuseArray:
                if CompareString.lower() in SourceCheck:
                    self.DiffuseTexture = os.path.basename( filename)
                    return "DIFFUSE";

            for CompareString in RoughnessArray:
                if CompareString.lower() in SourceCheck:
                    self.RoughnessTexture = os.path.basename( filename)
                    return "ROUGHNESS";

            for CompareString in EmissiveArray:
                if CompareString.lower() in SourceCheck:
                    self.EmissiveTexture = os.path.basename( filename)
                    return "EMISSIVE";

            for CompareString in DisplacementArray:
                if CompareString.lower() in SourceCheck:
                    self.DiscplacementTexture = os.path.basename( filename)
                    return "DISPLACEMENT";

            for CompareString in OpacityArray:
                if CompareString.lower() in SourceCheck:
                    self.OpacityTexture = os.path.basename( filename)
                    return "OPACITY";

            for CompareString in MetallicArray:
                if CompareString.lower() in SourceCheck:
                    self.MetalTexture = os.path.basename( filename)
                    return "METALLIC";
        except:
            print("Failed ", filename)