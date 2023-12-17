import cadquery as cq
from cq_viewer import show_object

tolerance = 0.1
rotary_enc_od = 6
rotary_enc_id = 4.5

inner_shaft_id = 6
inner_shaft_od = 8

outer_shaft_id = 8
outer_shaft_od = 10

tool_diameter = 1
rotary_enc_coupler_thickness = 4

rotary_enc_coupler = (
    cq.Workplane()
    .circle((inner_shaft_od + 5) / 2)
    .extrude(rotary_enc_coupler_thickness)
    .faces('>Z').workplane()
    .circle(inner_shaft_od / 2)
    .circle(inner_shaft_id / 2)
    .cutBlind(-rotary_enc_coupler_thickness / 2)
    .faces('>Z').workplane()
    .sketch()
    .segment((-1, -1), (1, -1), "cseg", True)
    .arc((0, 0), rotary_enc_od/2, 350, 200, "carc", True)
    .constrain("carc", "FixedPoint", None)
    .constrain("carc", "Radius", rotary_enc_od/2 + tolerance)
    .constrain("carc", "cseg", "Coincident", None)
    .constrain("cseg", "carc", "Coincident", None)
    .constrain("cseg", "Orientation", (1, 0))
    .constrain("carc", "cseg", "Distance", (0.5, 0.5, 4.5 + tolerance))
    # Actual
    .arc((0, 0), rotary_enc_od/2, 350, 200, "arc")
    .arc((-1, 0), tool_diameter/2, 180, 90, "db1")
    .arc((1, 0), tool_diameter/2, 270, 90, "db2")
    .segment((-1, -1), (1, -1), "seg")
    .constrain("arc", "FixedPoint", None)
    .constrain("arc", "Radius", rotary_enc_od/2 + tolerance)
    .constrain("db1", "Radius", tool_diameter/2)
    .constrain("db2", "Radius", tool_diameter/2)
    .constrain("db1", "cseg", "Distance", (0.5, 0, 0))
    .constrain("db2", "cseg", "Distance", (0.5, 1, 0))
    .constrain("cseg", "seg", "Distance", (0.5, 0.5, 0))
    .constrain("seg", "Orientation", (1, 0))
    .constrain("arc", "db1", "Coincident", None)
    .constrain("db1", "seg", "Coincident", None)
    .constrain("seg", "db2", "Coincident", None)
    .constrain("db2", "arc", "Coincident", None)
    .solve()
    .assemble()
    .finalize()
    .cutBlind(-rotary_enc_coupler_thickness)
)


show_object(rotary_enc_coupler)
#cq.exporters.export(rotary_enc_coupler, 'pp.stl')
