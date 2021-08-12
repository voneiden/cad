from typing import Optional, Union, Tuple

from cadquery import cq, Selector


def sub_edges(self: cq.Workplane,
              sub: Union['cq.Workplane', str],
              selector: Optional[Union[Selector, str]] = None,
              tag: Optional[str] = None,
              ):
    """
    Subtract given edges from current workplane edges, optionally filtered through selectors.
    Useful for applying fillets/chamfers to specific areas of the board without using
    complicated selectors.
    """
    wp = self.edges(selector, tag)
    if isinstance(sub, str):
        objects = self.workplaneFromTagged(sub).objects
    elif isinstance(sub, list):
        objects = sub
    else:
        objects = sub.objects

    wp.objects = [o for o in wp.objects if o not in objects]
    return wp


def sub_wires(self: cq.Workplane,
              sub: Union['cq.Workplane', str, list],
              selector: Optional[Union[Selector, str]] = None,
              tag: Optional[str] = None,
              ):
    """
    Subtract given wires from current workplane wires, optionally filtered through selectors.
    Useful for applying fillets/chamfers to specific areas of the board without using
    complicated selectors.
    """
    wp = self.wires(selector, tag)
    if isinstance(sub, str):
        objects = self.workplaneFromTagged(sub).objects
    elif isinstance(sub, list):
        objects = sub
    else:
        objects = sub.objects

    wp.objects = [o for o in wp.objects if o not in objects]
    return wp


def drop_outermost(self: cq.Workplane):
    self.objects = cq.sortWiresByBuildOrder(self.objects)[0][1:]
    return self


def rounded_rect(self: cq.Workplane, xlen, ylen, fillet_radius):
    rect = cq.Workplane().rect(xlen, ylen).val()
    pts = rect.Vertices()
    rect = rect.fillet2D(fillet_radius, pts)
    return self.eachpoint(lambda loc: rect.moved(loc), True)


class EdgeWireTracker:
    def __init__(self):
        self.previous_edges = []
        self.previous_wires = []

    def update_edges_and_wires(self, wp):
        edges = wp.sub_edges(self.previous_edges).objects
        wires = wp.sub_wires(self.previous_wires).objects
        self.previous_edges += edges
        self.previous_wires += wires
        return edges, wires


# (x, xd, xn)
# (x1,if xp and len(xd)  x2, x3)
def grid(self: cq.Workplane,
         xd: Optional[Tuple[int, float]] = None,
         yd: Optional[Tuple[int, float]] = None,
         xp: Optional[Tuple[int, float]] = None,
         yp: Optional[Tuple[int, float]] = None):
    if xd and xp:
        raise ValueError("Both xd and xp can't be given")

    if yd and yp:
        raise ValueError("Both yd and yp can't be given")

    if xd and len(xd) != 3:
        raise ValueError("xd must contain three elements: initial, delta and count")

    if yd and len(yd) != 3:
        raise ValueError("yd must contain three elements: initial, delta and count")

    points = [((xd[0] + x * xd[1] if xd else x), (yd[0] + y * yd[1] if yd else y))
              for x in (range(xd[2]) if xd else xp)
              for y in (range(yd[2]) if yd else yp)]

    return self.pushPoints(points)


def panel_text(self: cq.Workplane, text):
    return self.text(text, 4, -5, fontPath='./fonts/xA320PanelFont_V0.2b.ttf')
