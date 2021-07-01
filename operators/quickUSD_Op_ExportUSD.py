import bpy

from helpers.blender_MaterialHelper import MaterialHelper 

class ExportUSD(bpy.types.Operator):
    bl_idname = "wm.quickusd_exportusd"
    bl_label = "Export USD file"
    
    @classmethod 
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.type == 'MESH'
    
    def execute(self, context):
        materialHelper = MaterialHelper()
        # materialHelper.GetMaterialsFromSelected()
        # Report "Hello World" to the Info Area
        print("ExportUSD")
        return {'FINISHED'}

