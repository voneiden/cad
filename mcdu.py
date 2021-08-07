import cadquery as cq

from lib import sub_edges, rounded_rect

cq.Workplane.sub_edges = sub_edges
cq.Workplane.rounded_rect = rounded_rect

# Dynamic params
thickness = 4

width = 141
height = 225
half_width = width / 2
half_height = height / 2

tool_radius = 1.5875  # 1/8"

previous_edges = []
previous_wires = []

# Initial 2D workpiece
result = cq.Workplane("XY").rect(width, height, True)

# Alpha keyboard sketch
alpha_x = -7.5
alpha_y = -30.5
alpha_size = (10, 10)
alpha_points = [(x * 14.25 + alpha_x, y * -14.2 + alpha_y,) for x in range(5) for y in range(6)]
result = result.pushPoints(alpha_points).rounded_rect(*alpha_size, tool_radius)

# Num keyboard sketch
num_x = -20.5
num_y = -66.5
num_radius = 5
num_dx = -14.5
num_dy = -12
num_points = [(x * num_dx + num_x, y * num_dy + num_y) for x in range(3) for y in range(4)]
result = result.pushPoints(num_points).circle(num_radius)

# FN keys
fn_x = -47.25
fn_y = -2.77
fn_dx = 17
fn_dy = -12.5
fn_size = (13.5, 10.5)
fn_points = [(x * fn_dx + fn_x, y * fn_dy + fn_y,) for x in range(6) for y in range(2)]
fn_points2 = [(x * fn_dx + fn_x, (y + 2) * fn_dy + fn_y,) for x in range(2) for y in range(3)]
result = result.pushPoints(fn_points + fn_points2).rounded_rect(*fn_size, tool_radius)

# Brightness keys
bn_x = 53.5
bn_y = -3.5
bn_dy = -12
bn_points = [(bn_x, bn_y), (bn_x, bn_y + bn_dy)]
bn_size = (8, 10)
result = result.pushPoints(bn_points).rounded_rect(*bn_size, tool_radius)

# LK/RK keys
lk_x = -64
lk_y = 85.3
lk_dx = 128
lk_dy = -10.2
lk_size = (8, 7)
lk_points = [(x * lk_dx + lk_x, y * lk_dy + lk_y,) for x in range(2) for y in range(6)]
result = result.pushPoints(lk_points).rounded_rect(*lk_size, tool_radius)
lk_edges, lk_wires = update_edges_and_wires(result)

# Mount holes
mh_x = -65.5
mh_y = [99, -4, -98]
mh_dx = 131
mh_points = [(x * mh_dx + mh_x, mh_y[y]) for x in range(2) for y in range(3)]
result = result.pushPoints(mh_points).circle(1.6)

# Indicator lights
ind_x = -32.5
ind_y = 107.5
ind_dx = 16.5
ind_size = (8, 4)
ind_points = [(x * ind_dx + ind_x, ind_y) for x in range(5)]
result = result.pushPoints(ind_points).rounded_rect(*ind_size, tool_radius)

# Big indicators
big_x = -62
big_y = -58.5
big_dx = 124
big_size = (5, 30)
big_points = [(x * big_dx + big_x, big_y) for x in range(2)]
result = result.pushPoints(big_points).rounded_rect(*big_size, tool_radius)

# Initial extrusion to 6 mm
result = result.extrude(6)

# Cut off the outer shape
old_edges = result.edges()
chunk = cq.Workplane("XY").workplane(2).rect(width, height, True).extrude(4)
chunk = chunk.faces('>Z').workplane().moveTo(0, -half_height).line(57.5, 0).line(0, 23).line(10, 0) \
    .line(0, 56).line(-7, 0).line(0, 36).line(10, 0).line(0, 91).line(-10, 0).line(0, 11).line(10, 0) \
    .line(0, 8).line(-70.5, 0).mirrorY().cutBlind(-4)
result = result.cut(chunk)
del chunk
result = result.sub_edges(old_edges, '|Z').fillet(tool_radius)

# Cut off the L shaped keyguard
old_edges = result.edges()
chunk = cq.Workplane("XY").workplane(4).rect(width, height, True).extrude(2)
chunk = chunk.faces('>Z').workplane().moveTo(46.5, 4.48).line(0, -27).line(-68, 0).line(0, -37.5) \
    .line(-34.5, 0).line(0, 64.5).lineTo(46.5, 4.48).wire().cutBlind(-2)
result = result.cut(chunk)
del chunk
result = result.sub_edges(old_edges, '|Z').fillet(tool_radius).sub_edges(old_edges, '#Z and >Z').chamfer(1)

# LK/RK keyguards
lkkg_x = -61.25
lkkg_y = 80.2
lkkg_dx = 122.5
lkkg_dy = -10.2
lkkg_size = (16.5, 2.2)
lkkg_points = [(x * lkkg_dx + lkkg_x, y * lkkg_dy + lkkg_y,) for x in range(2) for y in range(5)]
lkkg_left_points = [(x * lkkg_dx + lkkg_x, y * lkkg_dy + lkkg_y,) for x in [0] for y in range(5)]
lkkg_right_points = [(x * lkkg_dx + lkkg_x, y * lkkg_dy + lkkg_y,) for x in [1] for y in range(5)]


def create_keyguards(self, right=False):
    lk_solid = cq.Workplane("XY").rect(*lkkg_size).extrude(2)
    if right:
        lk_solid = lk_solid.edges('>Z and (>Y or <Y or >X)').chamfer(0.5) \
            .edges('>Z and <X').chamfer(1.999)
    else:
        lk_solid = lk_solid.edges('>Z and (>Y or <Y or <X)').chamfer(0.5) \
            .edges('>Z and >X').chamfer(1.999)

    lk_solid = lk_solid.objects[0]

    solids = self.eachpoint(lambda loc: lk_solid.moved(loc), True)
    return self.union(solids, clean=True)


cq.Workplane.create_keyguards = create_keyguards

result = result.workplane(2).pushPoints(lkkg_left_points).create_keyguards()
result = result.workplane(2).pushPoints(lkkg_right_points).create_keyguards(True)


# Screen
old_edges = result.edges()
result = result.pushPoints([(0, 61.5)]).rect(100, 75).cutThruAll() \
    .sub_edges(old_edges, '|Z').fillet(tool_radius) \
    .sub_edges(old_edges, '#Z exc <Z').chamfer(thickness - 1)

del old_edges
