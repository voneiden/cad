import cadquery as cq

from lib import cqlib
from projects.a320.mcdu.common import bottom_cutout_outer_margin, bottom_cutout_inner_margin, cutter_radius

cqlib.setup(locals())

# Alpha cutout is 10x10 mm
# Alpha spacing is 14.25 x 14.20 mm (width / height)
# Best to leave 0.5 mm space on all sides?

cutout_margin = 0.5
size = (10 - cutout_margin * 2, 10 - cutout_margin * 2)


# TODO check safe values
leakshield_width = size[0] + 2
leakshield_height = size[1] + 2

mate = (
    cq.Workplane()
    .workplane(offset=-5)
    .rounded_rect(size[0] - bottom_cutout_outer_margin,
                  size[1] - bottom_cutout_outer_margin, cutter_radius)
    .extrude(-0.5)
    .faces('<Z')
    .workplane()
    .rect(leakshield_width, leakshield_height)
    .extrude(3.5)
    .faces('>Z')
    .rounded_rect(size[0] - bottom_cutout_inner_margin,
                  size[1] - bottom_cutout_inner_margin, cutter_radius)
    .cutBlind(2)
    .faces('<Z')
    .workplane()
    .circle(2)
    .cutThruAll()
    .faces('>Z')
    .tag('top')
    .end()
    .faces('<Z')
    #.tag('bottom')
    # TODO dogbone rect ?
    .rounded_rect(4.5 + 0.5, 6.5 + 0.5, cutter_radius)
    .cutBlind(-0.5)
    .faces('<Z[-2]')
    .tag('bottom')
    #.debug()
    .end()
)
