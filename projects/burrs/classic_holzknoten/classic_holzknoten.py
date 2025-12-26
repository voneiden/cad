import os

import ocp_freecad_cam as cam
from build123d import Axis

from projects.burrs.base import burr_piece
from cq_viewer import show_object

piece1 = burr_piece(
    9,
    [
        [
            [1, 1],
            [1, 1],
            [1, 0],
            [1, 0],
            [1, 1],
            [1, 1],
        ],
        [
            [1, 1],
            [0, 0],
            [1, 0],
            [0, 0],
            [0, 0],
            [1, 1],
        ],
    ],
)


piece2 = burr_piece(
    9,
    [
        [
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
        ],
        [
            [1, 1],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [1, 1],
        ],
    ],
)

piece3 = burr_piece(
    9,
    [
        [
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
        ],
        [
            [1, 1],
            [0, 0],
            [0, 0],
            [0, 0],
            [1, 1],
            [1, 1],
        ],
    ],
)
piece4 = burr_piece(
    9,
    [
        [
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 0],
            [1, 1],
            [1, 1],
        ],
        [
            [1, 1],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [1, 1],
        ],
    ],
)

piece5 = burr_piece(
    9,
    [
        [
            [1, 1],
            [1, 1],
            [1, 0],
            [1, 0],
            [1, 1],
            [1, 1],
        ],
        [
            [1, 1],
            [1, 0],
            [0, 0],
            [0, 0],
            [1, 0],
            [1, 1],
        ],
    ],
)

piece6 = burr_piece(
    9,
    [
        [
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
        ],
        [
            [1, 1],
            [0, 0],
            [1, 0],
            [1, 0],
            [0, 0],
            [1, 1],
        ],
    ],
)


pieces = [
    ("piece1", piece1),
    ("piece2", piece2),
    ("piece3", piece3),
    ("piece4", piece4),
    ("piece5", piece5),
    ("piece6", piece6),
]


if __name__ == "__main__":
    show_object(piece3)
    ##
    print(piece1)
