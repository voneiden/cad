import cadquery as cq

from lib import cqlib
from projects.a320.mcdu.common import bottom_cutout_outer_margin, cutter_radius, bottom_cutout_inner_margin

cqlib.setup(locals())
cq.Workplane = cqlib.CustomWorkplane
cq.Assembly = cqlib.Assembly
# Alpha cutout is 10x10 mm
# Alpha spacing is 14.25 x 14.20 mm (width / height)
# Best to leave 0.5 mm space on all sides?

cutout_margin = 0.5
size = (10 - cutout_margin * 2, 10 - cutout_margin * 2)

material_thickness = 3


base_button = (
    cq.Workplane()
    .rounded_rect(*size, cutter_radius)
    .extrude(material_thickness)
    .edges('>Z')
    .fillet(1)
)

sphere_radius = 8
detent_depth = 0.75
sphere_offset = sphere_radius + material_thickness - detent_depth
engraving_depth = 0.2

detent_sphere = (
    cq.Workplane()
    .workplane(offset=sphere_offset)
    .sphere(sphere_radius)
)

outer_sphere = (
    cq.Workplane()
    .workplane(offset=sphere_offset)
    .sphere(sphere_radius + engraving_depth)
)




mating_point_distance = (size[0] / 2) - 2.5
base_button = (
    base_button
    .faces('<Z')
    .workplane()
    .rounded_rect(size[0] - bottom_cutout_outer_margin,
                  size[1] - bottom_cutout_outer_margin, cutter_radius)
    .cutBlind(-0.5)
    .faces('<Z')
    .workplane()
    .rounded_rect(size[0] - bottom_cutout_inner_margin,
                  size[1] - bottom_cutout_inner_margin, cutter_radius)
    .cutBlind(-1)
    .faces('<Z[-2]')
    .tag('bottom')
    .end()

)

def create_button(character, detent_sphere, outer_sphere):
    if character:
        letter = (
            cq.Workplane()
            .panel_text(character, 7, material_thickness, fontPath='../../../fonts/blockschrift.ttf')
        )
        cut_sphere = detent_sphere.union(letter).intersect(outer_sphere)
        button = base_button.cut(cut_sphere, clean=True)
        return button
    else:
        return base_button.cut(detent_sphere)

#button = create_button('X', detent_sphere, outer_sphere)


"""
chars = [['A', 'B', 'C', 'D', 'E'],
         ['F', 'G', 'J', 'K', 'L'],
         ['M', 'N', 'O', 'P', 'Q'],
         ['R', 'S', 'T', 'U', 'V'],
         ['W', 'X', 'Y', 'Z', '?']]
"""

a = create_button('A', detent_sphere, outer_sphere)
#b = create_button('B', detent_sphere, outer_sphere)

#button_matrix = cq.Workplane().add(a).center(50, 50).add(b)
#for i, row in enumerate(chars):
#    for j, col in enumerate(row):
#        button_matrix = button_matrix.center(i*20, j*20).add(create_button(col, detent_sphere, outer_sphere))

#button_matrix.show()
cq.Assembly().add(
    create_button(None, detent_sphere, outer_sphere)
    ).save('button.step')

# Destroy construction geometry
del base_button
del detent_sphere
del outer_sphere

def assembly():
    from projects.a320.generic.pcb_switch_led import pcb_switch_led
    from projects.a320.mcdu.mate_alpha import mate
    return (
        cq.Assembly()
        .add(a, name='button', color=cq.Color('red'))
        .add(mate, name='mate', color=cq.Color('orange'))
        .constrain('button?bottom', 'mate?top', 'Plane')
        .add(pcb_switch_led, name='switch')
        .constrain('switch?top', 'mate?bottom', 'Plane')
        .solve()
        #.show(options={'alpha': 0.5})
    )


foo = assembly()
bb = foo.toCompound().BoundingBox()
print(bb)
#foo.save('assembly.step')
#show_object(foo, options={'alpha': 0.5})