import bpy

from bpy.types import ( Object )
from os.path import ( splitext )

from . import Engine
from . import Metadata
from . import Material

class RenderPanel(bpy.types.Panel):

    bl_label = "Render Settings"
    bl_idname = "RENDER_PT_Settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):

        layout = self.layout
        
        layout.use_property_split = True
        layout.use_property_decorate = False
        
        # resolution
        box = layout.box()
        keys = [ "resolution_x", "resolution_y", "resolution_percentage" ]
        for key in keys:
            box.prop(context.scene.render, key)

        # frame rate
        box = layout.box()
        keys = [ "fps" ]
        for key in keys:
            box.prop(context.scene.render, key)
        box.prop(context.scene.framedata, "frames")

class DataPanel(bpy.types.Panel):

    bl_label = "Data Settings"
    bl_idname = "DATA_PT_Settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context):

        layout = self.layout
        
        layout.use_property_split = True
        layout.use_property_decorate = False

        object = context.object

        if object != None:
            if isinstance(object.data, bpy.types.Camera):
                box = layout.box()
                box.prop(object.data, "lens")

class MaterialPanel(bpy.types.Panel):

    bl_label = "Material Settings"
    bl_idname = "MATERIAL_PT_Settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    def draw(self, context):

        layout = self.layout
        object = context.object

        if object != None:
            layout.use_property_split = True
            layout.use_property_decorate = False

            # vertex shader
            box = layout.box()
            metadata = object.metadata
            box.prop(metadata, "instances")
            box.prop(metadata, "vertex")
            box.prop(metadata, "fragment")
            for setting in metadata.settings:
                box.prop(setting, "value", text=setting.name.capitalize())

def get_panels():

    panels = []
    exclude_panels = { 'VIEWLAYER_PT_filter', 'VIEWLAYER_PT_layer_passes', }
    include_panels = { 'EEVEE_MATERIAL_PT_context_material', 'MATERIAL_PT_preview', }
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES'):
            if (('BLENDER_RENDER' in panel.COMPAT_ENGINES and panel.__name__ not in exclude_panels)
                or panel.__name__ in include_panels):
                panels.append(panel)

    return panels