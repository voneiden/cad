from typing import Optional, Union, Tuple, TypeVar
import cadquery
from cadquery import cq, Selector, Assembly
import logging
logger = logging.getLogger('cqlib')

T = TypeVar("T", bound='CustomWorkplaneMixin')


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


def rounded_rect(self: T, xlen, ylen, fillet_radius) -> T:
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


def panel_text(self: cq.Workplane, text, fontsize=4, distance=-5, fontPath='./fonts/xA320PanelFont_V0.2b.ttf',
               **kwargs):
    return self.text(text, fontsize, distance, fontPath=fontPath, **kwargs)


def add_all(self, objs, x, y):
    objs = list(objs)
    return self.pushPoints(((x, y) for _ in range(len(objs)))).eachpoint(lambda loc: objs.pop().moved(loc), True)


def _show_wrapper(show_object):
    def _show(self, name=None, options=None):
        if options is None:
            options = {}
        show_object(self, name, options)

    return _show


def _debug_wrapper(debug):
    def _debug(self, name=None):
        debug(self, name)

    return _debug


def dummy_show_f(self, name=None, options=None):
    logger.info("No show available")


def dummy_debug_f(self, name=None):
    logger.info("No show available")


def dummy_show_object(obj, name=None, options=None):
    logger.info("No show available")


def dummy_debug(obj, name=None):
    logger.info("No show available")


class CustomWorkplane(cq.Workplane):
    sub_edges = sub_edges
    rounded_rect = rounded_rect
    grid = grid
    panel_text = panel_text
    add_all = add_all
    show = dummy_show_f
    debug = dummy_debug_f


class CustomWorkplaneMixin:
    def rounded_rect(self: T, xlen, ylen, fillet_radius) -> T:
        rect = cq.Workplane().rect(xlen, ylen).val()
        pts = rect.Vertices()
        rect = rect.fillet2D(fillet_radius, pts)
        return self.eachpoint(lambda loc: rect.moved(loc), True)


class CustomAssembly(Assembly):
    show = dummy_show_f
    debug = dummy_debug_f


class CustomFunctions:
    show_object = dummy_show_object
    debug = dummy_debug


def setup(caller_locals):
    if 'show_object' in caller_locals:
        show_object = caller_locals['show_object']
        show_f = _show_wrapper(show_object)
    else:
        show_object = dummy_show_object
        show_f = dummy_show_f

    if 'debug' in caller_locals:
        debug = caller_locals['debug']
        debug_f = _debug_wrapper(debug)
    else:
        debug = dummy_debug
        debug_f = dummy_debug_f

    CustomWorkplane.show = show_f
    CustomWorkplane.debug = debug_f
    Assembly.show = show_f
    Assembly.debug = debug_f
    CustomFunctions.show_object = show_object
    CustomFunctions.debug = debug

    cq.Workplane = CustomWorkplane
    cq.Assembly = Assembly
    cadquery.Workplane = CustomWorkplane
    cadquery.Assembly = CustomAssembly


