

import bpy
import os 
import shutil
import json
import subprocess
from helpers.CenterObject import BlenderHelper_CenterObject
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
        self.ObjectPaths = { "ObjectPaths" : []}
        self.MaterialSlots = []
        self.ExportedUSDA = []
        self.ExportUSD_ = False
        self.USDConfig = {"Objects": []}
        self.BH_CenterObject = BlenderHelper_CenterObject()
        
    def CenterObject(self):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        self.BH_CenterObject.CenterObject(self.CurrentObject,quickusd_tool.bool_SnapToFloor)
        
    def ResetObject(self):
        self.BH_CenterObject.ResetObject()
        
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
            "MaterialPath" : materialpathh.replace(".", "_") ,
            "ShaderPath" : quickusd_tool.shaderpath.replace("$MATERIALPATH", materialpathh).replace(".", "_") ,
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
            "Path" : self.GetMatchingDict(self.CurrentObject.name)['ObjectMeshPath'],
            # "Path" : "/"+self.CurrentObject.name + "/" + self.CurrentObject.data.name,
            "Parent" : self.CurrentObject.parent.name if self.CurrentObject.parent !=None else "" ,
            "Children" : [childs.name for childs in self.CurrentObject.children],
            "ChildrenPaths" : self.GetChildrenPaths(self.CurrentObject),
            
            
            "MaterialSlots":self.MaterialSlots            
            # "ObjectPaths":self.ObjectPaths['ObjectPaths']                
                            
                            }
        

    def GetMaterialsFromObjects(self, ObjectsList):
        try:
            selectedobjects = ObjectsList
            # selectedobjects = bpy.context.selected_editable_objects
            texturepaths = []

            for f in selectedobjects:
                
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
            # selectedobjects = bpy.context.selected_editable_objects
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
                    self.MaterialSlots = []
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
        # print("textures", textures)
        # print("texturepaths", texturepaths)
        return texturepaths
    
    def ExportUSDA(self, OutputDirectoryPath, PackageTextures):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        self.ExportUSD_ = True
        self.PackageTexturesToDirectory(OutputDirectoryPath )

        # bpy.ops.wm.usd_export(filepath=OutputDirectoryPath+ "/"++".usda", selected_objects_only=True, visible_objects_only=False)
    def GetObjectsContainingMaterial(self, MaterialName):
        matchingobjects = []
        for obj in self.USDConfig['Objects']:
            for mat in obj["MaterialSlots"]:
                if MaterialName in mat['Name']:
                    matchingobjects.append( obj)
        return matchingobjects
    def SaveGroupUSDConfig(self):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        self.CleanMaterialSlots()
        materialpathh = quickusd_tool.materialpath.replace("$OBJ", self.currentMaterialName) 
        self.USDConfig["MaterialPath"] = materialpathh
        self.USDConfig["ShaderPath"] =quickusd_tool.shaderpath.replace("$MATERIALPATH", materialpathh) 
        with open(self.OutputDirectoryPath + '/usdconfig.json', 'w') as outfile:
            json.dump( self.USDConfig, outfile, indent = 4)
    
    
    def CleanMaterialSlots(self):
        currentmaterials = []
        currentmaterialsNames = []
        
        # Get Material Names
        for obj in self.USDConfig['Objects']:
            # print("OBJJJ " , obj)
            for mat in obj['MaterialSlots']:
                
                if mat['Name'] not in currentmaterialsNames:
                    currentmaterialsNames.append(mat['Name'])
                    currentmaterials.append(mat)

                    
        # Set Material Slots inside of each object to the cleane dup material slot
        for i in range(0,len(self.USDConfig['Objects']) - 1 ):
            self.USDConfig['Objects'][i]['MaterialSlots'] = currentmaterials  
            # print("UPDATED CLEAN : ", self.USDConfig['Objects'][i]['MaterialSlots'])

        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # for i in range(0,len(currentmaterials)  ):
        #     currentchoice = self.GetObjectsContainingMaterial(currentmaterials[i]['Name'])
        #     print("GET OBJECTS : ", currentchoice)
        #     self.USDConfig['MaterialSlots'][i]['Meshes'] = currentchoice
                    
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        
        # self.USDConfig['MaterialSlots'] = currentmaterials   
         
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
        # Make Texture Output Directory based on Object Name
        if not os.path.exists(self.BaseTexOutputDirectoryPath):
            os.mkdir(self.BaseTexOutputDirectoryPath)
        print("OUT MAT | ", self.MaterialJson)
        # Output MaterialJson File
        with open(OutputDirectoryPath + '/usdconfig.json', 'w') as outfile:
            json.dump(self.MaterialJson, outfile)
        self.USDConfig['Objects'].append(self.MaterialJson)
        
        # Copy files to output directory
        for filee in self.texturepaths:
            shutil.copy( filee, textureoutput)
        # Copy files to output directory
        for filee in self.texturepaths:
            shutil.copy( filee, self.BaseTexOutputDirectoryPath)
        
        self.SetSelectedObjectByName(objectt.name)
                
        if self.ExportUSD_ == True:
            # Center Object
            if quickusd_tool.bool_CenterObject:
                self.CenterObject()

            
            # Output USD File
            bpy.ops.wm.usd_export(filepath= OutputDirectoryPath+ "/"+objectt.name+".usda", selected_objects_only=True, visible_objects_only=False)
            self.RunApplyTextures(OutputDirectoryPath)
            self.ExportedUSDA.append(OutputDirectoryPath+ "/"+objectt.name+".usda")
            
            if quickusd_tool.bool_CenterObject:
            # Reset Position of object and origin
                self.ResetObject()
            
            
    def AddChildren(self,ob):

        for child in ob.children:
            currentlayer = self.GetMatchingDict(ob.name)['Path'] + '/' +child.name
        # currentlayer =self.currentlayer+ "/" + ob.name
            self.currentlayer = currentlayer
            self.selectedobjects.append(child)
            if len(child.children) != 0:
                    
                # child.name = ob.name + "_" + child.type
                self.AddObjectToObjectPaths(child.name,currentlayer, currentlayer + "/mesh_0")
                self.AddChildren(child)    
            else:
                self.AddObjectToObjectPaths(child.name, currentlayer ,currentlayer+ "/mesh_0")
                
    def CenterOrigin(self,SnapToFloor):
        #Get active object    
        act_obj = bpy.context.active_object
            
        #Get cursor
        cursor = bpy.context.scene.cursor

        #Get original cursor location
        self.original_cursor_location = (cursor.location[0], cursor.location[1], cursor.location[2])   

        #Make sure origin is set to geometry for cursor z move 
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')  

        #Set cursor location to object location
        cursor.location = act_obj.location
        if SnapToFloor:
            #Get cursor z move  
            half_act_obj_z_dim = act_obj.dimensions[2] / 2
            cursor_z_move = cursor.location[2] - half_act_obj_z_dim   
            
            #Move cursor to bottom of object
            cursor.location[2] = cursor_z_move

        #Set origin to cursor
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        
        #Assuming you're wanting object center to grid
        bpy.ops.object.location_clear(clear_delta=False)
        #bpy.ops.object.origin_clear()


                    
    def SetSelectedObject(self):
        bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
        bpy.context.view_layer.objects.active = self.CurrentObject   # Make the cube the active object 
        self.CurrentObject.select_set(True) 
            
    def SetSelectedObjectByName(self, ObjectName):
        objectt = bpy.data.objects[ObjectName]
        bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
        bpy.context.view_layer.objects.active = objectt   # Make the cube the active object 
        objectt.select_set(True) 
        
    def RunApplyTextures(self, OutputDirectoryPath):
        # Run ApplyUSDTextures.py
        # applyusdpython = os.path.dirname(os.path.realpath(__file__)) + "/ApplyUSDTextures.py"
        applyusdpython = os.path.dirname(os.path.realpath(__file__)) + "/ApplyUSDTextures.py"
        args = ["cmd.exe", "/c","python", applyusdpython, "--config",OutputDirectoryPath + '/usdconfig.json' ]
        subprocess.run(args) 
            
    def RunUSDCombineReferences(self, OutputDirectoryPath):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        self.ExportedUSDA.append(OutputDirectoryPath + "/" + quickusd_tool.outputmergedusdaname)
        # Run ApplyUSDTextures.py
        # applyusdpython = os.path.dirname(os.path.realpath(__file__)) + "/ApplyUSDTextures.py"
        applyusdpython = os.path.dirname(os.path.realpath(__file__)) + "/USDCombine.py"
        args = ["cmd.exe", "/c","python", applyusdpython, "--directory",OutputDirectoryPath, "--out", quickusd_tool.outputmergedusdaname ]
        subprocess.run(args) 
                
    def OpenUSDInViewer(self, USDfilepath):
        args = ["cmd.exe", "/c","usdview.cmd", USDfilepath ]
        subprocess.Popen(args) 
    
    def AddObjectToObjectPaths(self, ObjectName, ObjectPath, ObjectMeshPath):
        jsout = {
                "Name":ObjectName,
                "Path":ObjectPath,
                "RelativePath":'/'+ObjectName+'/mesh_0',
                "ObjectMeshPath":ObjectMeshPath
            }
        self.ObjectPaths['ObjectPaths'].append(jsout)
        
    def AddBaseSelectedObjects(self):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        for selobj in self.selectedobjects:
            jsout = {
                "Name":selobj.name,
                "Path":"/"+selobj.name + "/" + selobj.data.name
            }
            self.AddObjectToObjectPaths(selobj.name,"/"+selobj.name, "/"+selobj.name + "/mesh_0")
            self.currentlayer = "/"+selobj.name
            if quickusd_tool.bool_ExportHierarchy:
                self.AddChildren(selobj)
            # self.AddObjectToObjectPaths(selobj.name, "/"+selobj.name + "/" + selobj.data.name)
            # self.ObjectPaths['ObjectPaths'].append(jsout)
            # self.ObjectPaths[selobj.name] = "/"+selobj.name + "/" + selobj.data.name
            
    
    def GetMatchingPath(self, ObjectName):
        selectedpath = ""
        for objj in self.ObjectPaths['ObjectPaths']:
            if objj['Name'] == ObjectName:
                selectedpath = objj['Path']
                return selectedpath
                
    def GetMatchingDict(self, ObjectName):
        selectedpath = ""
        for objj in self.ObjectPaths['ObjectPaths']:
            if objj['Name'] == ObjectName:
                return objj
    
    def GetChildrenPaths(self, ParentObject):
        selectedpath = ""
        childrenobjs = []
        for objj in self.ObjectPaths['ObjectPaths']:
            if ParentObject.name in objj['ObjectMeshPath']:
                if objj['Name'] != ParentObject.name:
                    childrenobjs.append(objj)
        return childrenobjs
                        
            
    def PackageTexturesToDirectory(self,OutputDirectoryPath):
        scene = bpy.context.scene
        quickusd_tool = scene.quickusd_tool
        selectedobjects = bpy.context.selected_editable_objects
        self.selectedobjects = bpy.context.selected_editable_objects
        self.AddBaseSelectedObjects()
        # for selobj in selectedobjects:
        #     jsout = {
        #         "Name":selobj.name,
        #         "Path":"/"+selobj.name + "/" + selobj.data.name
        #     }
        #     self.AddObjectToObjectPaths(selobj.name, "/"+selobj.name + "/" + selobj.data.name)
        #     # self.ObjectPaths['ObjectPaths'].append(jsout)
        #     # self.ObjectPaths[selobj.name] = "/"+selobj.name + "/" + selobj.data.name
        print ("---------------------------------------------------------------")
        print ("---------------------------------------------------------------")
        print ("---------------------------------------------------------------")
        print ("self.ObjectPaths : ",self.ObjectPaths)
        print ("---------------------------------------------------------------")
        print ("---------------------------------------------------------------")
        print ("---------------------------------------------------------------")
        
        textureoutput =OutputDirectoryPath +  '/'.join(quickusd_tool.textureoutputdir.split('\\'))
        self.OutputDirectoryPath = OutputDirectoryPath
        self.BaseOutputDirectoryPath = OutputDirectoryPath
        self.BaseTexOutputDirectoryPath = OutputDirectoryPath + "/tex"
        # self.GetMaterialsFromObjects(selectedobjects)
        for objectt in self.selectedobjects:
        # for objectt in selectedobjects:
            self.OldDataName = objectt.data.name
            
            print("MATCHING PATH :: ", self.GetMatchingPath(objectt.name))
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
        # self.ExportPackage(selectedobjects[0], OutputDirectoryPath)
        # Make directory if it doesn't exist.
        self.SaveGroupUSDConfig()
        
        if quickusd_tool.bool_mergereferences:
            self.RunUSDCombineReferences(self.BaseOutputDirectoryPath)
            
        if quickusd_tool.bool_openPostExport:
            for filee in self.ExportedUSDA:
                self.OpenUSDInViewer(filee)
        
            
            
    def GetTextureType(self, filename):
        
        try:
            # print("GetTextureType A ")
            # print("GetTextureType filename ", filename)
            SourceCheck = os.path.basename( filename.lower())
            # print("GetTextureType SourceCheck ", SourceCheck)

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