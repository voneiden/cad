from projects.a320.jayel.jayel import frame, double_cap, lightplate
import cadquery as cq

from lib import cqlib
cqlib.setup(locals())


def assembly(width, height):
    frame_part = frame(width, height)
    double_cap_part = double_cap(width, height)
    lightplate_part = lightplate(width, height)
    return (
        cq.Assembly()
        .add(frame_part, name='frame', color=cq.Color("snow4"))
        .add(double_cap_part, name='double_cap', color=cq.Color("snow4"))
        .add(lightplate_part, name="upper_lightplate", color=cq.Color(0.9, 0.9, 0.9, 0.5))
        .add(lightplate_part, name="lower_lightplate", color=cq.Color(0.9, 0.9, 0.9, 0.5))
        .constrain("frame", "Fixed")
        .constrain("frame?Zp", "double_cap?Zp", "Plane", param=0)
        .constrain("double_cap", "FixedRotation", (0, 0, 0))
        .constrain("upper_lightplate?Zn", "double_cap?Zpu", "Plane")
        .constrain("upper_lightplate", "FixedRotation", (0, 0, 0))
        .constrain("lower_lightplate?Zn", "double_cap?Zpl", "Plane")
        .constrain("lower_lightplate", "FixedRotation", (0, 0, 0))
        .solve()
    )


wp = assembly(20, 20)
show_object(wp, "assembly", options={"parts": True})

