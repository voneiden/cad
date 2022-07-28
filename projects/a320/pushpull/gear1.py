import cadquery as cq
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from cq_gears import SpurGear

from cq_cam import JobV2, EdgeTabs, WireTabs
from cq_cam.operations import profile

spur_gear1 = SpurGear(module=1, teeth_number=16, width=4, bore_d=9.8)


result = (
    cq.Workplane().gear(spur_gear1)
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

cam.save_gcode('gear1.nc')
show_object(result)
cam.show(show_object)

