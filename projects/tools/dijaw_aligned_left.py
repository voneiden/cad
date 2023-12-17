from build123d import Box, Pos, Cylinder, Locations
from cq_viewer import show_object

result = (
    Box(50, 100, 5)
    + Pos(30, 45, 0) * Box(10, 10, 5)
    + Pos(-10, 0, 5) * Box(30, 100, 5)
    - [loc * Cylinder(3, 50) for loc in Locations((-15, -25), (-15, 25))]
)


show_object(result)