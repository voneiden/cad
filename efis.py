import cadquery as cq
from cadquery import Vector

import lib
import arc_calc as ac

cq.Workplane.sub_edges = lib.sub_edges
cq.Workplane.rounded_rect = lib.rounded_rect
cq.Workplane.grid = lib.grid

tool_radius = 1.5875  # 1/8"

width = 154
half_width = width / 2
left_height = 80
half_left_height = left_height / 2
right_height = 90
half_right_height = right_height / 2

result = cq.Workplane("XY")#.rect(width, height, True)

result.moveTo(-half_width, 35).line(0, -left_height).line(width, 0).line(0, right_height)\
    .spline([(half_width, 45),  (0, 42.6), (-half_width, 35)]).close()

# Rotary and flip switches
result = result.grid(xd=(2.34, 49.5, 2), yd=(-5.81, -24.79, 2)).circle(5)
result = result.grid(xp=[-45.5], yp=[-12.5]).circle(5)

# Top buttons
result = result.grid(xd=(-13.12, 19.13, 5), yp=[25.74]).rounded_rect(14.5, 12.5, tool_radius)

# Bottom buttons
result = result.grid(xd=(-54.62, 19.13, 2), yp=[-34.26]).rounded_rect(14.5, 12.5, tool_radius)

# Screen cutout
result = result.pushPoints([(-45.86, 17.59)]).rounded_rect(31.5, 14.5, tool_radius)

# Mount holes
result = result.pushPoints([(-72, 30), (-72, -40), (72, 40), (72, -40)]).circle(3)

result = result.extrude(3).faces('>Z').workplane()

# Arcs
result = result.grid(xd=(2.34, 49.5, 2), yp=[-5.81 - 24.79]).circle(13.3/2)
result = result.grid(xd=(2.34, 49.5, 2), yp=[-5.81 - 24.79]).circle(15.3/2)
result = result.cutBlind(-0.1)

# Rose Arc
rose_inner_arc_inside = ac.arc((-11.5, 0), 180)
rose_inner_arc_outer0 = ac.arc((12.5, 0), 0, -1)  # PLAN
rose_inner_arc_outer1 = ac.arc(rose_inner_arc_outer0[1], -45, 1.5)
rose_inner_arc_outer2 = ac.arc(rose_inner_arc_outer1[1], 0, -1)  # ARC
rose_inner_arc_outer2a = ac.arc((13.5, 0), -45, 0.5)
rose_inner_arc_outer2b = ac.arc((13.5, 0), -45, -0.5)
rose_inner_arc_outer3 = ac.arc(rose_inner_arc_outer2[1], -45, 1)
rose_inner_arc_outer4 = ac.arc(rose_inner_arc_outer3[1], 0, -1)  # NAV
rose_inner_arc_outer4a = ac.arc((13.5, 0), -90, 0.5)
rose_inner_arc_outer4b = ac.arc((13.5, 0), -90, -0.5)
rose_inner_arc_outer5 = ac.arc(rose_inner_arc_outer4[1], -45, 1)
rose_inner_arc_outer6 = ac.arc(rose_inner_arc_outer5[1], 0, -1)  # VOR
rose_inner_arc_outer6a = ac.arc((13.5, 0), -135, 0.5)
rose_inner_arc_outer6b = ac.arc((13.5, 0), -135, -0.5)
rose_inner_arc_outer7 = ac.arc(rose_inner_arc_outer6[1], -45, 1.5)
rose_inner_arc_outer8 = ac.arc(rose_inner_arc_outer7[1], 0, -1)  # ILS
rose_inner = cq.Workplane().moveTo(-11.5, 0)\
    .threePointArc(*rose_inner_arc_inside)\
    .line(2, 0).line(0, 1).lineTo(*rose_inner_arc_outer0[1])\
    .threePointArc(*rose_inner_arc_outer1) \
    .lineTo(*rose_inner_arc_outer2a[1]) \
    .lineTo(*rose_inner_arc_outer2b[1]) \
    .lineTo(*rose_inner_arc_outer2[1]) \
    .threePointArc(*rose_inner_arc_outer3) \
    .lineTo(*rose_inner_arc_outer4a[1]) \
    .lineTo(*rose_inner_arc_outer4b[1]) \
    .lineTo(*rose_inner_arc_outer4[1]) \
    .threePointArc(*rose_inner_arc_outer5) \
    .lineTo(*rose_inner_arc_outer6a[1]) \
    .lineTo(*rose_inner_arc_outer6b[1]) \
    .lineTo(*rose_inner_arc_outer6[1]) \
    .threePointArc(*rose_inner_arc_outer7) \
    .line(-1, 0).line(0, -1) \
    .close().vals()

