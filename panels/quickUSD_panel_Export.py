
import bpy
from panels.quickUSD_panel import QuickUSDTemplatePanel 

class QUSD_PT_Export(QuickUSDTemplatePanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_Export_panel'
    bl_parent_id = "OBJECT_PT_quickusd_panel"
    bl_label = "Export"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        quickusd_tool = scene.quickusd_tool
        layout.label(text="Export USD")

        layout.prop(quickusd_tool, "outputdir")
        layout.prop(quickusd_tool, "enum_objectFlatten", text="") 
        layout.prop(quickusd_tool, "bool_openPostExport")
        layout.operator("wm.quickusd_packagetextures")
        layout.operator("wm.quickusd_exportusd")
        layout.operator("wm.quickusd_openlastexportedusd")
        
        layout.separator()