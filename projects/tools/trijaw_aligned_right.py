from build123d import Box, Pos, Cylinder, Locations
from cq_viewer import show_object

# 17 from the hole edge to the edge of lower, so 20
# lower width is 20
# 10 to the outer edge
# wanna slide 50
# 50 + 10 + 20 + 20 = 100
result = (
        Box(100, 150, 5)
        + Pos(5, 0, 5) * Box(90, 150, 5)
        - [
            loc * Cylinder(3, 50) for loc in Locations((-20, 0),
                                                       (-20, 50),
                                                       (-20, -50),
                                                       (30, 0),
                                                       (30, 50),
                                                       (30, -50),
                                                       )
        ]
        - [
            loc * Box(50, 6, 50) for loc in Locations((5, 0),
                                                      (5, 50),
                                                      (5, -50))
        ]
)

show_object(result)
