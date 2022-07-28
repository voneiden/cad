import cadquery as cq
from cq_gears import SpurGear

from cq_cam import JobV2

spur_gear2 = SpurGear(module=1, teeth_number=24, width=4, bore_d=5.9)


result = (
    cq.Workplane().gear(spur_gear2)
)

cam = (
    JobV2(
        top=result.faces('>Z').workplane().plane,
        feed=300,
        tool_diameter=1.0,
        plunge_feed=100)
    .profile(result.faces('<Z'), inner_offset=-1, stepdown=1)
    .profile(result.faces('<Z'), outer_offset=1, stepdown=1)
)

cam.save_gcode('gear2.nc')
show_object(result)
cam.show(show_object)


