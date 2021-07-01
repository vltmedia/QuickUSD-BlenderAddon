
import bpy
from panels.quickUSD_panel import QuickUSDTemplatePanel 

class QUSD_PT_nvidiaOmniverseFilepath(QuickUSDTemplatePanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_nvidiaOmniverseFilepath_panel'
    bl_parent_id = "OBJECT_PT_nvidiaOmniverse_panel"
    bl_label = "Send Asset"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        quickusd_tool = scene.quickusd_tool
        layout.label(text="Base Folder")

        layout.prop(quickusd_tool, "enum_nucleusFolders", text="") 
        layout.prop(quickusd_tool, "nucleusTargetFolder")
        
        layout.operator("wm.quickusd_exporttoomniverse")
        layout.operator("wm.quickusd_checkomniverselogin")
        
        layout.separator()