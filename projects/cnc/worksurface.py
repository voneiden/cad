import build123d as b
from cq_viewer import show_object, setup

table_size = 350
table_height = 13
pentagon_side_to_circle_radius = 0.8506508084
pentagon_side = 153
circle_radius = pentagon_side * pentagon_side_to_circle_radius

motor_width = 70
motor_length = 100

clamp_spacing = 50
clamp_radius = 5  # TODO: check
clamp_sink_radius = 7  # TODO: check

attachment_radius = 3
attachment_sink_depth = 3  # TODO: check
attachment_sink_radius = 5.5
# Original would be 270, but this aligns very poorly on top of the rails
# in two positions. This is unpleasant, so if remaking the table consider other
# something else
# attachment_count 7/270 seems kinda OK, but possibly gets too close to upper
# slider mounts.
attachment_count = 6
attachment_start_angle = 240


with b.BuildPart() as upper_table:
    b.Box(table_size, table_size, table_height)

    top = upper_table.faces().sort_by(sort_by=b.Axis.Z)[-1]
    bottom = upper_table.faces().sort_by(sort_by=b.Axis.Z)[0]

    # Attachment holes
    with b.BuildSketch(bottom):
        with b.PolarLocations(circle_radius, attachment_count, attachment_start_angle):
            b.Circle(attachment_radius)
        with b.Locations([(0, clamp_spacing / 2), (0, -clamp_spacing / 2)]):
            b.Circle(attachment_radius)

    # Clamp holes
    with b.BuildSketch(bottom) as clamp_sketch:
        with b.GridLocations(
            clamp_spacing,
            clamp_spacing,
            int(table_size / clamp_spacing),
            int(table_size / clamp_spacing),
        ):
            b.Circle(clamp_radius)

    b.extrude(
        amount=-table_height,
        mode=b.Mode.SUBTRACT,
    )

    # Attachment sinks
    with b.BuildSketch(bottom.offset(-table_height)):
        with b.PolarLocations(circle_radius, attachment_count, attachment_start_angle):
            b.RegularPolygon(attachment_sink_radius, 6)
        with b.Locations([(0, clamp_spacing / 2), (0, -clamp_spacing / 2)]):
            b.RegularPolygon(attachment_sink_radius, 6)
    b.extrude(amount=attachment_sink_depth, mode=b.Mode.SUBTRACT)

    # Clamp sinks
    with b.BuildSketch(bottom) as clamp_sink_sketch:
        with b.GridLocations(50, 50, int(table_size / 50), int(table_size / 50)):
            b.Circle(clamp_sink_radius)

    b.extrude(amount=-1, mode=b.Mode.SUBTRACT)

    # Motor mount cutout
    with b.BuildSketch(bottom):
        with b.Locations([(0, table_size / 2 - motor_length / 2)]):
            b.Rectangle(motor_width, motor_length)
    b.extrude(amount=-5, mode=b.Mode.SUBTRACT)

    # Rebuild from the other side and fill the unneeded holes..
    with b.BuildSketch(top):
        with b.Locations([(0, -table_size / 2 + motor_length / 2)]):
            b.Rectangle(motor_width, motor_length)
    b.extrude(amount=-table_height + 5)

    upper_table_bottom_location = b.Location(bottom.center(b.CenterOf.BOUNDING_BOX))
    print("FOO", upper_table_bottom_location)
    b.RigidJoint("upper_bottom", joint_location=upper_table_bottom_location)

with b.BuildPart() as lower_table:
    b.Box(table_size, table_size, table_height)

    bottom = lower_table.faces().sort_by(sort_by=b.Axis.Z)[0]

    # Attachment holes
    with b.BuildSketch(bottom):
        with b.PolarLocations(circle_radius, attachment_count, attachment_start_angle):
            b.Circle(3)
        with b.Locations([(0, clamp_spacing / 2), (0, -clamp_spacing / 2)]):
            b.Circle(attachment_radius)

    # Motor cutout
    with b.BuildSketch(bottom):
        with b.Locations([(0, table_size / 2 - motor_length / 2)]):
            b.Rectangle(motor_width, motor_length)

    # Rail mounts
    with b.BuildSketch(bottom):
        with b.GridLocations(150, 150, 2, 2):
            with b.GridLocations(30, 30, 2, 2):
                b.Circle(3)
    b.extrude(
        amount=-table_height,
        mode=b.Mode.SUBTRACT,
    )

    lower_table_top_location = b.Location(
        lower_table.faces().sort_by(b.Axis.Z)[-1].center(b.CenterOf.BOUNDING_BOX)
    )
    b.RigidJoint(
        "lower_top", to_part=lower_table, joint_location=lower_table_top_location
    )

# setup(projection="perspective")
# setup(projection="orthographic")
print(lower_table.part.joints)
print(upper_table.part.joints)
lower_table.part.joints["lower_top"].connect_to(upper_table.part.joints["upper_bottom"])
show_object(lower_table, transparency=0)
show_object(upper_table, transparency=0)
