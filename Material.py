import bpy
import gpu

from mathutils import ( Matrix )
from gpu.types import ( GPUShader, GPUBatch )
from bpy.types import ( Collection )

data = {}

class Material:

    shader: GPUShader
    uniforms = []
    vertex = ""
    fragment = ""

    def __init__(self, shader, uniforms, vertex="", fragment=""):

        self.shader = shader
        self.uniforms = uniforms
        self.vertex = vertex
        self.fragment = fragment

class Uniform:

    name: str
    type: str

    def __init__(self, name, type):

        self.name = name
        self.type = type

    def __repr__(self): return self.name + "(" + self.type + ")"
    def __str__(self): return self.name + "(" + self.type + ")"

def make_from_path(vertex, fragment) -> Material:
            
    # shader container
    shader_info = gpu.types.GPUShaderCreateInfo()
    vert_out = gpu.types.GPUStageInterfaceInfo("shader")

    # vertex shader source
    source = open(bpy.path.abspath(vertex), "r").read()
    rows = source.split("\n")
    lines = []
    uniforms = []

    for row in rows:

        # manage uniforms
        if "uniform" in row:
            column = row.split(" ")
            type = column[1].upper()
            name = column[2].rstrip(';')
            shader_info.push_constant(type, name)
            uniforms.append(Uniform(name, type))

        if "uniform" not in row and "attribute" not in row and "varying" not in row:
            lines.append(row)

    shader_info.vertex_source("\n".join(lines))

    # vertex shader attributes
    shader_info.vertex_in(0, 'VEC3', "position")

    # vertex shader varying
    vert_out.smooth('VEC2', "uv")
    shader_info.vertex_out(vert_out)

    # fragment shader source
    source = open(bpy.path.abspath(fragment), "r").read()
    rows = source.split("\n")
    lines = []
    images = 0

    for row in rows:

        if "uniform" in row:
            column = row.split(" ")
            type = column[1].upper()
            name = column[2].rstrip(';')

            already = False
            for uniform in uniforms:
                if uniform.name == name:
                    already = True
                    break
            
            if not already:
                uniforms.append(Uniform(name, type))
                
                if "SAMPLER2D" in type:
                    shader_info.sampler(images,"FLOAT_2D", name)
                    images += 1

                else:
                    shader_info.push_constant(type, name)

        elif "varying" not in row and "vec4 FragColor;" not in row:
            lines.append(row)

    shader_info.fragment_source("\n".join(lines))

    # fragment shader out
    shader_info.fragment_out(0, 'VEC4', "FragColor")

    shader = gpu.shader.create_from_info(shader_info)
    
    del vert_out
    del shader_info
    
    return Material(shader, uniforms, vertex, fragment)

def update(objects):

    # print(metadatas)
    # for id in data.keys():
    #     recycle = True
    #     for object in objects:
    #         if id == object.name:
    #             recycle = False
    #             break
    #     # actually recycle

    for object in objects:
        id = object.name
        metadata = object.metadata
        if id in data:
            if data[id].fragment != metadata.fragment \
            or data[id].vertex != metadata.vertex:
                data[id] = make_from_path(metadata.vertex, metadata.fragment)
            # check update

        else:

            # create and store material
            material = make_from_path(metadata.vertex, metadata.fragment)
            data[id] = material

            # create settings from uniforms
            for uniform in material.uniforms:
                if uniform.type == "FLOAT":
                    already = False
                    for setting in metadata.settings:
                        if uniform.name == setting.name:
                            uniform.value = setting.value
                            already = True
                            break

                    if not already:
                        setting = metadata.settings.add()
                        setting.name = uniform.name
                        setting.value = 1

            
