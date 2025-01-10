import bpy

class Setting(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty()
    value: bpy.props.FloatProperty()

class Metadata(bpy.types.PropertyGroup):

    vertex: bpy.props.StringProperty(
        name="Vertex",
        default="//shader/mesh.vert",
        subtype='FILE_PATH')
    
    fragment: bpy.props.StringProperty(
        name="Fragment",
        default="//shader/mesh.frag",
        subtype='FILE_PATH')
    
    settings: bpy.props.CollectionProperty(
        name="Settings",
        type=Setting)
    
    instances: bpy.props.IntProperty(
        name="Instances",
        default=1,
    )

class FrameData(bpy.types.PropertyGroup):

    frames: bpy.props.IntProperty(
        name="Frames",
        default=1,
    )