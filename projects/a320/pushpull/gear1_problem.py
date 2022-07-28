import cadquery as cq
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from cq_gears import SpurGear

from cq_cam import JobV2, EdgeTabs, WireTabs
from cq_cam.operations import profile

spur_gear1 = SpurGear(module=1.026, teeth_number=26, width=3, bore_d=9.8)


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
    .profile(result.faces('<Z'), outer_offset=1, stepdown=1,
             tabs=WireTabs(count=4, width=1, height=1))
)

show_object(result)
cam.show(show_object)
show_object(profile.TAB_ERRORS, 'tab-errors')
show_object(profile.OG_WIRE, 'og-edges')
wire_builder = BRepBuilderAPI_MakeWire()

for e in profile.TAB_ERRORS:
    wire_builder.Add(e.wrapped)
    if not wire_builder.IsDone():
        show_object(e, 'failededge')
        break