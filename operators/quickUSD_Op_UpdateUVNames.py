import bpy


class UpdateUVNames(bpy.types.Operator):
    bl_idname = "wm.quickusd_updateuvnames"
    bl_label = "Update UV Names"

    def execute(self, context):
        # Report "Hello World" to the Info Area
        print("UpdateUVNames")
        return {'FINISHED'}

