#from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
#set_port(3939)
import time

import cadquery as cq

from cq_cam import Job
from cq_cam.operations.tabs import EdgeTabs

panel = cq.importers.importStep('autobrake_panel.step')

job_wp = panel.faces('>Z').workplane()
profile_face = panel.faces('<Z')

t1 = time.time()
cam = (
    Job(
        top=job_wp.plane,
        feed=300,
        tool_diameter=3.175
    )
    .profile(
        profile_face,
        inner_offset=-1,
        stepdown=1.5
    )
    .profile(
        profile_face,
        outer_offset=1,
        stepdown=1.5,
        tabs=EdgeTabs(spacing=35, width=5, height=1.5, only='LINE')
    )
)
t2 = time.time()
cam.save_gcode('autobrake_panel_profile.nc')
t3 = time.time()
engrave_faces = panel.faces('>Z[-2]')
i= 1
engrave = (
    Job(
        top=job_wp.plane,
        feed=300,
        tool_diameter=0.5,
        rapid_height=1.0,
        op_safe_height=0.5,
    )
    .pocket(
        #[engrave_faces.objects[28]],
        engrave_faces.objects,
        stepover=0.8,
    )
)
t4 = time.time()
engrave.save_gcode('autobrake_panel_engrave.nc')
t5 = time.time()
print(f"Job took: {t2-t1}s")
print(f"Export took: {t3-t2}s")
print(f"Engrave job took: {t4-t4}s")
print(f"Engrave export took: {t5-t4}s")
print(f"Total took: {t5-t1}s")
# Benchmark 1.0865793228149414
show_object(panel, 'panel')
#show_object(engrave_faces.objects[i], 'faces')
cam.show(show_object)
engrave.show(show_object)
#for j,obj in enumerate(pocket.DEBUG):
    #if isinstance(obj, cq.Wire):
    #    for k, edge in enumerate(wire_to_ordered_edges(obj)):
    #        show_object(edge, f'debug-w-{j}-e-{k}')
    #        show_object(cq.Vertex.makeVertex(*edge_start_point(edge).toTuple()), f'debug-w-{j}-e-{k}-start')

#    show_object(obj, f'debug-w-{j}')

#show_object(pocket.DEBUG[0].offset2D(-0.1, 'intersection')[0], 'test_offset')
#with open('autobrake_panel.nc', 'w') as f:
#    f.write(cam.to_gcode())
