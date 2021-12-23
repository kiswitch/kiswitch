
from KicadModTree.Vector import Vector2D
from KicadModTree.nodes.Node import Node
from KicadModTree.nodes.specialized import RectLine, PolygoneLine


class Keycap(Node):
    def __init__(self, keycap_type: str = None,
                 spacing: float = None,
                 x_spacing: float = None, y_spacing: float = None,
                 width: float = None, rotation: float = 0,
                 x_offset: float = 0, y_offset: float = 0):

        Node.__init__(self)

        if spacing is not None:
            self.x_spacing = spacing
            self.y_spacing = spacing
        elif x_spacing is None or y_spacing is None:
            raise Exception('Keycap spacing not specified')
        else:
            self.x_spacing = x_spacing
            self.y_spacing = y_spacing

        self.width = width
        self.rotation = rotation
        self.x_offset = x_offset
        self.y_offset = y_offset

        if keycap_type == 'regular':
            self.virtual_childs = self._init_regular_keycap()
        elif keycap_type == 'ISOEnter':
            self.virtual_childs = self._init_ISOEnter_keycap()
        else:
            raise Exception('Keycap type not supported')

    def _init_regular_keycap(self):

        nodes = []

        if self.width is None:
            raise Exception('Keycap width not specified')

        self.tags = f'{self.width:1.2f}u'
        if self.rotation != 0:
            self.tags += f' {self.rotation}deg'
        if self.x_offset != 0 or self.y_offset != 0:
            self.tags += ' Offset'
        self.name = self.tags.replace(' ', '_')

        start = Vector2D(-(self.x_spacing * self.width)/2 + self.x_offset,
                         -self.y_spacing/2 + self.y_offset)
        end = Vector2D((self.x_spacing * self.width)/2 + self.x_offset,
                       self.y_spacing/2 + self.y_offset)

        if self.rotation:
            start = start.rotate(self.rotation)
            end = end.rotate(self.rotation)

        nodes.append(RectLine(start=start, end=end,
                     layer='Dwgs.User', width=0.1))

        return nodes

    def _init_ISOEnter_keycap(self):
        nodes = []

        self.tags = 'ISOEnter'
        if self.rotation != 0:
            self.tags += f' {self.rotation}deg'
        self.name = self.tags.replace(' ', '_')

        polyline = [Vector2D((self.x_spacing*1.25)/2 + self.x_offset,
                             self.y_spacing + self.y_offset),
                    Vector2D((self.x_spacing*1.25)/2 + self.x_offset,
                             -self.y_spacing + self.y_offset),
                    Vector2D(-(self.x_spacing*1.75)/2 + self.x_offset,
                             -self.y_spacing + self.y_offset),
                    Vector2D(-(self.x_spacing*1.75)/2 + self.x_offset,
                             0 + self.y_offset),
                    Vector2D(-(self.x_spacing*1.25)/2 + self.x_offset,
                             0 + self.y_offset),
                    Vector2D(-(self.x_spacing*1.25)/2 + self.x_offset,
                             self.y_spacing + self.y_offset),
                    Vector2D((self.x_spacing*1.25)/2 + self.x_offset,
                             self.y_spacing + self.y_offset)]

        if self.rotation:
            for point in polyline:
                point = point.rotate(self.rotation)

        nodes.append(PolygoneLine(polygone=polyline,
                                  layer='Dwgs.User', width=0.1))

        return nodes

    def getVirtualChilds(self):
        return self.virtual_childs
