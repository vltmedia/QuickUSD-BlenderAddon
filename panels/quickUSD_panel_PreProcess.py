
import bpy
from panels.quickUSD_panel import QuickUSDTemplatePanel 

class QUSD_PT_Preprocess(QuickUSDTemplatePanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_Preprocess_panel'
    bl_parent_id = "OBJECT_PT_quickusd_panel"
    bl_label = "Pre Processing"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.operator("wm.quickusd_cleanupgeo")
        layout.separator()
        