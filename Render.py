import bpy
import gpu
import mathutils

from . import Mesh
from . import Image
from . import Material
from mathutils import ( Matrix )

shared: dict = {}

shared["tick"] = 0
shared["time"] = 0
shared["viewMatrix"] = Matrix.Identity(4)
shared["windowMatrix"] = Matrix.Identity(4)
shared["viewMatrixInvert"] = Matrix.Identity(4)
shared["windowMatrixInvert"] = Matrix.Identity(4)

def draw(object):

    gpu.state.depth_test_set('LESS_EQUAL')
    gpu.state.depth_mask_set(True)

    update_uniforms(object)
    id = object.name
    mesh = Mesh.data[id]
    material = Material.data[id]
    batch = mesh.batch
    instances = object.metadata.instances

    if instances > 1:
        batch.draw_instanced(material.shader, instance_count=instances)
    else:
        batch.draw(material.shader)

    gpu.state.depth_mask_set(False)

def update_matrix(windowMatrix, viewMatrix):
    
    shared["viewMatrix"] = viewMatrix
    shared["windowMatrix"] = windowMatrix
    shared["viewMatrixInvert"] = viewMatrix.inverted()
    shared["windowMatrixInvert"] = windowMatrix.inverted()

def update_uniforms(object):

    id = object.name
    material = Material.data[id]
    shader = material.shader
    uniforms = material.uniforms
    for uniform in uniforms:

        name = uniform.name

        if name == "worldMatrix":
            try: shader.uniform_float(name, object.matrix_world)
            except: pass

        elif name in Image.images:
            try: shader.uniform_sampler(name, Image.images[name])
            except: pass

        elif name in shared:
            try: shader.uniform_float(name, shared[name])
            except: pass

        else:
            for setting in object.metadata.settings:
                if name == setting.name:
                    try: shader.uniform_float(name, setting.value)
                    except: pass