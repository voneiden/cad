# Switch adapter for button caps

import cadquery as cq

from lib import cqlib

cq.Workplane.sub_edges = cqlib.sub_edges
cq.Workplane.rounded_rect = cqlib.rounded_rect
cq.Workplane.grid = cqlib.grid
cq.Workplane.panel_text = cqlib.panel_text
cq.Workplane.add_all = cqlib.add_all

tool_radius = 1.5875  # 1/8"
glue_point_distance = 2.5
glue_point_depth = 1
alphanum_led_space_radius = 3


result = cq.Workplane("XY").rect(20, 20, centered=True).extrude(2)
result = result.faces('>Z').workplane() \
    .moveTo(-glue_point_distance, 0).circle(tool_radius) \
    .moveTo(glue_point_distance, 0).circle(tool_radius) \
    .extrude(glue_point_depth)\
    .faces('>Z').workplane().circle(alphanum_led_space_radius).cutBlind(-1)
#.moveTo(0, glue_point_distance).circle(tool_radius) \
#.moveTo(0, -glue_point_distance).circle(tool_radius) \
