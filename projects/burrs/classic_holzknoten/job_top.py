from ocp_freecad_cam.api import Ramp
from projects.burrs.classic_holzknoten.classic_holzknoten import pieces
from projects.burrs.classic_holzknoten.bench import spacing, burr_width, burr_height
from cq_viewer import show_object
import build123d as b
import ocp_freecad_cam as cam
from ocp_freecad_cam.api_util import Expression

pieces: list[b.Part] = [piece[1] for piece in pieces]
locs = b.GridLocations(burr_width + spacing, burr_height + spacing, 2, 3)
print(burr_width)
pieces = [piece.located(loc) for piece, loc in zip(pieces, locs)]
print(pieces)
compound = b.Compound(children=pieces)
show_object(compound)


top = compound.faces().group_by(b.Axis.Z)[-1][0]
# show_object(top[-1])
tool = cam.Endmill(diameter=3.175, h_feed=800, v_feed=600)
pockets = compound.faces().group_by(b.Axis.Z)[-4]
job = (
    cam.Job(top, compound, "grbl")
    .pocket(
        pockets,
        tool,
        step_down=-2,
        step_over=50,
        pattern="zigzag_offset",
        extra_offset=-0.05,
    )
    .profile(compound, tool, final_depth=-burr_height, step_down=-2, dressups=[Ramp()])
)
# profile_job.show(show_object)

# show_object(pockets)
job.show(show_object)
with open("projects/burrs/classic_holzknoten/nc/01_job_top.nc", "w") as f:
    f.write(job.to_gcode())


job.save_fcstd()
