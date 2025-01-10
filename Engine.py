import bpy
import gpu
from . import Render
from . import Mesh
from . import Material

engines = []

class Engine(bpy.types.RenderEngine):

    bl_idname = "Shader"
    bl_label = "Shader"
    bl_use_preview = True
    bl_use_gpu_context = True

    def __init__(self):
        engines.append(self)

    def view_update(self, context, depsgraph):

        meshes = []
        for object in context.scene.objects:
            if isinstance(object.data, bpy.types.Mesh):
                meshes.append(object)
                
        Mesh.update(meshes)
        Material.update(meshes)
    
    def view_draw(self, context, depsgraph):
        windowMatrix = context.region_data.window_matrix
        viewMatrix = bpy.context.region_data.view_matrix
        Render.update_matrix(windowMatrix, viewMatrix)
        self.bind_display_space_shader(depsgraph.scene)

        for object in context.scene.objects:
            if isinstance(object.data, bpy.types.Mesh):
                if object.visible_get():
                    Render.draw(object)
                    
        Render.shared["tick"] += 1
        Render.shared["time"] = Engine.get_time(depsgraph)
        self.unbind_display_space_shader()

    def render(self, depsgraph):
        scene = depsgraph.scene
        width = self.render.resolution_x
        height = self.render.resolution_y
        offscreen = gpu.types.GPUOffScreen(width, height, format="RGBA32F")
        with offscreen.bind():
            windowMatrix = scene.camera.calc_matrix_camera(
                depsgraph,
                x=width,
                y=height,
            )
            viewMatrix = scene.camera.matrix_world.inverted()
            Render.update_matrix(windowMatrix, viewMatrix)
            self.bind_display_space_shader(depsgraph.scene)

            for object in scene.objects:
                if isinstance(object.data, bpy.types.Mesh):
                    if object.visible_get():
                        Render.draw(object)
                        
            Render.shared["tick"] += 1
            self.unbind_display_space_shader()

        result = self.begin_result(0, 0, width, height)
        layer = result.layers[0].passes["Combined"]
        array = offscreen.texture_color.read()
        array = [item for sub_list in array for item in sub_list]
        layer.rect = array
        self.end_result(result)
        offscreen.free()
        del offscreen

    # https://github.com/KoltesDigital/shiba/blob/master/blender/shiba/render_engine.py
    @staticmethod
    def get_time(depsgraph):
        scene = depsgraph.scene
        actual_fps = scene.render.fps / scene.render.fps_base
        time = scene.frame_current / actual_fps
        return time