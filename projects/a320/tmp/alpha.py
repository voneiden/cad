# Alpha button caps

import cadquery as cq

from lib import cqlib
from switch_adapter import tool_radius, glue_point_depth, glue_point_distance

cq.Workplane.sub_edges = cqlib.sub_edges
cq.Workplane.rounded_rect = cqlib.rounded_rect
cq.Workplane.grid = cqlib.grid
cq.Workplane.panel_text = cqlib.panel_text
cq.Workplane.add_all = cqlib.add_all

width = 10 - 0.2
height = 10 - 0.2
depth = 3

chamfer_radius = 1
engraving_depth = 0.1
srad = 10


def button(letter):
    result = cq.Workplane("XY").rounded_rect(width, height, tool_radius)
    result = result.extrude(depth)
    result = result.faces('>Z').fillet(chamfer_radius)

    sphere_offset = srad - 0.5 + depth
    engraving_sphere = cq.Workplane("XY").workplane(offset=sphere_offset).sphere(srad + engraving_depth)
    engraving_letter = (cq.Workplane("XY").workplane(offset=sphere_offset)
                        .panel_text(letter, 6, -srad - engraving_depth, fontPath='../../../fonts/blockschrift.ttf')
                        )
    projected_letter = engraving_sphere.intersect(engraving_letter, clean=True)
    detent_sphere = cq.Workplane("XY").workplane(offset=sphere_offset).sphere(srad)

    result = result.cut(detent_sphere, clean=True)
    result = result.cut(projected_letter, clean=True)

    result = result.faces('<Z').workplane().circle(3).cutBlind(-1.5)
    result = (result.faces('<Z').workplane()
              .moveTo(-glue_point_distance, 0).circle(tool_radius)
              .moveTo(glue_point_distance, 0).circle(tool_radius)
              .cutBlind(-glue_point_depth)
              )
    return result


result = button("A")

# test = cq.Workplane("XY").sphere(srad + engraving_depth)

# test = test.intersect(letter, clean=True)
# test = test.center(0, 0).sphere(srad)
