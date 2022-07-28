import cadquery as cq
from cq_gears import SpurGear
module = 1
# Big moves 40 degs when other moves 60
spur_gear1 = SpurGear(module=module, teeth_number=24, width=3, bore_d=5.9)
spur_gear2 = SpurGear(module=module, teeth_number=16, width=3, bore_d=9.8)
print("D", spur_gear1.r0 + spur_gear2.r0)

result = (
    cq.Workplane()
    .gear(spur_gear1)
    .center(spur_gear1.r0 + spur_gear2.r0, 0)
    .addGear(spur_gear2)
)
