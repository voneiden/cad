# Alpha button caps

import cadquery as cq

from lib import cqlib

cq.Workplane.sub_edges = cqlib.sub_edges
cq.Workplane.rounded_rect = cqlib.rounded_rect
cq.Workplane.grid = cqlib.grid
cq.Workplane.panel_text = cqlib.panel_text
cq.Workplane.add_all = cqlib.add_all


inner_radius = 10
depth = 0.1



tool_radius = 1.5875  # 1/8"
inner_sphere = cq.Workplane("XY").sphere(inner_radius)
outer_sphere = cq.Workplane("XY").sphere(inner_radius + depth)
text_rose = cq.Workplane("XY").panel_text("A", fontsize=8, font="Monospace", fontPath=None).wires('>Z').vals()
text = cq.Workplane("XY").workplane(offset=inner_radius+depth)
text = text.add_all(text_rose, -0.25, 0)
text = text.extrude((inner_radius+depth) * -2)

union = outer_sphere.intersect(text)
final = union.cut(inner_sphere, clean=True)

