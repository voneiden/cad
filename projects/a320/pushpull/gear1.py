import cadquery as cq
from cq_gears import SpurGear

spur_gear1 = SpurGear(module=1.026, teeth_number=26, width=3, bore_d=9.8)


result = (
    cq.Workplane().gear(spur_gear1)
)

cq.exporters.export(result, 'gear1.stl')
