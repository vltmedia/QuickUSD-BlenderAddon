import bpy


class CheckOmniverseLogin(bpy.types.Operator):
    bl_idname = "wm.quickusd_checkomniverselogin"
    bl_label = "Check Omniverse Login"

    def execute(self, context):
        # Report "Hello World" to the Info Area
        print("CheckOmniverseLogin")
        return {'FINISHED'}

