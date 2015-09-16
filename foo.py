import bpy
import math
import inspect
import os

ROBOT_PARTS = [
    '971-15-A-3200_Fridge.STL',
    '971-15-A-4800_Arm Assembly.STL',
    '971-15-A-5900_Elevator Carriage Mirrored.STL',
    '971-15-A-1100_DrivebaseStructure.STL',
]

ROBOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(
            inspect.getfile(
                inspect.currentframe()))))

DIST_ELEVATOR_TO_BASE = 0.33682


class RobotPart(object):

  def __init__(self, filename, label, axis_up = 'Z', axis_forward = 'Y'):
    bpy.ops.import_mesh.stl(filepath=ROBOT_DIR + '/' + filename,
                            files=[{"name": filename}],
                            directory=ROBOT_DIR,
                            axis_up=axis_up,
                            axis_forward=axis_forward)
    bpy.context.selected_objects[0].name = label
    self.bpy_obj = bpy.data.objects[label]
    self.label = os.path.splitext(filename)

  def set_default_rotation(self, x, y, z):
    pass


class DriveBase(RobotPart):

  def __init__(self, label):
    super().__init__(ROBOT_PARTS[3], label, axis_up='Y', axis_forward='Z')


class Elevator(RobotPart):

  def __init__(self, distance_at_zero_height, label, mirrored=False):
    super().__init__(ROBOT_PARTS[2], label, axis_up='Y', axis_forward='Z')
    self.distance_at_zero_height = distance_at_zero_height
    self.height = 0
    self.mirrored = mirrored

  def set_height(self, height):
    self.height = height


def main():
  drive_base = DriveBase('drive_base')
  elevator_left = Elevator(DIST_ELEVATOR_TO_BASE, 'elevator_left', 
      mirrored=False)
  elevator_right = Elevator(DIST_ELEVATOR_TO_BASE, 'elevator_right', 
      mirrored=True)

main()
