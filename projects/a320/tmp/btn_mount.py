import cadquery as cq

from lib import cqlib

cqlib.setup(locals())
# 6x4.5
inner = (4.5, 6)
dimensions = (10, 10)

btn_mount = (
    cq.Workplane()
    .rect(*dimensions)
    .extrude(3)
    .faces('<Z')
    .workplane()
    .rect(*inner)
    .cutBlind(-0.5)
    .faces('<Z[1]')
    .tag('mount_bottom')
    .end()
)