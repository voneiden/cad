from typing import Optional, Union

from cadquery import cq, Selector


def sub_edges(self,
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


def sub_wires(self,
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


def drop_outermost(self):
    self.objects = cq.sortWiresByBuildOrder(self.objects)[0][1:]
    return self


def rounded_rect(self, xlen, ylen, fillet_radius):
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
