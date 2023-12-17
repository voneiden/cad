from build123d import Box, Pos, Cylinder, Locations
from cq_viewer import show_object

result = (
    Box(50, 150, 5)
    + Pos(30, 70, 0) * Box(10, 10, 5)
    + Pos(-10, 0, 5) * Box(30, 150, 5)
    - [loc * Cylinder(3, 50) for loc in Locations((-15, 0), (-15, 50), (-15, -50))]
)


show_object(result)