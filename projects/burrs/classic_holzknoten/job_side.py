from ocp_freecad_cam.api import Ramp
from projects.burrs.classic_holzknoten.classic_holzknoten import pieces
from projects.burrs.classic_holzknoten.bench import spacing, burr_width, burr_height
from cq_viewer import show_object
import build123d as b
import ocp_freecad_cam as cam
from ocp_freecad_cam.api_util import Expression


def create_blank():
    return b.Part(children=[b.Vertex()])


def rotate_part(piece):
    # return piece
    piece.orientation = (90, 0, 0)
    piece.position += (0, 9, 0)
    return piece


pieces: list[b.Part] = [piece[1] for piece in pieces]
pieces = [pieces[0], pieces[3], pieces[4]]
locs = b.GridLocations(burr_width + spacing, burr_height + spacing, 2, 3)
locs = list(locs)
locs = [locs[0], locs[3], locs[4]]
print(burr_width)
pieces = [rotate_part(piece.located(loc)) for piece, loc in zip(pieces, locs)]
print(pieces)
compound = b.Compound(children=pieces)
show_object(compound)


top = compound.faces().group_by(b.Axis.Z)[-1][0]
# show_object(top[-1])
tool = cam.Endmill(diameter=3.175, h_feed=800, v_feed=600)
pockets = compound.faces().filter_by(b.Axis.Z).group_by(b.Axis.Z)[-2]
# show_object(pockets)
job = cam.Job(top, compound, "grbl").pocket(
    pockets,
    tool,
    step_down=-2,
    step_over=50,
    pattern="zigzag_offset",
    extra_offset=-0.05,
)

job.show(show_object)
with open("projects/burrs/classic_holzknoten/nc/02_job_side.nc", "w") as f:
    f.write(job.to_gcode())


# job.save_fcstd()
# print(burr_width)
# piece = piece.located([loc for loc in locs][2])
# piece.orientation = (90, 0, 0)
# piece.position += (0, 9, 0)
