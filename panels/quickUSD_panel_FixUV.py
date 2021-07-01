
import bpy
from panels.quickUSD_panel import QuickUSDTemplatePanel 

class QUSD_PT_FixUV(QuickUSDTemplatePanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_FixUV_panel'
    
    bl_parent_id = "OBJECT_PT_Preprocess_panel"
    bl_label = "Fix UV"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        quickusd_tool = scene.quickusd_tool
        layout.label(text="Set Output UV Name/Attribute")

        layout.prop(quickusd_tool, "enum_uvNames", text="")
        layout.operator("wm.quickusd_updateuvnames")
        
        layout.separator()