import cadquery as cq

from lib import cqlib

cqlib.setup(locals())

mill_radius = 3.175 / 2

# Panel outline
width = 117
right_height = 135
left_height = 95
right_width = 39
big_arc = 7.5
small_arc = 2

side_arc_width_single = big_arc + small_arc * 2
side_arc_width_double = side_arc_width_single * 2

panel = (
    cq.Workplane()
    .moveTo(-width/2, right_height/2)
    .move(big_arc + small_arc*2, 0)
    .line(width - side_arc_width_double, 0)
    .ellipseArc(small_arc, small_arc, 0, 90, 0, -1)
    .ellipseArc(big_arc, big_arc, 0, 90, 180, 1)
    .ellipseArc(small_arc, small_arc, 0, 90, 0, -1)
    .line(0, -right_height + side_arc_width_double)
    .ellipseArc(small_arc, small_arc, 0, 90, 270, -1)
    .ellipseArc(big_arc, big_arc, 0, 90, 90, 1)
    .ellipseArc(small_arc, small_arc, 0, 90, 270, -1)
    .line(-right_width + side_arc_width_single + big_arc, 0)
    .ellipseArc(big_arc, big_arc, 0, 90, 180, -1)
    .line(0, right_height - left_height - big_arc*2)
    .ellipseArc(big_arc, big_arc, 0, 90, 0, 1)
    .line(-width+right_width +
          side_arc_width_single + big_arc, 0)
    .ellipseArc(small_arc, small_arc, 0, 90, 180, -1)
    .ellipseArc(big_arc, big_arc, 0, 90, 0, 1)
    .ellipseArc(small_arc, small_arc, 0, 90, 180, -1)
    .line(0, left_height - side_arc_width_double)
    .ellipseArc(small_arc, small_arc, 0, 90, 90, -1)
    .ellipseArc(big_arc, big_arc, 0, 90, 270, 1)
    .ellipseArc(small_arc, small_arc, 0, 90, 90, -1)
    .close()
)

# Screw holes
screw_distance_from_side = 7
screw_outer_diameter = 7
screw_inner_diameter = 4  # TODO
screw_positions = [
    (0, right_height/2 - screw_distance_from_side),
    (-width / 2 + side_arc_width_single + screw_distance_from_side,
     -right_height/2 + (right_height - left_height) + screw_distance_from_side),
    (width/2 - right_width + screw_distance_from_side,
     -right_height / 2 + screw_distance_from_side)
]

screw = (
    panel
    .pushPoints(screw_positions)
    .circle(screw_inner_diameter/2)
)


# Landing gear cutout
ldg_gear_height = 20
ldg_gear_width = 60
ldg_gear_top_margin = 14
ldg_gear = (
    screw
    .moveTo(-width / 2 + 13 + ldg_gear_width / 2,
            right_height/2 - ldg_gear_top_margin - ldg_gear_height / 2)
    .rounded_rect(ldg_gear_width, ldg_gear_height, mill_radius)
)

# Brake fan
brake_fan_width = 20
brake_fan_height = 20
brake_fan = (
    ldg_gear
    .moveTo(width / 2 - 10 - brake_fan_width / 2, right_height/2 - 14 - ldg_gear_height / 2)
    .rounded_rect(20, 20, mill_radius)
)

# Auto brake
ab_left_width = 40
ab_right_width = 20
ab_height = 20
ab_spacing = 7
ab_left_margin = 9
ab_top_margin = ldg_gear_top_margin + ldg_gear_height + 20
autobrake = (
    brake_fan
    .moveTo(-width / 2 + ab_left_margin + ab_left_width / 2,
            right_height / 2 - ab_top_margin - ldg_gear_height / 2)
    .rounded_rect(ab_left_width, ab_height, mill_radius)
    .moveTo(-width / 2 + ab_left_margin + ab_left_width + ab_spacing + ab_right_width / 2,
            right_height / 2 - ab_top_margin - ldg_gear_height / 2)
    .rounded_rect(ab_right_width, ab_height, mill_radius)
)

# Anti skid
askid_right_margin = 20
askid_inner_radius = 5 # TODO
askid_outer_radius = 10
askid_point = (width / 2 - askid_right_margin,
               right_height / 2 - ab_top_margin - ldg_gear_height / 2)
askid = (
    autobrake
    .moveTo(*askid_point)
    .circle(askid_inner_radius)
)


# Terr on ND
terr_bottom_margin = 11
terr_right_margin = 9
terr_width = 20
terr_height = 20
terr = (
    askid
    .moveTo(width/2 - terr_right_margin - terr_width / 2,
            -right_height/2 + terr_bottom_margin + terr_height / 2)
    .rounded_rect(terr_width, terr_height, mill_radius)
)

panel_base = terr.extrude(3)

# Countersinks
panel_cs = (
    panel_base.faces('>Z').workplane()
    .pushPoints(screw_positions)
    .circle(screw_outer_diameter/2)
    .cutBlind(-1)
    .moveTo(*askid_point)
    .circle(askid_outer_radius)
    .cutBlind(-1)
)

# Text engravings
panel_engravings = (
    panel_cs
        .moveTo(0, 28)
        .rect(110, 1)
        .moveTo(0, -9)
        .rect(110, 1)
        .moveTo(20, 45)
        .rect(1, 25)
        .moveTo(20, 10)
        .rect(1, 30)
        .cutBlind(-0.1)

)

panel_engravings = (
    panel_engravings
    .center(-16, 57)
    .panel_text('LDG GEAR', fontsize=5, distance=-0.1)
    .center(53, 0)
    .panel_text('BRK FAN', fontsize=5, distance=-0.1)
    .center(-53, -35)
    .panel_text('AUTO BRK', fontsize=5, distance=-0.1)
    .center(-24, -5)
    .panel_text('LOW', fontsize=4, distance=-0.1)
    .center(20, 0)
    .panel_text('MED', fontsize=4, distance=-0.1)
    .center(20 + ab_spacing, 0)
    .panel_text('MAX', fontsize=4, distance=-0.1)
    .center(31, 0)
    .panel_text('N/W STRG', fontsize=5, distance=-0.1)
    .center(0, 5)
    .panel_text('A/SKID &', fontsize=5, distance=-0.1)
    .center(13, -10)
    .panel_text('ON', fontsize=4, distance=-0.1)
    .center(0, -17)
    .panel_text('OFF', fontsize=4, distance=-0.1)
    .center(-13, -28)
    .panel_text('TERR ON ND', fontsize=5, distance=-0.1)
)


show_object(panel_engravings, 'result')
















