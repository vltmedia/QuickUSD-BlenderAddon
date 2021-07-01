import bpy

from helpers.blender_MaterialHelper import MaterialHelper 

class PackageTextures(bpy.types.Operator):
    bl_idname = "wm.quickusd_packagetextures"
    bl_label = "Package Textures"
    
    @classmethod 
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.type == 'MESH'
    
    def execute(self, context):
        scene = context.scene
        quickusd_tool = scene.quickusd_tool
        
        materialHelper = MaterialHelper()
        outputdir = '/'.join(quickusd_tool.outputdir.split('\\'))
        # materialHelper.ExportUSDA(outputdir, True)
        materialHelper.PackageTexturesToDirectory(outputdir)
        # Report "Hello World" to the Info Area
        print("ExportUSD")
        return {'FINISHED'}

