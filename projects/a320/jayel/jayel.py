import cadquery as cq
from cadquery.selectors import NearestToPointSelector


from lib import cqlib
from lib.cqlib import CustomWorkplaneMixin

cqlib.setup(locals())


class Workplane(CustomWorkplaneMixin, cq.Workplane):
    pass


def frame(width, height, thickness=2, ledge=1, depth=5, tool_radius=0.5):
    half_thickness = thickness / 2
    half_ledge = ledge / 2
    return (
        Workplane()
        .rounded_rect(width, height, tool_radius)
        .rounded_rect(width + thickness + ledge, height + thickness + ledge, tool_radius)
        .extrude(-1)
        .faces('<Z')
        .workplane()
        .rounded_rect(width, height, tool_radius)
        .rounded_rect(width + thickness, height + thickness, 1.5875)
        .extrude(depth)
        .faces('>Z')
        .tag('Zp')
        .end()
        .faces('>Z[1]')
        .tag('Zm')
        .end()
    )


def double_cap(width, height, depth=5, upper_depth=1.5, thickness=1, ledge=1, tool_radius=0.5):
    y_center = height / 4 - thickness / 4
    half_width = width / 2
    half_height = height / 2
    upper_width = width - 2 * thickness
    upper_height = half_height - 2.5 * thickness + thickness
    lower_width = width - 2 * (thickness + ledge)
    lower_height = half_height - 2 * (thickness + ledge) + thickness / 2

    return (
        Workplane()
        .rounded_rect(width, height, tool_radius)
        .extrude(depth)
        .faces('>Z')
        .workplane()
        .pushPoints([(0, y_center), (0, -y_center)])
        .rounded_rect(upper_width, upper_height, tool_radius)
        .cutBlind(-upper_depth)
        .faces('>Z')
        .workplane()
        .pushPoints([(0, y_center), (0, -y_center)])
        .rounded_rect(lower_width, lower_height, tool_radius)
        .cutBlind(-depth)
        .faces('>Z')
        .tag('Zp')
        .end()
        .faces(NearestToPointSelector((0, y_center, upper_depth)))
        .tag('Zpu')
        .end()
        .faces(NearestToPointSelector((0, -y_center, upper_depth)))
        .tag('Zpl')
        .end()
    )


def lightplate(width, height, depth=1.5, thickness=1, tool_radius=.5):
    plate_width = width - 2 * thickness
    plate_height = height / 2 - 2.5 * thickness + thickness
    return (
        Workplane()
        .rounded_rect(plate_width, plate_height, tool_radius)
        .extrude(depth)
        .faces('<Z')
        .tag('Zn')
        .end()
    )




