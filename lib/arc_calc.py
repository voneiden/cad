import math
# def arc_calc(x, y, x1, y1, angle, adjust_distance =0):
from typing import Tuple, List, Optional, Union

from cadquery import cq


def arc(start, angle, adjust_distance: Union[int, float] = 0):
    radius = length(start)

    # Flip the angle so that positive angle == clockwise
    final_angle = angle + arc_length_to_degrees(adjust_distance, radius)
    print("(final angle: ", final_angle, ")")
    half_angle = final_angle / 2

    v_final = rotate(start, final_angle)
    v_half = rotate(start, half_angle)

    return (v_half[0], v_half[1]), (v_final[0], v_final[1])


# r**2 = (x - x0)**2 + (y - y0)**2
# r**2 = (x - x1)**2 + (y - y1)**2

def length(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def unit(v, mul=1):
    l = length(v)
    return v[0] / l * mul, v[1] / l * mul


def rotate(v, angle):
    x, y = v
    angle_radians = math.radians(-angle)
    c = math.cos(angle_radians)
    s = math.sin(angle_radians)
    return c * x - s * y, s * x + c * y


def arc_length_to_degrees(l, r):
    return l / (2 * math.pi * r) * 360


def add_previous_arc(current_arc, previous_arc):
    return (
        (current_arc[0][0] + previous_arc[0], current_arc[0][1] + previous_arc[1]),
        (current_arc[1][0] + previous_arc[0], current_arc[1][1] + previous_arc[1])
    )


def sum(v1, v2):
    print(v1)
    print(v2)
    return v1[0] + v2[0], v1[1] + v2[1]

def sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


# Vector rotation
# x2 = cos a x1 - sin a y1
# y2 = sin a x1 + cos a y1

# Arc length l = 2 pi r (a/360)
