import cadquery as cq
from OCP.gp import gp_Ax1
from cadquery.occ_impl import exporters

import lib.arc_calc as ac

outer_d = 30
inner_d = 25
teeth = 12
tooth_gap_ratio = 0.55
length = 50
outer_r = outer_d / 2
inner_r = inner_d / 2
result = (
    cq.Workplane()
    .moveTo(0, outer_r)
    .radiusArc((0, -outer_r), outer_r)
    .lineTo(-length, -outer_r)
    .radiusArc((-length, outer_r), outer_r)
    .close()
    .extrude(4)
    .moveTo(0, 0)
    .circle(inner_r)
    .moveTo(-length, 0)
    .cutThruAll()
    #.moveTo(0, 0)
    .faces('>Z')
    .workplane()
)

outer_tooth_r = outer_r + 50
def generate_tooth(wp: cq.Workplane) -> cq.Workplane:
    tooth_segment_angle = 360 / teeth
    tooth_segments = [i * tooth_segment_angle for i in range(12)]

    tooth_angle = tooth_segment_angle * tooth_gap_ratio
    gap_angle = tooth_segment_angle - tooth_angle
    half_tooth_angle = tooth_angle / 2

    unit_v = (0, 1)
    unit_v = ac.arc(unit_v, -half_tooth_angle)[1]
    for i in range(12):
        op1 = ac.mul(unit_v, outer_tooth_r)
        ip1 = ac.mul(unit_v, inner_r)
        unit_v = ac.arc(unit_v, tooth_angle)[1]
        op2 = ac.mul(unit_v, outer_tooth_r)
        ip2 = ac.mul(unit_v, inner_r)

        wp = (
            wp.moveTo(*op1)
            .radiusArc(op2, outer_tooth_r)
            .lineTo(*ip2)
            .radiusArc(ip1, -inner_r)
            .close()
            .cutBlind(-2)
        )
        unit_v = ac.arc(unit_v, gap_angle)[1]


    return wp


result = generate_tooth(result)

exporters.export(result, 'suntour.stl')