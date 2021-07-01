from panels.quickUSD_panel_OmniverseFilepath import QUSD_PT_nvidiaOmniverseFilepath
from panels.quickUSD_panel_Omniverse import QUSD_PT_nvidiaOmniverse
from panels.quickUSD_panel_PreProcess import QUSD_PT_Preprocess
from panels.quickUSD_panel_Export import QUSD_PT_Export
from panels.quickUSD_panel_FixUV import QUSD_PT_FixUV
from quickUSD import CleanUpGeo
import bpy
from bpy.props import IntProperty, PointerProperty, BoolProperty, CollectionProperty,FloatProperty

from bpy.types import Panel, PropertyGroup, WindowManager
from quickUSD import CleanUpGeo, OBJECT_PT_QuickUSDPanel
from quickUSD_props import QuickUSDProperties

from operators.quickUSD_Operators import QuickUSD_Operators

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "QuickUSD",
    "author" : "Justin Jaro",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "3D View > Tools",
    "warning" : "",
    "category" : "Generic"
}


classes = (
    CleanUpGeo,
    OBJECT_PT_QuickUSDPanel,
    
    # Populate Child Panels in Order from Top to Bottom


    # QUSD_PT_nvidiaOmniverse,
    # QUSD_PT_nvidiaOmniverseFilepath,
    QUSD_PT_Preprocess,
    QUSD_PT_FixUV,
    QUSD_PT_Export
)
operators = QuickUSD_Operators()

def register():

    # WindowManager.swapObject_vars = PointerProperty(type=swapObjectVars)
    try:
        bpy.utils.register_class(QuickUSDProperties)
    except:
        print("QuickUSDProperties exists")
    bpy.types.Scene.quickusd_tool = PointerProperty(type=QuickUSDProperties)
    
    operators.register()
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError as e:
            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)
    
    

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.quickusd_tool

