import cadquery as cq

import lib

cq.Workplane.sub_edges = lib.sub_edges
cq.Workplane.rounded_rect = lib.rounded_rect
cq.Workplane.grid = lib.grid

width = 141
height = 225
half_height = height / 2

tool_radius = 1.5875  # 1/8"

# Initial 2D workpiece
result = cq.Workplane("XY").rect(width, height, True)

# Alpha keyboard sketch
result = result.grid(xd=(-7.5, 14.25, 5), yd=(-30.5, -14.2, 6)).rounded_rect(10, 10, tool_radius)

# Num keyboard sketch
result = result.grid(xd=(-20.5, -14.5, 3), yd=(-66.5, -12, 4)).circle(5)

# FN keys
fn_x = -47.25
fn_dx = 17
fn_y = -2.77
fn_dy = -12.5
fn_size = (13.5, 10.5)
result = result.grid(xd=(fn_x, fn_dx, 6), yd=(fn_y, fn_dy, 2)).rounded_rect(*fn_size, tool_radius)
result = result.grid(xd=(fn_x, fn_dx, 2), yd=(fn_y + fn_dy * 2, fn_dy, 3)).rounded_rect(*fn_size, tool_radius)

# Brightness keys
result = result.grid(xd=(53.5, 0, 1), yd=(-3.5, -12, 2)).rounded_rect(8, 10, tool_radius)

# LK/RK keys
result = result.grid(xd=(-64, 128, 2), yd=(85.3, -10.2, 6)).rounded_rect(8, 7, tool_radius)

# Mount holes
result = result.grid(xd=(-65.5, 131, 2), yp=[99, -4, -98]).circle(1.6)

# Indicator lights
result = result.grid(xd=(-32.5, 16.5, 5), yp=[107.5]).rounded_rect(8, 4, tool_radius)

# Big indicators
result = result.grid(xd=(-62, 124, 2), yp=[-58.5]).rounded_rect(5, 30, tool_radius)

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
def create_keyguards(self, right=False):
    lk_solid = cq.Workplane("XY").rect(16.5, 2.2).extrude(2)
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

x = -61.25
yd = (80.2, -10.2, 5)
result = result.workplane(2).grid(xp=[x], yd=yd).create_keyguards()
result = result.workplane(2).grid(xp=[x + 122.5], yd=yd).create_keyguards(True)

# Screen
old_edges = result.edges()
result = result.pushPoints([(0, 61.5)]).rect(100, 75).cutThruAll() \
    .sub_edges(old_edges, '|Z').fillet(tool_radius) \
    .sub_edges(old_edges, '#Z exc <Z').chamfer(3)

del old_edges
