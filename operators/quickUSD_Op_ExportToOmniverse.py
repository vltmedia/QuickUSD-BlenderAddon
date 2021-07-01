import bpy


class ExportToOmniverse(bpy.types.Operator):
    bl_idname = "wm.quickusd_exporttoomniverse"
    bl_label = "Export To Omniverse"

    def execute(self, context):
        # Report "Hello World" to the Info Area
        print("ExportToOmniverse")
        return {'FINISHED'}

