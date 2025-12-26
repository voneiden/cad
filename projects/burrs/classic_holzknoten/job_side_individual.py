from ocp_freecad_cam.api import Ramp
from projects.burrs.classic_holzknoten.classic_holzknoten import pieces
from projects.burrs.classic_holzknoten.bench import spacing, burr_width, burr_height
from cq_viewer import show_object
import build123d as b
import ocp_freecad_cam as cam
from ocp_freecad_cam.api_util import Expression
import copy

extra_internal_space = 0.05


def create_blank():
    return b.Part(children=[b.Vertex()])


def rotate_part(piece):
    # return piece
    piece = copy.deepcopy(piece)
    piece.orientation = (90, 0, 0)
    piece.position += (0, 9, 0)
    return piece


pieces: list[b.Part] = [piece[1] for piece in pieces]
pieces = [pieces[0], pieces[3], pieces[4]]
# pieces = [rotate_part(piece) for piece in pieces]
# locs = b.GridLocations(burr_width + spacing, burr_height + spacing, 2, 3)
# locs = list(locs)
# locs = [locs[0], locs[3], locs[4]]
# print(burr_width)
# pieces = [rotate_part(piece.located(loc)) for piece, loc in zip(pieces, locs)]
# print(pieces)

for i, piece in enumerate(pieces):
    top = piece.faces().group_by(b.Axis.Y)[-1]
    top_center = b.Compound(top).center(b.CenterOf.BOUNDING_BOX)
    top_plane = b.Plane(top_center, (1, 0, 0), (0, 1, 0))
    tool = cam.Endmill(diameter=3.175, h_feed=800, v_feed=600)
    pockets = piece.faces().filter_by(b.Axis.Y).group_by(b.Axis.Y)[-2]
    pockets = b.offset(pockets, 3.175 / 2) - piece + pockets
    pockets = b.offset(pockets, extra_internal_space).faces()
    job = cam.Job(top_plane, piece, "grbl")

    for pocket in pockets:
        pocket.position += (0, 0, -extra_internal_space)
        job = job.profile(pocket, tool, step_down=10, side="in")

    if i == 2:
        show_object(top)
        show_object(b.Vertex(top_center))
        show_object(pockets)
        # show_object(piece)
        job.show(show_object)
        job.save_fcstd()
    with open(f"projects/burrs/classic_holzknoten/nc/02_job_side__{i}.nc", "w") as f:
        f.write(job.to_gcode())

# print(burr_width)
# piece = piece.located([loc for loc in locs][2])
# piece.orientation = (90, 0, 0)
# piece.position += (0, 9, 0)
