import cadquery as cq
from cq_gears import SpurGear

spur_gear2 = SpurGear(module=1.026, teeth_number=13, width=3, bore_d=5.8)


result = (
    cq.Workplane().gear(spur_gear2)
)

cq.exporters.export(result, 'gear2.stl')
