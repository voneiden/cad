from typing import Tuple, Union, Optional, List

from cadquery import cq

from lib.arc_calc import length, unit, arc, sub, sum


def create_rotary_selector_arc(
        start: Tuple[Union[float, int], Union[float, int]],
        thickness: Union[float, int],
        angle: Union[float, int],
        inner_ticks: Optional[List[Union[float, int]]] = None,
        outer_ticks: Optional[List[Union[float, int]]] = None,
        tick_width: Union[float, int] = 1,
        tick_height: Union[float, int] = 1,
        round_start=False,
        round_end=False):
    """
    Dragons ahead, bloody confusing code.

    Let's just call it art.

    Use it only to draw clockwise (positive angle) selector arcs.

    :param start: vector to inside arc starting point
    :param thickness: distance between the inner and outer arc
    :param angle: angle to draw
    :param inner_ticks: angle from start of inside ticks
    :param outer_ticks: angle from start of outside ticks
    :param tick_width: tick width
    :param tick_height: tick height
    :return:
    """

    half_tick = tick_width / 2
    inner_radius = length(start)
    outer_start = unit(start, inner_radius + thickness)

    def draw_tick(wp, start, inner=True, ccw=False, start_back=False):
        back_step = half_tick if ccw else -half_tick
        if start_back:
            back = start
            start = arc(back, 0, -back_step)[1]
            front = arc(start, 0, -back_step)[1]
        else:
            back = arc(start, 0, back_step)[1]
            front = arc(start, 0, -back_step)[1]

        direction = unit(start)
        projection = unit(direction, -tick_height if inner else tick_height)
        wp = wp.moveTo(*back).lineTo(*sum(back, projection)).lineTo(*sum(front, projection)).lineTo(*front)
        return wp, back, start, front

    inner_ticks = sorted(inner_ticks) if inner_ticks else []
    outer_ticks = sorted(outer_ticks) if outer_ticks else []

    inner_start_tick = inner_ticks and inner_ticks[0] == 0
    inner_ticks = inner_ticks[1:] if inner_start_tick else inner_ticks

    inner_end_tick = inner_ticks and inner_ticks[-1] == angle
    inner_ticks = inner_ticks[:-1] if inner_end_tick else inner_ticks

    outer_start_tick = outer_ticks and outer_ticks[0] == 0
    outer_ticks = outer_ticks[1:] if outer_start_tick else outer_ticks

    outer_end_tick = outer_ticks and outer_ticks[-1] == angle
    outer_ticks = outer_ticks[:-1] if outer_end_tick else outer_ticks

    result = cq.Workplane().moveTo(*start)

    # Draw the inside arc
    last_arc = start

    if inner_start_tick:
        result, _, _, last_arc = draw_tick(result, start)
        adjust_start_segment = half_tick
    elif outer_start_tick:
        # Step half tick back to be aligned with the outer start tick
        last_arc = arc(start, 0, -half_tick)[1]
        result = result.moveTo(*last_arc)
        adjust_start_segment = -half_tick
    else:
        adjust_start_segment = 0

    if inner_end_tick:
        adjust_end_segment = half_tick
    elif outer_end_tick:
        adjust_end_segment = half_tick
    else:
        adjust_end_segment = 0

    def draw_segments(wp: cq.Workplane, start, angle, ticks: List[Union[float, int]], first_adjust, last_adjust, ccw=False):
        last_arc = start
        ticks.sort()
        if ccw:
            angle = -angle
            ticks = [angle + t for t in ticks]
            ticks.reverse()

        adjust_multiplier = 1 if ccw else -1

        if not ticks:
            adjust = adjust_start_segment + adjust_end_segment
            adjust *= adjust_multiplier
            current = arc(start, angle, adjust)
            return wp.threePointArc(*current), current[1]
        else:
            last_segment_angle = 0
            for segment_i, segment_angle in enumerate(ticks):
                adjust = (first_adjust + half_tick) if segment_i == 0 else half_tick * 2
                adjust *= adjust_multiplier
                segment_angle_delta = segment_angle - last_segment_angle
                last_segment_angle = segment_angle
                current = arc(last_arc, segment_angle_delta, adjust)
                wp = wp.threePointArc(*current)
                wp, _, _, last_arc = draw_tick(wp, current[1], start_back=True, inner=not ccw, ccw=ccw)

            adjust = last_adjust + half_tick
            adjust *= adjust_multiplier
            current = arc(last_arc, angle - last_segment_angle, adjust)
            last_arc = current[1]
            return wp.threePointArc(*current), last_arc

    result, last_arc = draw_segments(result, last_arc, angle, inner_ticks, adjust_start_segment, adjust_end_segment)

    # Update last arc to match outer arc starting position
    if inner_end_tick:
        result, _, _, _ = draw_tick(result, last_arc, start_back=True)
    elif outer_end_tick:
        current = arc(last_arc, 0, tick_width)
        result = result.threePointArc(*current)
        last_arc = current[0]

    # Move to outer arc drawing position (end, draw ccw)
    # and adjust the end segment to match the end ticks
    if inner_end_tick or outer_end_tick:
        last_arc = arc(outer_start, angle, half_tick)[1]
        result = result.lineTo(*last_arc)
        if not outer_end_tick:
            adjust_end_segment = -half_tick
        else:
            adjust_end_segment = half_tick
    elif round_end:
        # Project last arc to middle
        round_center = unit(last_arc, inner_radius + (thickness / 2))
        local_start = sub(last_arc, round_center)
        local_arc = arc(local_start, -180)
        current = [sum(c, round_center) for c in local_arc]
        result = result.threePointArc(*current)
        last_arc = current[1]

    else:
        last_arc = unit(last_arc, thickness + inner_radius)
        result = result.lineTo(*last_arc)

    if outer_end_tick:
        last_arc = unit(last_arc, inner_radius + thickness)
        result, _, _, last_arc = draw_tick(result, last_arc, inner=False, ccw=True, start_back=True)

    # Adjust the outer start segment
    if outer_start_tick:
        adjust_start_segment = half_tick
    elif inner_start_tick:
        adjust_start_segment = -half_tick

    # Draw the outer arc
    result, last_arc = draw_segments(result, last_arc, angle, outer_ticks, adjust_end_segment, adjust_start_segment, ccw=True)

    if outer_start_tick:
        result, _, _, last_arc = draw_tick(result, last_arc, inner=False, ccw=True, start_back=True)

    elif round_start:
        # Project last arc to middle
        round_center = unit(last_arc, inner_radius + (thickness / 2))
        local_start = sub(last_arc, round_center)
        local_arc = arc(local_start, -180)
        current = [sum(c, round_center) for c in local_arc]
        result = result.threePointArc(*current)
        last_arc = current[1]

    return result


