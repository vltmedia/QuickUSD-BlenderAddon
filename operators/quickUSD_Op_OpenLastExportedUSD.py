import bpy


class OpenLastExportedUSD(bpy.types.Operator):
    bl_idname = "wm.quickusd_openlastexportedusd"
    bl_label = "Open Last Exported USD"

    def execute(self, context):
        # Report "Hello World" to the Info Area
        print("OpenLastExportedUSD")
        return {'FINISHED'}

