from build123d import *
from cq_viewer import show_object

from jayel import double_cap as cq_double_cap

# Customizable
width = 20
height = 20
thickness = 1
frame_ledge = 2
frame_ledge_height = 1
frame_thickness = 1
# Derived
lightplate_offset = height / 4 - thickness * 0.25
upper_cap_height = height / 2 - thickness * 1.5
lower_cap_height = height / 2 - thickness * 3.5
with BuildPart() as double_cap:
    with BuildSketch():
        RectangleRounded(20, 20, 1)
        with Locations((0, lightplate_offset), (0, -lightplate_offset)):
            RectangleRounded(width - thickness * 2, upper_cap_height, 1, mode=Mode.SUBTRACT)
    extrude(amount=-2)

    with BuildSketch(double_cap.faces().sort_by(Axis.Z)[0]):
        RectangleRounded(20, 20, 1)
        with Locations((0, lightplate_offset), (0, -lightplate_offset)):
            RectangleRounded(width - thickness * 4, lower_cap_height, 1, mode=Mode.SUBTRACT)
    extrude(amount=3)

with BuildPart() as frame:
    with BuildSketch():
        RectangleRounded(width + 2*frame_thickness + 2*frame_ledge,
                         height + 2*frame_thickness + 2*frame_ledge,
                         1)
        RectangleRounded(width, height, 1, mode=Mode.SUBTRACT)
    extrude(amount=-frame_ledge_height)
    with BuildSketch(frame.faces().sort_by(Axis.Z)[0]):
        RectangleRounded(width + 2*frame_thickness,
                         height + 2*frame_thickness,
                         1)
        RectangleRounded(width, height, 1, mode=Mode.SUBTRACT)
    extrude(amount=5 - frame_ledge_height)


def make_lightplate(text=None, y_offset=0.0):
    with BuildPart() as part:
        with BuildSketch():
            with Locations((0, y_offset)):
                RectangleRounded(width - thickness * 2, upper_cap_height, 1)
        extrude(amount=-2)
        if text:
            with BuildSketch():
                with Locations((0, y_offset)):
                    # TODO
                    Text(text, 5, font_path="../../../fonts/xA320PanelFont_V0.2b.ttf")
            extrude(amount=-0.1, mode=Mode.SUBTRACT)
    return part

upper_plate = make_lightplate("CRIMNL", y_offset=lightplate_offset)
lower_plate = make_lightplate("SCUM", y_offset=-lightplate_offset)

show_object(double_cap, color="gray20")
show_object(frame, color="gray30")
show_object(upper_plate, color="gray40")
show_object(lower_plate, color="gray40")

#show_object(cq_double_cap(20, 20))