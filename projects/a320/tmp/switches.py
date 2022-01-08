import cadquery as cq

from lib import cqlib

cqlib.setup(locals())




tactile_led = (
    cq.Workplane()
    .rect(6, 6)
    .extrude(5)
    .faces('<Z')
    .tag('mount_bottom')
    .end()
    .faces('>Z')
    .workplane()
    .rect(4.5, 4.5)
    .extrude(2)
    .faces('>Z')
    .workplane()
    .rect(4.5, 6)
    .extrude(0.5)
    .faces('>Z')
    .tag('mount_top')
    .workplane()
    .circle(1.5)
    .extrude(2)
)


