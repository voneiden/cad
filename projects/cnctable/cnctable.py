import math

import cadquery as cq

from lib.cqlib import rounded_rect




cq.Workplane.rounded_rect = rounded_rect


# Cold formed internal/external radius: 1t and 2t when t<6mm
# Hot formed 1.5t external
def create_tube(length):
    tube = cq.Workplane("XY")
    tube = tube.pushPoints([(0, 0)]).rounded_rect(30, 30, 3)
    tube = tube.pushPoints([(0, 0)]).rounded_rect(28, 28, 2)
    tube = tube.extrude(length)
    tube.faces(">Z").tag("zp").end()
    tube.faces("<Z").tag("zn").end()
    tube.faces(">Y").tag("yp").end()
    tube.faces("<Y").tag("yn").end()
    tube.faces(">X").tag("xp").end()
    tube.faces("<X").tag("xn").end()
    return tube

table = (
    cq.Assembly()
    .add(cq.Workplane("XY").tag("up"), name="floor")
    .add(create_tube(300), name="desk1")
    .add(create_tube(300), name="desk2")
    #.add(create_tube(300), name="hleft")
    #.add(create_tube(300), name="hbottom")
    #.constrain("desk1?yn", "X", "Axis")
    .constrain("desk1?zp", "desk2?xp", "Axis", param=math.pi)
    .constrain("desk1?zp", "desk2?xp", "Point")
    #.constrain("hright?top", "hbottom@faces@>Z", "Plane")
    #.constrain("hbottom?top", "hleft@faces@>Y", "Plane")
    #.constrain("hleft?top", "htop@faces@>Y", "Plane")
)

table.solve()

show_object(table, name='door')
