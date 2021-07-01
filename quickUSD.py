import bpy
from bpy.props import IntProperty, PointerProperty, BoolProperty, CollectionProperty,FloatProperty

from bpy.types import Panel, PropertyGroup, WindowManager
from quickUSD_props import QuickUSDProperties


# This is the tab area
class swapObjectVars(PropertyGroup):
    NamePattern: bpy.props.StringProperty(name="Source Name Pattern", default="Cube.*")
    TemplateObject: bpy.props.StringProperty(name="Template Object Name", default="Template")


class CleanUpGeo(bpy.types.Operator):
    bl_idname = "wm.quickusd_cleanupgeo"
    bl_label = "Clean Up Geo For USD"

    def execute(self, context):
        # Report "Hello World" to the Info Area
        print("CleanGEO")
        return {'FINISHED'}


class OBJECT_OT_swapobjectsingle(bpy.types.Operator):
    bl_idname = 'object.swapobjectsingle'
    bl_label = 'Swap Object Single'
    bl_options = {'REGISTER', 'UNDO'}
    NamePattern: bpy.props.StringProperty(name="Source Name Pattern", default="Cube.*")
    TemplateObject: bpy.props.StringProperty(name="Template Object Name", default="Template")


    def execute(self, context):
        bpy.ops.object.select_pattern(pattern= self.NamePattern)
        selects = context.selected_objects
        currentcount = 0
        transformss = []
        for obj in selects:
            transformss.append([obj.location, obj.rotation_quaternion, obj.scale])
            
            ob = bpy.data.objects.get(self.TemplateObject)
            # ob = bpy.data.objects.get("Template")
            ob_dup = ob.copy()
            print(ob_dup.name)
            bpy.data.collections['Collection'].objects.link(ob_dup)
            ob_dup.name = 'NewObjectName_' + str(currentcount)
            # template_object = bpy.data.objects.get('Template')
            # template_object = context.selected_objects[0]
            # if template_object:
            # Create the new object by linking to the template's mesh data
            new_object = ob_dup
            obj.hide_viewport = True
            obj.hide_render = True
            # new_object = bpy.data.objects.new('NewObjectName_' + str(currentcount), template_object.data)
            # Create a new animation for the newly created object
            nextcount = currentcount + 1
            currentcount = nextcount
            print(new_object.location)
            
            new_object.location = obj.location
            print(obj.location)
        
            # Link the new object to the appropriate collection

        return {'FINISHED'}

class OBJECT_MT_swapmenu(bpy.types.Menu):
    bl_idname = 'object.swapmenu'
    bl_label = 'Swap Objects'

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_swapobjectsingle.bl_idname)
classes = [
	OBJECT_OT_swapobjectsingle,
	OBJECT_MT_swapmenu
]


class swapObject_PT_panel(Panel):
    bl_idname = 'swapObject_PT_panel'
    bl_label = 'Quick Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QuickTools'

    def draw(self, context):
        operator = self.layout.operator('object.swapobjectsingle', icon='BLENDER', text='Swap Objects By Name')
        operator.NamePattern = context.window_manager.swapObject_vars.NamePattern
        operator.TemplateObject = context.window_manager.swapObject_vars.TemplateObject
        self.layout.prop(context.window_manager.swapObject_vars, 'NamePattern')
        self.layout.prop(context.window_manager.swapObject_vars, 'TemplateObject')

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_QuickUSDPanel(Panel):
    bl_label = "Quick USD"
    bl_idname = "OBJECT_PT_quickusd_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Quick USD"
    bl_context = "objectmode"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        quickusd_tool = scene.quickusd_tool
        layout.prop(quickusd_tool, "enum_exportSelection", text="")

        # layout.prop(quickusd_tool, "outputdir")
        # layout.prop(quickusd_tool, "enum_objectFlatten", text="") 
        # layout.prop(quickusd_tool, "enum_exportSelection", text="")
        # layout.prop(quickusd_tool, "bool_openPostExport")
        # layout.operator("wm.quickusd_cleanupgeo")
        # layout.separator()