import bpy
import math

NUM_CUBES = 20
DISTANCE = 8

for i in range(0, NUM_CUBES):
    angle = i * 2 * math.pi / NUM_CUBES
    x = math.sin(angle) * DISTANCE
    y = math.cos(angle) * DISTANCE

    bpy.ops.mesh.primitive_cube_add(radius=1, location=(x, y, 0), \
            rotation=(0, 0, 0))

    i += 1
