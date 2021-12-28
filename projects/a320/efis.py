from itertools import chain

import cadquery as cq
from cadquery.selectors import BoxSelector, StringSyntaxSelector

from lib import cqlib
from lib.arc_calc import rotate
from lib.rotary_selector import create_rotary_selector_arc

"""
A320 EFIS

TODO: fillet the button edges
TODO: add vertical line seperator
"""

cq.Workplane.sub_edges = cqlib.sub_edges
cq.Workplane.rounded_rect = cqlib.rounded_rect
cq.Workplane.grid = cqlib.grid
cq.Workplane.panel_text = cqlib.panel_text




cq.Workplane.add_all = cqlib.add_all

tool_radius = 1.5875  # 1/8"

width = 154
half_width = width / 2
left_height = 80
half_left_height = left_height / 2
right_height = 90
half_right_height = right_height / 2

result = cq.Workplane("XY")

result.moveTo(-half_width, 35).line(0, -left_height).line(width, 0).line(0, right_height) \
    .spline([(half_width, 45), (0, 42.6), (-half_width, 35)]).close()

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
result = result.grid(xd=(2.34, 49.5, 2), yp=[-5.81 - 24.79]).circle(13.3 / 2)
result = result.grid(xd=(2.34, 49.5, 2), yp=[-5.81 - 24.79]).circle(15.3 / 2)
result = result.cutBlind(-0.1).faces('>Z').workplane()

last = None

# Rose Arc
rose_inner = create_rotary_selector_arc((-11.5, 0), 1, 180, [0, 45, 90, 135, 180], []).close().vals()
rose_outer_lower = create_rotary_selector_arc((-21, 0), 1, 35, [0], round_end=True).close().vals()
rose_outer_upper = create_rotary_selector_arc(rotate((0, 21), -35), 1, 35, [35], round_start=True).close().vals()

text_rose = cq.Workplane().center(-17, 15).panel_text("ROSE").wires('>Z').vals()
text_ils = cq.Workplane().center(-17, 1).panel_text("ILS").wires('>Z').vals()
text_vor = cq.Workplane().center(-14, 10).panel_text("VOR").wires('>Z').vals()
text_nav = cq.Workplane().center(-0.5, 17).panel_text("NAV").wires('>Z').vals()
text_arc = cq.Workplane().center(14, 10).panel_text("ARC").wires('>Z').vals()
text_plan = cq.Workplane().center(19, 1).panel_text("PLAN").wires('>Z').vals()

result = result.add_all(rose_inner + rose_outer_lower + rose_outer_upper + text_rose + text_ils + text_vor + text_nav + text_arc + text_plan, 2.34, -5.81)



ranges = [0, 45, 90, 135, 180, 235]
range_labels = ["10", "20", "40", "80", "160", "320"]

range_arc = create_rotary_selector_arc((-11.5, 0), 1, 235, [], ranges, round_start=False, round_end=False).close().vals()
range_texts = list(chain.from_iterable(
    [cq.Workplane().center(*rotate((-16.5, 0), angle)).panel_text(label).wires('>Z').vals() for angle, label in zip(ranges, range_labels)]))

result = result.add_all(range_arc + range_texts, 51.84, -5.81)

# ADF
adf_1_title = cq.Workplane().center(-0.5, 10).panel_text("1").wires('>Z').vals()
adf_2_title = cq.Workplane().center(-0.5, 10).panel_text("2").wires('>Z').vals()
adf_texts = list(chain.from_iterable([
    cq.Workplane().center(-14, 0).panel_text("ADF").wires('>Z').vals(),
    cq.Workplane().center(14, 0).panel_text("VOR").wires('>Z').vals(),
    cq.Workplane().center(-0.5, -11).panel_text("OFF").wires('>Z').vals(),
]))
result = result.add_all(adf_texts + adf_1_title, 2.34, -30.6)
result = result.add_all(adf_texts + adf_2_title, 51.84, -30.6)

baro_arc = create_rotary_selector_arc(rotate((0, 12), -22.5), 1, 45, [], [0, 45]).close().vals()
text_inHg = cq.Workplane().center(-7, 16).panel_text("in Hg").wires('>Z').vals()
text_hPa = cq.Workplane().center(7, 16).panel_text("hPa").wires('>Z').vals()
result = result.add_all(baro_arc + text_inHg + text_hPa, -45.5, -12.5)

result = result.cutBlind(-0.5).faces(">Z").workplane()
# Fillet the buttons

result = result.grid(xd=(-13.12, 19.13, 5), yp=[25.74]).rounded_rect(16.5, 14.5, 2.5)
result = result.cutBlind(-1)

selector = BoxSelector((-13.12-16.5/2-0.9, 25.74+14.5/2+0.9, 1), (-13.12+16.5/2+0.9, 25.74-14.5/2-0.9, 2.5))
selector2 = BoxSelector((-13.12-16.5/2+0.9, 25.74+14.5/2-0.9, 1), (-13.12+16.5/2-0.9, 25.74-14.5/2+0.9, 2.5))
inner_edges = result.edges(selector2 - StringSyntaxSelector('|Z'))
outer_edges = result.sub_edges(inner_edges, selector - StringSyntaxSelector('|Z')).fillet(0.99)
#result = result.edges(BoxSelector((-22.5, 32.5, 1), (72.5, 17.5, 5))).fillet(-1)
#xx = result.workplane(2).center(25, 25).rect(95, 15)
#xx = result.workplane(2).center(-45, -35).rect(35, 15)
