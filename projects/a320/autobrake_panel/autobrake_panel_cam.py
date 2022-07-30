import cadquery as cq
from cq_cam import JobV2, EdgeTabs, ContourStrategy
from cq_cam.operations import pocket
from cq_cam.utils.utils import wire_to_ordered_edges, edge_start_point

panel = cq.importers.importStep('autobrake_panel.step')

job_wp = panel.faces('>Z').workplane()
profile_face = panel.faces('<Z')

cam = (
    JobV2(
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
cam.save_gcode('autobrake_panel_profile.nc')

engrave_faces = panel.faces('>Z[-2]')
i= 1
engrave = (
    JobV2(
        top=job_wp.plane,
        feed=300,
        tool_diameter=0.1,
        rapid_height=1.0,
        op_safe_height=0.5,
    )
    .pocket(
        #[engrave_faces.objects[28]],
        engrave_faces.objects,
    )
)
engrave.save_gcode('autobrake_panel_engrave.nc')

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
