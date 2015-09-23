import bpy
import mathutils
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


def find_circle_center(p1, p2, p3):
  normal_12 = p2 - p1
  normal_13 = p3 - p1
  mid_12 = (p1 + p2) / 2
  mid_13 = (p1 + p3) / 2
  center_axis = mathutils.geometry.intersect_plane_plane(mid_12, normal_12,
      mid_13, normal_13)

  points_str = map(str, (p1, p2, p3))

  if not center_axis:
    raise Exception('Could not find center axis of %s, %s, %s' % points_str)

  center_axis_p1 = center_axis[0]
  center_axis_p2 = center_axis[0] + center_axis[1]

  circle_normal = normal_12.cross(normal_13)

  center_point = mathutils.geometry.intersect_line_plane(center_axis_p1,
      center_axis_p2, p1, circle_normal)

  if not center_point:
    raise Exception('Could not find center point of %s, %s, %s' % points_str)

  return center_point


class RobotPart(object):

  def __init__(self, filename, label, axis_up = 'Z', axis_forward = 'Y', mirror_x = False, mirror_y = False, mirror_z = False):
    if not label in bpy.data.objects:
      bpy.ops.import_mesh.stl(filepath=ROBOT_DIR + '/' + filename,
                              files=[{"name": filename}],
                              directory=ROBOT_DIR,
                              axis_up=axis_up,
                              axis_forward=axis_forward)
      bpy.context.selected_objects[0].name = label

      if mirror_x or mirror_y or mirror_z:
        bpy.ops.transform.mirror(constraint_axis = (mirror_x, mirror_y, mirror_z))
    self.label = label
    self.bpy_obj = bpy.data.objects[self.label]


class DriveBase(RobotPart):

  BOTTOM_PLANE_Z = 0.02619

  # Two points to help calculate the horizontal center of the base.
  HORIZONTAL_CENTER1 = (0.50648, -0.11303)
  HORIZONTAL_CENTER2 = (-0.50648, -0.05959)

  def __init__(self, label):
    super().__init__(ROBOT_PARTS[3], label, axis_up='Y', axis_forward='Z')

  def get_reference_point(self):
    point = self.bpy_obj.location.copy()
    point[0] = (self.HORIZONTAL_CENTER1[0] + self.HORIZONTAL_CENTER2[0]) / 2
    point[1] = (self.HORIZONTAL_CENTER1[1] + self.HORIZONTAL_CENTER2[1]) / 2
    point[2] += self.BOTTOM_PLANE_Z
    return point


class Elevator(RobotPart):

  BOTTOM_PLANE_Z = 0.0
  DIST_ELEVATOR_TO_BASE = 0.33682

  # TODO(phil): Figure out what this number is.
  # This is the distance from the center of the drive base to the center of
  # the elevator guides on the sides of the robot.
  DIST_TO_GUIDE = 0.48

  CIRCLE_POINTS = [
      mathutils.Vector((-0.04754, 0.14925, 0.07720)),
      mathutils.Vector((-0.04754, 0.12102, 0.11049)),
      mathutils.Vector((-0.04754, 0.12122, -0.00817)),
  ]
  OFF_CIRCLE_POINT = mathutils.Vector((-0.03942, 0.15211, 0.03365))

  def __init__(self, label, parent, mirrored=False):
    super().__init__(ROBOT_PARTS[2], label, axis_up='Y', axis_forward='Z', mirror_x=mirrored)
    self.parent = parent
    self.height = 0
    self.mirrored = mirrored
    self.local_reference = find_circle_center(*self.CIRCLE_POINTS)

  def set_height(self, height):
    self.height = height
    location = self.parent.get_reference_point()
    location[0] += self.DIST_TO_GUIDE if self.mirrored else -self.DIST_TO_GUIDE
    location[2] += self.DIST_ELEVATOR_TO_BASE - self.BOTTOM_PLANE_Z + height
    self.bpy_obj.location = location
    return self

  def get_reference_point(self):
     point = self.bpy_obj.location.copy() + self.local_reference
     return point


def main():
  drive_base = DriveBase('drive_base')
  elevator_left = Elevator('elevator_left', drive_base, mirrored=True)
  elevator_right = Elevator('elevator_right', drive_base, mirrored=False)

  elevator_left.set_height(0.0)
  elevator_right.set_height(0.3)

  print('foo=%s' % str(drive_base.get_reference_point()))
  print('foo=%s' % str(elevator_left.get_reference_point()))

main()
