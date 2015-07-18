import bpy
import math

NUM_CUBES = 20
DISTANCE = 8

cubes = []

for i in range(0, NUM_CUBES):
    angle = i * 2 * math.pi / NUM_CUBES
    x = math.sin(angle) * DISTANCE
    y = math.cos(angle) * DISTANCE

    bpy.ops.mesh.primitive_cube_add(radius=1, location=(x, y, 0), \
            rotation=(0, 0, 0))

    cubes.append(bpy.context.active_object)
    cubes[-1].keyframe_insert(data_path='rotation_euler', frame=0)

    i += 1

scn = bpy.context.scene

for i in range(0, 50):
    for cube in cubes:
        cube.select = True

        cube.rotation_euler[0] += math.pi / 4
        cube.convert_space(from_space='LOCAL', to_space='WORLD')

        cube.keyframe_insert(data_path='rotation_euler', frame=10 * (i + 1))

        cube.select = False

# Move the camera further away
camera = bpy.data.objects['Camera']
camera.select = True
camera.location = (DISTANCE * 4, - DISTANCE * 4, DISTANCE * 3)
camera.select = False
