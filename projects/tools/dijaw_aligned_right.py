from build123d import Box, Pos, Cylinder, Locations, Axis, Face
from cq_viewer import show_object
import ocp_freecad_cam as cam
# 17 from the hole edge to the edge of lower, so 20
# lower width is 20
# 10 to the outer edge
# wanna slide 50
# 50 + 10 + 20 + 20 = 100
result = (
        Box(100, 100, 5)
        + Pos(5, 0, 5) * Box(90, 100, 5)
        - [
            loc * Cylinder(3, 50) for loc in Locations((-20, 25),
                                                       (-20, -25),
                                                       (30, 25),
                                                       (30, -25),
                                                       )
        ]
        - [
            loc * Box(50, 6, 50) for loc in Locations((5, 25),
                                                      (5, -25))
        ]
)




tool = cam.Endmill(diameter=3.175)
faces = (result.faces() | Axis.Z).group_by(Axis.Z)
wires = faces[-3].wires()

job = (
    cam.Job(faces[-1][0], result, post_processor="grbl")
    .pocket(faces[-2], tool=tool, pattern="offset")
    .pocket([Face.make_from_wires(w) for w in wires[1:]], tool=tool, pattern="offset")
    .profile(wires[0], tool=tool)
)

show_object(result)
#show_object(wires[1:])
job.show(show_object)