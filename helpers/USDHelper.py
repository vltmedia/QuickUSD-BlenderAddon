# Use this python class to add Textures to USD obejcts.

from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade
import os
class USDHelper:

    def __init__(self):

        self.CreatedMaterials = []
        self.CreatedPbrShaders = []
    
    def Check(self):
        print("USDHelper Loaded!")
    
    def LoadUSDFile(self, filepath):
        self.usdStage = Usd.Stage.Open(filepath)
    
    def SelectPrimitive(self, PrimitivePath):
        self.usdPrimitive =  self.usdStage.GetPrimAtPath(PrimitivePath)
        self.usdPrimitivePath = self.usdPrimitive.GetPath()

    def GetPrimitivePath(self):
        return self.usdPrimitivePath
    
    def Save(self):
        self.usdStage.Save()
    
    def SetRoughness(self, RoughnessTexturePath):

        # Setup Diffuse Texture
        TextureSampler = UsdShade.Shader.Define(self.usdStage,RoughnessTexturePath)
        TextureSampler.CreateIdAttr('UsdUVTexture')
        # Set Image File path
        TextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(RoughnessTexturePath)
        TextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(self.stReader.ConnectableAPI(), 'result')
        TextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
        # Connect Texture to Material
        self.Currentpbrshader.CreateInput("roughness", Sdf.ValueTypeNames.Color3f).ConnectToSource(TextureSampler.ConnectableAPI(), 'rgb')
        stInput = self.Currentmaterial.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
        stInput.Set('st')
        self.stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)
    
    
    def SetTexture(self, TextureUSDPath, TextureFilePath, InputName):

        # Setup Diffuse Texture
        TextureSampler = UsdShade.Shader.Define(self.usdStage,TextureUSDPath)
        TextureSampler.CreateIdAttr('UsdUVTexture')
        # Set Image File path
        TextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(TextureFilePath)
        TextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(self.stReader.ConnectableAPI(), 'result')
        TextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
        # Connect Texture to Material
        self.Currentpbrshader.CreateInput(InputName, Sdf.ValueTypeNames.Color3f).ConnectToSource(TextureSampler.ConnectableAPI(), 'rgb')
        stInput = self.Currentmaterial.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
        stInput.Set('st')
        self.stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)
    
    def SetDiffuseTexture(self, DiffuseTexture):
        if os.path.exists(DiffuseTexture):
            
            self.SetTexture(self.CurrentmaterialPath+'/diffuseColor',DiffuseTexture,"diffuseColor")
    def SetRoughnessTexture(self, RoughnessTexture):
        if os.path.exists(RoughnessTexture):
            self.SetTexture(self.CurrentmaterialPath+'/roughness',RoughnessTexture,"roughness")
        else:
            self.Currentpbrshader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
            
    def SetNormalTexture(self, NormalTexture):
        if os.path.exists(NormalTexture):
            self.SetTexture(self.CurrentmaterialPath+'/normal',NormalTexture,"normal")
        # else:
        #     self.Currentpbrshader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Float).Set(0.4)
            
                
    def SetMetallicTexture(self, MetallicTexture):
        if os.path.exists(MetallicTexture):
            self.SetTexture(self.CurrentmaterialPath+'/metallic',MetallicTexture,"metallic")
        # else:
            # self.Currentpbrshader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.4)
            
    def ApplyMaterialToPrimitive(self,MaterialPath, PrimitivePath):
        material = UsdShade.Material.Get(self.usdStage,MaterialPath)
        Primitive_ = self.usdStage.GetPrimAtPath(PrimitivePath)
        
        print("Prim Path :", PrimitivePath)
        print("material Path :", MaterialPath)
        UsdShade.MaterialBindingAPI(Primitive_).Bind(material)
    
    def ApplyCurrentMaterialAndPrimitive(self):
        self.ApplyMaterialToPrimitive(self.CurrentmaterialPath, self.usdPrimitivePath)
    
    def QuickCreateNewMaterial(self, NewMaterialPath, ShaderName, DiffuseTexture, RoughnessTexture, MetallicTexture, NormalTexture):
        diff = DiffuseTexture
        roughnesss = RoughnessTexture
        metallicc = MetallicTexture
        # Texturing
        self.stReader = UsdShade.Shader.Define(self.usdStage, NewMaterialPath+'/stReader')
        self.stReader.CreateIdAttr('UsdPrimvarReader_float2')

        # Material Setup
        material = UsdShade.Material.Define(self.usdStage, NewMaterialPath)
        self.Currentmaterial = material
        self.CurrentmaterialPath = NewMaterialPath
        
        # Shader Setup
        pbrShader = UsdShade.Shader.Define(self.usdStage, ShaderName)
        pbrShader.CreateIdAttr("UsdPreviewSurface")
        self.Currentpbrshader = pbrShader
        
        # Connect Shader to Material
        material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")
        
        
        print(RoughnessTexture)
        if diff != "":
            self.SetTexture(NewMaterialPath+'/diffuseColor',DiffuseTexture,"diffuseColor")
        else:
            pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Float).Set(0.4)
            
            
        if roughnesss != "":
            self.SetTexture(NewMaterialPath+'/roughness',RoughnessTexture,"roughness")
        else:
            pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
            
            
        if metallicc != "":
            self.SetTexture(NewMaterialPath+'/metallic',MetallicTexture, "metallic")
        else:
            pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.4)
                    
        if NormalTexture != "":
            self.SetTexture(NewMaterialPath+'/normal',NormalTexture, "normal")
        else:
            print("Normal Empty")
            # pbrShader.CreateInput("normal", Sdf.ValueTypeNames.Float).Set(0.4)
            
        # self.CreatedMaterials.append(material)
        # self.CreatedPbrShaders.append(pbrShader)
        UsdShade.MaterialBindingAPI(self.usdPrimitive).Bind(material)
        


    
    def CreateNewMaterial(self, NewMaterialPath, ShaderName):

        # Texturing
        self.stReader = UsdShade.Shader.Define(self.usdStage, NewMaterialPath+'/stReader')
        self.stReader.CreateIdAttr('UsdPrimvarReader_float2')

        # Material Setup
        material = UsdShade.Material.Define(self.usdStage, NewMaterialPath)
        self.Currentmaterial = material
        self.CurrentmaterialPath = NewMaterialPath
        
        # Shader Setup
        pbrShader = UsdShade.Shader.Define(self.usdStage, ShaderName)
        pbrShader.CreateIdAttr("UsdPreviewSurface")
        self.Currentpbrshader = pbrShader
        
        # Connect Shader to Material
        material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")



