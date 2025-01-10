import bpy
import numpy as np

from bpy.types import ( Mesh, Collection )
from gpu.types import ( GPUBatch, GPUVertBuf, GPUVertFormat, GPUIndexBuf )

data = {}

class Mesh():

    batch: GPUBatch
    vertex_count: int = 0

    def __init__(self, batch, vertex_count):

        self.batch = batch
        self.vertex_count = vertex_count

def make_plane() -> GPUBatch:

    positions = [(-1, 1, 0), (-1, -1, 0), (1, -1, 0), (1, 1, 0)]
    indices = [(0,1,2), (2,3,0)]
    vertex_count = 4

    attributes = GPUVertFormat()
    attributes.attr_add(id="position", comp_type="F32", len=3, fetch_mode="FLOAT")
    buffer = GPUVertBuf(attributes, vertex_count)
    buffer.attr_fill(id="position", data=positions)
    index_buffer = GPUIndexBuf(type='TRIS', seq=indices)

    return Mesh(
        GPUBatch(type='TRIS', buf=buffer, elem=index_buffer),
        vertex_count
    )

def make_batch(mesh: Mesh) -> GPUBatch:

    mesh.calc_loop_triangles()
    vertices = np.empty((len(mesh.vertices), 3), 'f')
    indices = np.empty((len(mesh.loop_triangles), 3), 'i')
    mesh.vertices.foreach_get("co", np.reshape(vertices, len(mesh.vertices) * 3))
    mesh.loop_triangles.foreach_get("vertices", np.reshape(indices, len(mesh.loop_triangles) * 3))
    vertex_count = len(mesh.vertices)

    attributes = GPUVertFormat()
    attributes.attr_add(id="position", comp_type="F32", len=3, fetch_mode="FLOAT")
    buffer = GPUVertBuf(attributes, vertex_count)
    buffer.attr_fill(id="position", data=vertices)
    index_buffer = GPUIndexBuf(type='TRIS', seq=indices)

    return Mesh(
        GPUBatch(type='TRIS', buf=buffer, elem=index_buffer),
        vertex_count
    )

def update(objects: Collection):

    for id in data.keys():
        recycle = True
        for object in objects:
            if id == object.name:
                recycle = False
                break
        # actually recycle

    for object in objects:
        id = object.name
        if id in data:
            # check update
            if data[id].vertex_count != len(object.data.vertices):
                data[id] = make_batch(object.data)

        else:
            data[id] = make_batch(object.data)