# Outer rose, lower shape
rose_outer1_arc1 = ac.arc((-21, 0), 35)
rose_outer1_arc2_offset = ac.unit(rose_outer1_arc1[1], -0.5)
rose_outer1_arc2 = ac.add_previous_arc(ac.arc(rose_outer1_arc2_offset, -180, 0), ac.sum(ac.rotate(rose_outer1_arc2_offset, 180), rose_outer1_arc1[1]))
rose_outer1_arc3 = ac.arc(rose_outer1_arc2[1], -35)

# TODO calc line end via arc?
rose_outer1 = cq.Workplane().moveTo(-21, 0) \
    .line(1, 0).line(0, 1).line(-1, 0) \
    .threePointArc(*rose_outer1_arc1) \
    .threePointArc(*rose_outer1_arc2) \
    .threePointArc(*rose_outer1_arc3).close().vals()


# Outer rose, upper shape
rose_outer2_arc1 = ac.arc((0, 21), -35)
rose_outer2_arc2_offset = ac.unit(rose_outer2_arc1[1], -0.5)
rose_outer2_arc2 = ac.add_previous_arc(ac.arc(rose_outer2_arc2_offset, 180, 0), ac.sum(ac.rotate(rose_outer2_arc2_offset, 180), rose_outer2_arc1[1]))
rose_outer2_arc3 = ac.arc(rose_outer2_arc2[1], 35, 0.5)

rose_outer2 = cq.Workplane().moveTo(0.5, 21) \
    .line(0, -1).line(-1, 0).line(0, 1) \
    .threePointArc(*rose_outer2_arc1) \
    .threePointArc(*rose_outer2_arc2) \
    .threePointArc(*rose_outer2_arc3) \
    .close().vals()

ro1r1 = cq.Workplane().center(-22, 0.5).rect(1.5, 1).vals()

text_rose = cq.Workplane().center(-17, 15).text("ROSE", 4, -5, fontPath='./fonts/xA320PanelFont_V0.2b.ttf').wires('>Z').vals()
text_ils = cq.Workplane().center(-17, 1).text("ILS", 4, -5, fontPath='./fonts/xA320PanelFont_V0.2b.ttf').wires('>Z').vals()
text_vor = cq.Workplane().center(-14, 10).text("VOR", 4, -5, fontPath='./fonts/xA320PanelFont_V0.2b.ttf').wires('>Z').vals()
text_nav = cq.Workplane().center(-0.5, 17).text("NAV", 4, -5, fontPath='./fonts/xA320PanelFont_V0.2b.ttf').wires('>Z').vals()
text_arc = cq.Workplane().center(14, 10).text("ARC", 4, -5, fontPath='./fonts/xA320PanelFont_V0.2b.ttf').wires('>Z').vals()
text_plan = cq.Workplane().center(19, 1).text("PLAN", 4, -5, fontPath='./fonts/xA320PanelFont_V0.2b.ttf').wires('>Z').vals()


def add_all(self, objs, x, y):
    objs = list(objs)
    return self.pushPoints(((x, y) for _ in range(len(objs)))).eachpoint(lambda loc: objs.pop().moved(loc), True)
cq.Workplane.add_all = add_all

result = result.add_all(rose_inner + rose_outer1 + rose_outer2 + text_rose + text_ils + text_vor + text_nav + text_arc + text_plan, 2.34, -5.81)
result = result.cutBlind(-0.5)

#tmp_debug = result.add_all(tmp_debug.vals(), 2.34, -5.81)
#tmp_debug2 = result.add_all(tmp_debug2.vals(), 2.34, -5.81)
# Text
#result = result.workplane(2).text("Hello world", 12, -4)

#result = result.workplane(3).text("EFIS", 12, -5, fontPath='./fonts/xA320PanelFont_V0.2b.ttf')
