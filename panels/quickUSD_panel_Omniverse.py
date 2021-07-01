
import bpy
from panels.quickUSD_panel import QuickUSDTemplatePanel 

class QUSD_PT_nvidiaOmniverse(QuickUSDTemplatePanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_nvidiaOmniverse_panel'
    bl_parent_id = "OBJECT_PT_quickusd_panel"
    bl_label = "NVIDIA Omniverse"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        quickusd_tool = scene.quickusd_tool
        layout.label(text="Settings for Omniverse")

        layout.prop(quickusd_tool, "nucleusIP")
        layout.prop(quickusd_tool, "nucleusPort")
        layout.prop(quickusd_tool, "enum_objectFlatten", text="") 
