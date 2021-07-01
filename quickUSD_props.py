
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

