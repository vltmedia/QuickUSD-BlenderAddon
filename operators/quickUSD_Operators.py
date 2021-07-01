import bpy
from operators.quickUSD_Op_PackageTextures import PackageTextures
from operators.quickUSD_Op_ExportUSD import ExportUSD
from operators.quickUSD_Op_OpenLastExportedUSD import OpenLastExportedUSD
from operators.quickUSD_Op_UpdateUVNames import UpdateUVNames
from operators.quickUSD_Op_ExportToOmniverse import ExportToOmniverse
from operators.quickUSD_Op_CheckOmniverseLogin import CheckOmniverseLogin


class QuickUSD_Operators:

    def __init__(self):
        
        self.classes = [
        ExportUSD,
        UpdateUVNames,
        ExportToOmniverse,
        CheckOmniverseLogin,
        OpenLastExportedUSD,
        PackageTextures
        ]


    def register(self):
        
        for cls in self.classes:
                try:
                    bpy.utils.register_class(cls)
                except ValueError as e:
                    bpy.utils.unregister_class(cls)
                    bpy.utils.register_class(cls)

