import cadquery as cq

from cq_cam import JobV2
from lib import cqlib

cqlib.setup(locals())

frame_inner_x = 18
top_frame_y = 14
frame_y = 10
coupler_height = 3
frame_inner_z = 21.4 + coupler_height

thickness = 3
margin = 1
tool_diameter = 1
tool_radius = tool_diameter / 2

top_slot_center_x = frame_inner_x/2 + margin + thickness/2

top_frame = (
    cq.Workplane()
    .rect(frame_inner_x + 2*(thickness + margin * 2), top_frame_y)
    .extrude(thickness)
    .faces('>Z').workplane()
    .circle(5)
    .center(-top_slot_center_x, 0)
    .rounded_rect(thickness, frame_y - 2 * margin, tool_radius)
    .center(2*top_slot_center_x, 0)
    .rounded_rect(thickness, frame_y - 2 * margin, tool_radius)
    .cutThruAll()
)

bottom_frame = (
    cq.Workplane()
        .rect(frame_inner_x + 2*(thickness + margin * 2), top_frame_y)
        .extrude(thickness)
        .faces('>Z').workplane()
        .center(-top_slot_center_x, 0)
        .rounded_rect(thickness, frame_y - 2 * margin, tool_radius)
        .center(2*top_slot_center_x, 0)
        .rounded_rect(thickness, frame_y - 2 * margin, tool_radius)
        .cutThruAll()
)

side_frame = (
    cq.Workplane('XY')
    .line(0, frame_y/2 - margin)
    .line(thickness, 0)
    #.ellipseArc(tool_radius, tool_radius, 0, 90, 270)
    .line(0, margin)
    .line(frame_inner_z/2, 0)
    .line(0, -frame_y/2)
    .close()
    .extrude(3)
)

side_frame = (
    side_frame
    .mirror(side_frame.faces('>X'), union=True)
    .mirror(side_frame.faces('<Y'), union=True)
)


assembly = (
    cq.Assembly()
    .add(top_frame, name='top')
    .add(side_frame,
         loc=cq.Location(
             cq.Vector(frame_inner_x/2 + margin, 0, thickness),
             cq.Vector(0, 1, 0),
             90),
         name='side1')
    .add(side_frame,
         loc=cq.Location(
             cq.Vector(-frame_inner_x/2 - margin - thickness, 0, thickness),
             cq.Vector(0, 1, 0),
             90),
         name='side2')
    .add(bottom_frame,
         loc=cq.Location(
             cq.Vector(0, 0, -frame_inner_z - thickness)),
         name='bottom')
)

cam_top = (
    JobV2(
        name='Top',
        top=top_frame.faces('>Z').workplane().plane,
        feed=300,
        tool_diameter=1.0,
        plunge_feed=100)
    .profile(top_frame.faces('<Z'), inner_offset=-1, stepdown=1)
    .profile(top_frame.faces('<Z'), outer_offset=1, stepdown=1)
)

cam_side = (
    JobV2(
        name='Side',
        top=side_frame.faces('>Z').workplane().plane,
        feed=300,
        tool_diameter=1.0,
        plunge_feed=100)
    .profile(side_frame.faces('<Z'), inner_offset=-1, stepdown=1)
    .profile(side_frame.faces('<Z'), outer_offset=1, stepdown=1)
)

cam_bottom = (
    JobV2(
        name='Bottom',
        top=bottom_frame.faces('>Z').workplane().plane,
        feed=300,
        tool_diameter=1.0,
        plunge_feed=100)
    .profile(bottom_frame.faces('<Z'), inner_offset=-1, stepdown=1)
    .profile(bottom_frame.faces('<Z'), outer_offset=1, stepdown=1)
)



cam_top.save_gcode('cam_top.nc')
cam_side.save_gcode('cam_side.nc')
cam_bottom.save_gcode('cam_bottom.nc')

show_object(assembly)
cam_top.show(show_object)
cam_side.show(show_object)
cam_bottom.show(show_object)
