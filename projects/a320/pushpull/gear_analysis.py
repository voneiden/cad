import cadquery as cq
from cq_gears import SpurGear

spur_gear1 = SpurGear(module=1.026, teeth_number=26, width=3, bore_d=9.8)
spur_gear2 = SpurGear(module=1.026, teeth_number=13, width=3, bore_d=5.8)
print("D", spur_gear1.r0 + spur_gear2.r0)

result = (
    cq.Workplane()
    .gear(spur_gear1)
    .center(spur_gear1.r0 + spur_gear2.r0, 0)
    .addGear(spur_gear2)
)
