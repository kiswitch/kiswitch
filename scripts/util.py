from KicadModTree.nodes.Node import Node
from KicadModTree.nodes.base import Pad
from KicadModTree.Vector import Vector2D
from math import sqrt


class SwitchMountHole(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        kwargs.__setitem__('type', Pad.TYPE_NPTH)
        kwargs.__setitem__('shape', kwargs.get('shape', Pad.SHAPE_CIRCLE))
        kwargs.__setitem__('layers', Pad.LAYERS_NPTH)
        if kwargs.get('size', None) is None:
            drill = kwargs.get('drill')
            kwargs.__setitem__('size', Vector2D(drill, drill) if type(drill) in [int, float] else Vector2D(drill))
        self.virtual_childs = [Pad(**kwargs)]

    def getVirtualChilds(self):
        return self.virtual_childs


class SwitchPad(Node):

    TYPE_REGULAR = 'regular'
    TYPE_MASKED = 'masked'
    TYPE_SMALL_TOP = 'small_top'

    _TYPES = [TYPE_REGULAR, TYPE_MASKED, TYPE_SMALL_TOP]

    LAYERS_FRONT = ['F.Cu', 'F.Mask']
    LAYERS_BACK = ['B.Cu', 'B.Mask']
    LAYERS_FRONT_MASK = ['F.Mask']
    LAYERS_MASKED_FRONT = ['*.Cu', 'B.Mask']

    def __init__(self, **kwargs):

        Node.__init__(self)

        self.virtual_childs = []

        self.type = kwargs.get('pad_type', SwitchPad.TYPE_MASKED)

        if self.type not in SwitchPad._TYPES:
            raise ValueError(f'{self.type} is an invalid type for SwitchPad')

        elif self.type == SwitchPad.TYPE_REGULAR:
            self._init_regular_pad(**kwargs)
        if self.type == SwitchPad.TYPE_MASKED:
            self._init_masked_pad(**kwargs)
        elif self.type == SwitchPad.TYPE_SMALL_TOP:
            self._init_small_top_pad(**kwargs)

    def _init_regular_pad(self, **kwargs):
        kwargs.__setitem__('type', Pad.TYPE_THT)
        kwargs.__setitem__('layers', Pad.LAYERS_THT)
        self.virtual_childs.append(Pad(**kwargs))

    def _init_masked_pad(self, **kwargs):
        self.mask_margin = kwargs.get(
            'solder_mask_margin', 0.05)  # default 0.05mm
        self.drill_size = kwargs.get('drill')

        kwargs.__setitem__('type', Pad.TYPE_THT)
        kwargs.__setitem__('layers', SwitchPad.LAYERS_MASKED_FRONT)
        self.virtual_childs.append(Pad(**kwargs))

        size = Vector2D(self.drill_size, self.drill_size) if type(
            self.drill_size) in [int, float] else Vector2D(self.drill_size)

        kwargs.__setitem__('type', Pad.TYPE_SMT)
        kwargs.__setitem__(
            'size', size + Vector2D(self.mask_margin, self.mask_margin))
        kwargs.__setitem__('layers', SwitchPad.LAYERS_FRONT_MASK)
        kwargs.__setitem__('offset', Vector2D(0, 0))
        self.virtual_childs.append(Pad(**kwargs))

    def _init_small_top_pad(self, **kwargs):
        self.annular_ring = kwargs.get('annular_ring', 0.13)  # default 0.13mm
        self.drill_size = kwargs.get('drill')

        kwargs.__setitem__('type', Pad.TYPE_THT)

        kwargs.__setitem__('layers', SwitchPad.LAYERS_BACK)
        self.virtual_childs.append(Pad(**kwargs))

        size = Vector2D(self.drill_size, self.drill_size) if type(
            self.drill_size) in [int, float] else Vector2D(self.drill_size)

        kwargs.__setitem__(
            'size', size + Vector2D(self.annular_ring, self.annular_ring))
        kwargs.__setitem__('layers', SwitchPad.LAYERS_FRONT)
        kwargs.__setitem__('offset', Vector2D(0, 0))
        self.virtual_childs.append(Pad(**kwargs))

    def getVirtualChilds(self):
        return self.virtual_childs


def norm_vector(v):
    source_v = Vector2D(v)
    radius, angle = source_v.to_polar()
    return source_v / radius if radius != 0 else Vector2D(0, 0)

    return new_polyline


def offset_poly(poly: list, offset: float, origin: Vector2D = Vector2D(0, 0), outer_ccw=True):
    new_poly = []
    outer_ccw = 1 if outer_ccw else -1
    closed = poly[0] == poly[-1]

    if closed:
        poly.pop()

    num_points = len(poly)

    for curr in range(num_points):
        curr_point = Vector2D(poly[curr]) - origin
        prev_point = Vector2D(poly[(curr + num_points - 1) % num_points]) - origin
        next_point = Vector2D(poly[(curr + 1) % num_points]) - origin

        vn = next_point - curr_point
        vnn = norm_vector(vn)
        nnn = Vector2D([vnn.y, -vnn.x])

        vp = curr_point - prev_point
        vpn = norm_vector(vp)
        npn = Vector2D([vpn.y * outer_ccw, -vpn.x * outer_ccw])

        bis = (nnn + npn) * outer_ccw
        bisn = norm_vector(bis)

        bislen = offset / sqrt(1 + nnn.x*npn.x + nnn.y*npn.y)

        new_point = (curr_point + (bisn * bislen)) + origin

        new_poly.append(new_point.round_to(0.001))

    if closed:
        new_poly.append(new_poly[0])

    return new_poly
