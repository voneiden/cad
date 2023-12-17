from ocp_freecad_cam import Job, Endmill
from projects.a320.jayel.jayel import frame

frm = frame(20, 20)

top = frm.faces("<Z")

tool = Endmill(diameter=1)
job = (
    Job(top, frm, "grbl")
    .profile(frm.faces(">Z[1]").objects[0].innerWires()[0], tool)
    .profile(frm.faces(">Z"), tool)
)

show_object(frm, "Frame", options={"color": "purple"})
job.show(show_object)
with open('double_cap.nc', 'w') as f:
    f.write(job.to_gcode())