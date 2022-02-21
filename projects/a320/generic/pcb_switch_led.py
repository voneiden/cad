import cadquery as cq

from lib import cqlib

cqlib.setup(locals())

# Base 6x6x5 mm
# Switch lower 4.5x4.5x2mm
# Switch upper 6x4.5x0.5
# LED diameter 3 mm

pcb_switch_led = (
    cq.Workplane()
    .rect(6, 6)
    .extrude(5)
    .faces('>Z')
    .workplane()
    .rect(4.5, 4.5)
    .extrude(2)
    .faces('>Z')
    .workplane()
    .rect(4.5, 6)
    .extrude(0.5)
    .faces('>Z')
    .tag('top')
    .end()
)