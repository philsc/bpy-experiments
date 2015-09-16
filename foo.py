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

  def __init__(self, filename, label):
    bpy.ops.import_mesh.stl(filepath=ROBOT_DIR + '/' + filename,
                            files=[{"name": filename}],
                            directory=ROBOT_DIR)
    self.bpy_obj = None
    self.label = label


class DriveBase(RobotPart):

  def __init__(self):
    super().__init__(ROBOT_PARTS[3], 'drive_base')


class Elevator(RobotPart):

  def __init__(self, distance_at_zero_height):
    super().__init__(ROBOT_PARTS[2], 'elevator')
    self.distance_at_zero_height = distance_at_zero_height
    self.height = 0

  def set_height(self, height):
    self.height = height


def main():
  drive_base = DriveBase()
  elevator = Elevator(0.33682)

main()