def test():
    def add_all(self, objs, x, y):
        objs = list(objs)
        return self.pushPoints(((x, y) for _ in range(len(objs)))).eachpoint(lambda loc: objs.pop().moved(loc), True)

    cq.Workplane.add_all = add_all
    result = cq.Workplane()

    range_arc = create_rotary_selector_arc((-11.5, 0), 1, 180, [], [0, 45, 90, 135], round_start=False, round_end=False)
    range_arc2 = create_rotary_selector_arc((-11.5, 0), 1, 180, [0], [0, 45, 90, 135, 180], round_start=False, round_end=False)
    range_arc3 = create_rotary_selector_arc((-11.5, 0), 1, 180, [180], [0, 45, 90, 135, 180], round_start=False, round_end=False)
    range_arc4 = create_rotary_selector_arc((-11.5, 0), 1, 180, [], [0, 45, 90, 135, 180], round_start=False, round_end=False)
    range_arc5 = create_rotary_selector_arc((-11.5, 0), 1, 180, [], [], round_start=False, round_end=False)
    range_arc6 = create_rotary_selector_arc((-11.5, 0), 1, 180, [], [], round_start=False, round_end=False)

    range_arcX1 = create_rotary_selector_arc((-11.5, 0), 3, 270, [0, 45, 90, 135], [10, 50, 200], round_start=False, round_end=False, tick_height=5)
    range_arcX2 = create_rotary_selector_arc((-11.5, 0), 1, 180, [0, 45, 90, 135, 180], [0], round_start=False, round_end=False)
    range_arcX3 = create_rotary_selector_arc((-11.5, 0), 1, 180, [0, 45, 90, 135, 180], [180], round_start=False, round_end=False)

    d = 12.5
    lol = 0.7071
    #aimpoint = cq.Workplane().lineTo(-d, 0).lineTo(-d * lol, d * lol).lineTo(0, d).lineTo(d * lol, d * lol).lineTo(d, 0).close().vals()
    aimpoint = []
    print("RANGE ARC", range_arc, range_arc.vals())
    xxx = result.add_all(range_arc.close().vals() + aimpoint, 51.84, -5.81)
    xxx2 = result.add_all(range_arc2.close().vals() + aimpoint, 21.84, -25.81)
    xxx3 = result.add_all(range_arc3.close().vals() + aimpoint, 51.84, -25.81)
    xxx4 = result.add_all(range_arc4.close().vals() + aimpoint, -11.84, -25.81)
    xxx5 = result.add_all(range_arc5.close().vals() + aimpoint, 21.84, -5.81)
    xxx6 = result.add_all(range_arc6.close().vals() + aimpoint, -11.84, -5.81)
    xxxX1 = result.add_all(range_arcX1.close().vals() + aimpoint, -11.84, -50.81)
    xxxX2 = result.add_all(range_arcX2.close().vals() + aimpoint, 21.84, -50.81)
    xxxX3 = result.add_all(range_arcX3.close().vals() + aimpoint, 51.84, -50.81)
