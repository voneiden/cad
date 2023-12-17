from ocp_freecad_cam import Job, Endmill
from ocp_freecad_cam.api import Tab
from projects.a320.jayel.jayel import double_cap
import cadquery as cq
frm = double_cap(20, 20)

top = frm.faces(">Z")
pocket_faces = []
for face in frm.faces(">Z[1]").objects:
    pocket_faces.append(
        cq.Face.makeFromWires(face.outerWire(), face.innerWires()[0].offset2D(-0.1))
    )



tool = Endmill(diameter=1, h_feed=500, v_feed=200)
job = (
    Job(top, frm, "grbl", clearance_height_offset=1)
    .pocket(pocket_faces, tool, pattern="offset")
    .profile(frm.faces("<Z"), tool, perimeter=False, holes=True)
    .profile(frm.faces("<Z"), tool, dressups=[Tab()]) # TODO tabs
)

show_object(frm, "Frame", options={"color": "purple"})
job.show(show_object)
with open('double_cap.nc', 'w') as f:
    f.write(job.to_gcode())