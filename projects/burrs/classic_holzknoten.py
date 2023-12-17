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
        ]
    ]
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
            [1, 1],
            [0, 0],
            [0, 0],
            [0, 0],
            [1, 1],
        ]
    ]
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
            [0, 0],
            [1, 1],
        ]
    ]
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
        ]
    ]
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
        ]
    ]
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
        ]
    ]
)


standard_pieces = [
    ("piece1", piece1),
    ("piece2", piece2),
    ("piece3", piece3),
    ("piece4", piece4),
    ("piece5", piece5),
    ("piece6", piece6)
]


def save(fname, data):
    try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f"classic_holzknoten_nc/{fname}.nc"), 'w') as f:
            f.write(data)
    except NameError:
        print("Failed to save")


for i, (fname, piece) in enumerate(standard_pieces):
    tool = cam.Endmill(diameter=3.175)
    faces = (piece.faces() | Axis.Z).group_by(Axis.Z)
    job = (
        cam.Job(faces[-1][0], piece.compound(), post_processor="grbl")
        .pocket(faces[-2], tool=tool, pattern="offset")
    )
    save(fname, job.to_gcode())
    # Right: 0, 3, 4
    #if i == 0:
    #    show_object(piece)
    #    job.show(show_object)

for i, (fname, piece) in enumerate([standard_pieces[0], standard_pieces[3], standard_pieces[4]]):
    fname = fname + "_right"
    tool = cam.Endmill(diameter=3.175)
    faces = (piece.faces() | Axis.Y).group_by(Axis.Y)
    job = (
        cam.Job(faces[-1][0], piece.compound(), post_processor="grbl")
        .pocket(faces[-2], tool=tool, pattern="offset", use_outline=True)
    )
    save(fname, job.to_gcode())
    if i == 2:
        show_object(piece)
        job.show(show_object)

#faces6 = (piece6.faces6() | Axis.Z).group_by(Axis.Z)
#job6 = (
#    cam.Job(faces6[-1][0], piece6.compound(), post_processor="grbl")
#    .pocket(faces6[-2], tool=tool, pattern="offset")
#)

