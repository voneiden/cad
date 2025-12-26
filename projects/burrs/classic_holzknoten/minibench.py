import build123d as b
from cq_viewer import show_object
import ocp_freecad_cam as cam
from ocp_freecad_cam.api import Ramp
import pathlib
from ocp_freecad_cam.api import Dogbone
# Burr is 72x18x18
# 10 mm separation
# 2x3
# 3*10+2*72

burr_size = 9
outer_width_spacing = 10
outer_height_spacing = 25
spacing = 10
burr_width = burr_size * 6
burr_height = burr_size * 2
bench_height = 18

tightness = 0.1

if __name__ == "__cq_viewer__":
    calibration_hole = None
    with b.BuildPart() as bench:
        b.Box(
            burr_width + outer_width_spacing * 2,
            burr_height + outer_height_spacing * 2,
            bench_height,
        )

        with b.BuildSketch(bench.faces().sort_by(b.Axis.Z)[-1]):
            with b.Locations((0, 20)):
                b.Circle(3.175 / 2)
        b.extrude(amount=-10, mode=b.Mode.SUBTRACT)
        calibration_hole = (
            bench.faces(b.Select.LAST).filter_by(b.Axis.Z).sort_by(b.Axis.Z)[0]
        )

        with b.BuildSketch(bench.faces().sort_by(b.Axis.Z)[-1]):
            b.Rectangle(burr_width - tightness, burr_height - tightness)
            b.Rectangle(burr_width + 15, 7.5)
            b.Rectangle(7.5, burr_height + 15)
        b.extrude(amount=-burr_height / 2, mode=b.Mode.SUBTRACT)
        pocket_faces = bench.faces().filter_by(b.Axis.Z).group_by(b.Axis.Z)[-2]

        with b.BuildSketch(bench.faces().sort_by(b.Axis.Z)[-1]):
            with b.GridLocations(50, 50, 2, 2):
                b.Circle(3)
        b.extrude(amount=-bench_height, mode=b.Mode.SUBTRACT)
        mount_holes = b.edges(b.Select.LAST).group_by(b.Axis.Z)[0]

        with b.BuildSketch(bench.faces().filter_by(b.Axis.Z).group_by(b.Axis.Z)[-1]):
            with b.GridLocations(burr_width / 3, 0, 3, 1):
                b.Circle(5)
        b.extrude(amount=-bench_height, mode=b.Mode.SUBTRACT)
        poke_holes = b.edges(b.Select.LAST).group_by(b.Axis.Z)[0]

    # show_object(bench)
    # show_object(pocket_faces.wires()[0])
    # show_object(pocket_faces)
    # print(bench)
    bench = bench.part

    tool = cam.Endmill(diameter=3.175, h_feed=1000, v_feed=500)
    top = bench.faces().sort_by(b.Axis.Z)[-1]

    bottom = bench.faces().sort_by(b.Axis.Z)[0]

    job = (
        cam.Job(top, bench, post_processor="grbl")
        .helix(mount_holes, tool)
        .drill(calibration_hole, tool)
        # .adaptive(pocket_faces, tool, step_down=2, step_over=75)
        .pocket(
            pocket_faces,
            tool,
            step_down=-2,
            step_over=75,
            pattern="zigzag",
            # dressups=[Dogbone()],
            # keep_tool_down=True,
            # min_travel=True,
        )
        .profile(pocket_faces, tool, dressups=[Dogbone()], side="in")
        .helix(poke_holes, tool, start_depth=-burr_size + 0.5, start_side="in")
        .profile(
            bottom,
            tool,
            dressups=[Ramp()],
        )
    )
    job.show(show_object)
    with open("projects/burrs/classic_holzknoten/nc/minibench.nc", "w") as f:
        f.write(job.to_gcode())

    job.save_fcstd()
    # show_object(poke_holes)
