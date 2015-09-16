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


class RobotPart(object):

  def __init__(self, filename, label, axis_up = 'Z', axis_forward = 'Y'):
    bpy.ops.import_mesh.stl(filepath=ROBOT_DIR + '/' + filename,
                            files=[{"name": filename}],
                            directory=ROBOT_DIR,
                            axis_up=axis_up,
                            axis_forward=axis_forward)
    bpy.context.selected_objects[0].name = label
    self.label = label
    self.bpy_obj = bpy.data.objects[self.label]


class DriveBase(RobotPart):

  BOTTOM_PLANE_Z = 0.02619

  def __init__(self, label):
    super().__init__(ROBOT_PARTS[3], label, axis_up='Y', axis_forward='Z')

  def get_reference_point(self):
    point = self.bpy_obj.location.copy()
    point[2] += self.BOTTOM_PLANE_Z
    return point


class Elevator(RobotPart):

  BOTTOM_PLANE_Z = 0.0
  DIST_ELEVATOR_TO_BASE = 0.33682

  def __init__(self, label, parent, mirrored=False):
    super().__init__(ROBOT_PARTS[2], label, axis_up='Y', axis_forward='Z')
    self.parent = parent
    self.height = 0
    self.mirrored = mirrored

  def set_height(self, height):
    self.height = height
    self.bpy_obj.location = self.parent.get_reference_point()
    self.bpy_obj.location[2] += (self.DIST_ELEVATOR_TO_BASE - 
        self.BOTTOM_PLANE_Z)
    return self


def main():
  drive_base = DriveBase('drive_base')
  elevator_left = Elevator('elevator_left', drive_base, mirrored=False)
  elevator_right = Elevator('elevator_right', drive_base, mirrored=True)

  elevator_left.set_height(0.3)

  print('foo=%s' % str(drive_base.get_reference_point()))

main()
