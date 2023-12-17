from ocp_freecad_cam import Job, Endmill
from projects.a320.jayel.jayel import lightplate

frm = lightplate(20, 20)

top = frm.faces("<Z")

tool = Endmill(diameter=1)
job = (
    Job(top, frm, "grbl")
    .profile(frm.faces("<Z"), tool)
    #.profile(frm.faces(">Z"), tool)
)

show_object(frm, "Frame", options={"color": "purple"})
job.show(show_object)
with open('double_cap.nc', 'w') as f:
    f.write(job.to_gcode())