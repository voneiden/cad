import cadquery as cq

from lib import cqlib

cqlib.setup(locals())

# Alpha cutout is 10x10 mm
# Alpha spacing is 14.25 x 14.20 mm (width / height)

# Num cutout diameter is 10 mm



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
