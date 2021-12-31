import cadquery as cq

from lib import cqlib

cqlib.setup()

result = (
    cq.Workplane()
    .rect(10, 10)
    .extrude(10)
    .faces('<Y')
    .workplane()
    .rect(5, 5)
    .extrude(3)
    
)
# result = (
#    cq.Workplane()
#    .rounded_rect(10, 10, 1)
#    .extrude(2)
#    .edges('>Z')
#    .fillet(1)
# )
