
import bpy

from bpy.props import (StringProperty,
                    BoolProperty,
                    IntProperty,
                    FloatProperty,
                    FloatVectorProperty,
                    EnumProperty,
                    PointerProperty,
                    )
from bpy.types import (Panel,
                    Menu,
                    Operator,
                    PropertyGroup,
                    )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class QuickUSDProperties(PropertyGroup):

    bool_openPostExport: BoolProperty(
        name="Post Open In USDView",
        description="Open the saved out USD(s) in USDView after exporting",
        default = False
        )
    bool_mergereferences: BoolProperty(
        name="Merge .usda To File",
        description="Merge all the selected objects'.usda into a single .usda importing them as references.",
        default = True
        )
    bool_CenterObject: BoolProperty(
        name="Center Object",
        description="Do you want to Center the Object to 0,0,0? If Snap to Floor is off, Origin will be placed at the center of the object.",
        default = True
        )

    bool_SnapToFloor: BoolProperty(
        name="Snap To Floor",
        description="Do you want to Snap the object to the floor when centered? Only works if Center Object is checked.",
        default = True
        )
    bool_ExportHierarchy: BoolProperty(
        name="Export Parents & Children",
        description="Export Full Hierarchy, including Parents & Children",
        default = True
        )

    # my_int: IntProperty(
    #     name = "Int Value",
    #     description="A integer property",
    #     default = 23,
    #     min = 10,
    #     max = 100
    #     )

    # my_float: FloatProperty(
    #     name = "Float Value",
    #     description = "A float property",
    #     default = 23.7,
    #     min = 0.01,
    #     max = 30.0
    #     )

    # my_float_vector: FloatVectorProperty(
    #     name = "Float Vector Value",
    #     description="Something",
    #     default=(0.0, 0.0, 0.0), 
    #     min= 0.0, # float
    #     max = 0.1
    # ) 

    outputmergedusdaname: StringProperty(
        name="Merged .usda Name",
        description="The filename of the USDA that will hold all the USD created. Use this for Layout work.",
        default="merged.usda",
        maxlen=2048,
        )
    outputdir: StringProperty(
        name="Output Directory",
        description="Output Directory of the USD file(s)",
        default="",
        maxlen=2048,
        )
    materialpath: StringProperty(
        name="Material USD Path",
        description="The Material USD Path",
        default="/Looks/$OBJ",
        maxlen=2048,
        )
    shaderpath: StringProperty(
        name="Shader USD Path",
        description="The Material Shader USD Path",
        default="$MATERIALPATH/PBRShader",
        maxlen=2048,
        )

    textureoutputdir: StringProperty(
        name="Texture Output Directory",
        description="Texture Output Directory of the USD file(s)",
        default="/tex",
        maxlen=2048,
        )


    nucleusIP: StringProperty(
        name="Nucleus IP/URL",
        description="IP or URL to connect to an NVIDIA Nucleus server.",
        default="localhost",
        maxlen=2048,
        )


    nucleusPort: StringProperty(
        name="Nucleus Port",
        description="Port to connect to an NVIDIA Nucleus server",
        default="8080",
        maxlen=2048,
        )


    nucleusTargetFolder: StringProperty(
        name="Target Folder",
        description="Target Folder to send an asset to an NVIDIA Nucleus server",
        default="/ExampleProject/Objects/Props",
        maxlen=2048,
        )


    enum_objectFlatten: EnumProperty(
        name="Object Flatten:",
        description="Should the export be a single USD, or each object to it's own USD?",
        items=[ ('OP1', "Single USD", ""),
                ('OP2', "Multiple USD", "")
            ]
        )        
    
    enum_exportSelection: EnumProperty(
        name="Export Selection:",
        description="Which objects to export to USD(s)",
        items=[ ('OP1', "Only Selected Object", ""),
                ('OP2', "All Objects In Scene", ""),
                ('OP2', "Active Collection", "")
            ]
        )  

    enum_uvNames: EnumProperty(
        name="Export Selection:",
        description="Set the UV attribute name. USD usually needs st.",
        items=[ ('OP1', "st", ""),
                ('OP2', "UV", ""),
                ('OP2', "Keep", "")
            ]
        )  
    enum_nucleusFolders: EnumProperty(
        name="Export Selection:",
        description="Set the UV attribute name. USD usually needs st.",
        items=[ ('OP1', "Projects", ""),
                ('OP2', "User", ""),
                ('OP2', "Library", "")
            ]
        )  

