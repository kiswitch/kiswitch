#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

from KiSwitch.deps_path import deps_path

with deps_path():
    from KicadModTree.Vector import Vector3D
    from KicadModTree.KicadFileHandler import DEFAULT_LAYER_WIDTH


class GenericRenderer(object):
    def __init__(self, scale: int = 1, center: tuple[int, int] = (0, 0)):
        self.mod = None
        self.scale = scale
        self.center = center

    def draw(self, mod):
        self.mod = mod
        nodes = self.mod.serialize()

        grouped_nodes = {}

        for single_node in nodes:
            node_type = single_node.__class__.__name__

            current_nodes = grouped_nodes.get(node_type, [])
            current_nodes.append(single_node)

            grouped_nodes[node_type] = current_nodes

        for key, value in sorted(grouped_nodes.items()):
            # check if key is a base node, except Model and Text
            if key not in {"Arc", "Circle", "Line", "Pad", "Polygon"}:
                print(f"ignoring {key}")
                continue

            # render base nodes
            for node in value:
                self._call_draw(node)

    def point_to_pixel(self, point) -> tuple[int, int]:
        point = Vector3D(point)
        return (self.scale_value(point.x) + self.center[0], self.scale_value(point.y) + self.center[1])

    def scale_value(self, value) -> int:
        return int(value * self.scale)

    def width_to_pixel(self, width, layer=None) -> int:
        if not width:
            if layer in DEFAULT_LAYER_WIDTH:
                width = DEFAULT_LAYER_WIDTH[layer]
            else:
                width = 0.1

        return self.scale_value(width)

    def layer_to_color(self, layer):
        color_map = {
            "F.Cu": "#C83434FF",
            "B.Cu": "#4D7FC4FF",
            "F.Paste": "#B4A09AE6",
            "B.Paste": "#00C2C2E6",
            "F.SilkS": "#F2EDA1FF",
            "B.SilkS": "#E8B2A7FF",
            "F.Mask": "#D864FF66",
            "B.Mask": "#02FFEE66",
            "Edge.Cuts": "#D0D2CDFF",
            "User.D": "#C2C2C2FF",
            "B.CrtYd": "#26E9FFFF",
            "F.CrtYd": "#FF26E2FF",
            "F.Fab": "#AFAFAFFF",
            "B.Fab": "#585D84FF",
            "Eco1.User": "#B4DBD2FF",
            "ThroughHole": "#E3B72EFF",
        }

        if layer in color_map:
            return color_map[layer]
        else:
            print(f"layer {layer} not found in color map")
            return "#D75B6BCC"

    def _call_draw(self, node):
        """
        call the corresponding method to draw the node
        """
        method_type = node.__class__.__name__
        method_name = f"_draw_node_{method_type}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            raise NotImplementedError(f"{method_name} (node) not found, cannot draw the node of type {method_type}")

    def _draw_node_ArcPoints(self, node):
        raise NotImplementedError
        # # in KiCAD, some file attributes of Arc are named not in the way of their real meaning
        # center_pos = node.getRealPosition(node.center_pos)
        # end_pos = node.getRealPosition(node.start_pos)

        # return [
        #         ['start', center_pos.x, center_pos.y],
        #         ['end', end_pos.x, end_pos.y],
        #         ['angle', node.angle]
        #        ]

    def _draw_node_Arc(self, node):
        raise NotImplementedError
        # sexpr = ['fp_arc']
        # sexpr += self._draw_node_ArcPoints(node)
        # sexpr += [
        #           ['layer', node.layer],
        #           ['width', _get_layer_width(node.layer, node.width)]
        #          ]  # NOQA

        # return sexpr

    def _draw_node_Circle(self, node):
        print("_draw_node_Circle")
        center_pos = self.point_to_pixel(node.getRealPosition(node.center_pos))
        radius = self.scale_value(node.radius)
        color = self.layer_to_color(node.layer)
        width = self.width_to_pixel(node.width, node.layer)

        self.draw_circle(center_pos, radius, color, width)

    def _draw_node_Line(self, node):
        start_pos = self.point_to_pixel(node.getRealPosition(node.start_pos))
        end_pos = self.point_to_pixel(node.getRealPosition(node.end_pos))
        color = self.layer_to_color(node.layer)
        width = self.width_to_pixel(node.width, node.layer)

        self.draw_line(start_pos, end_pos, color, width)

    def _draw_node_Text(self, node):
        print("_draw_node_Text")
        # sexpr = ['fp_text', node.type, node.text]

        # position, rotation = node.getRealPosition(node.at, node.rotation)
        # if rotation:
        #     sexpr.append(['at', position.x, position.y, rotation])
        # else:
        #     sexpr.append(['at', position.x, position.y])

        # sexpr.append(['layer', node.layer])
        # if node.hide:
        #     sexpr.append('hide')
        # sexpr.append(SexprSerializer.NEW_LINE)

        # effects = [
        #         'effects',
        #         ['font',
        #             ['size', node.size.x, node.size.y],
        #             ['thickness', node.thickness]]]

        # if node.mirror:
        #     effects.append(['justify', 'mirror'])

        # sexpr.append(effects)
        # sexpr.append(SexprSerializer.NEW_LINE)

        # return sexpr

    def _draw_node_Model(self, node):
        print("_draw_node_Model")
        # sexpr = ['model', node.filename,
        #          SexprSerializer.NEW_LINE,
        #          ['at', ['xyz', node.at.x, node.at.y, node.at.z]],
        #          SexprSerializer.NEW_LINE,
        #          ['scale', ['xyz', node.scale.x, node.scale.y, node.scale.z]],
        #          SexprSerializer.NEW_LINE,
        #          ['rotate', ['xyz', node.rotate.x, node.rotate.y, node.rotate.z]],
        #          SexprSerializer.NEW_LINE
        #         ]  # NOQA

        # return sexpr

    def _draw_node_CustomPadPrimitives(self, pad):
        print("_draw_node_CustomPadPrimitives")
        # all_primitives = []
        # for p in pad.primitives:
        #     all_primitives.extend(p.serialize())

        # grouped_nodes = {}

        # for single_node in all_primitives:
        #     node_type = single_node.__class__.__name__

        #     current_nodes = grouped_nodes.get(node_type, [])
        #     current_nodes.append(single_node)

        #     grouped_nodes[node_type] = current_nodes

        # sexpr_primitives = []

        # for key, value in sorted(grouped_nodes.items()):
        #     # check if key is a base node, except Model
        #     if key not in {'Arc', 'Circle', 'Line', 'Pad', 'Polygon', 'Text'}:
        #         continue

        #     # render base nodes
        #     for p in value:
        #         if isinstance(p, Polygon):
        #             sp = ['gr_poly',
        #                   self._draw_node_PolygonPoints(p, newline_after_pts=True)
        #                  ]  # NOQA
        #         elif isinstance(p, Line):
        #             sp = ['gr_line'] + self._draw_node_LinePoints(p)
        #         elif isinstance(p, Circle):
        #             sp = ['gr_circle'] + self._draw_node_CirclePoints(p)
        #         elif isinstance(p, Arc):
        #             sp = ['gr_arc'] + self._draw_node_ArcPoints(p)
        #         else:
        #             raise TypeError('Unsuported type of primitive for custom pad.')
        #         sp.append(['width', DEFAULT_WIDTH_POLYGON_PAD if p.width is None else p.width])
        #         sexpr_primitives.append(sp)
        #         sexpr_primitives.append(SexprSerializer.NEW_LINE)

        # return sexpr_primitives

    def _draw_node_Pad(self, node):
        print("_draw_node_Pad")
        # sexpr = ['pad', node.number, node.type, node.shape]

        position, rotation = node.getRealPosition(node.at, node.rotation)

        position = self.point_to_pixel(position)
        rotation = rotation % 360

        print(node.layers)

        color = self.layer_to_color(None)

        size = (self.scale_value(node.size.x), self.scale_value(node.size.y))

        print(size)

        self.draw_circle(position, size[0] // 2, color)

        # if not rotation % 360 == 0:
        #     sexpr.append(['at', position.x, position.y, rotation])
        # else:
        #     sexpr.append(['at', position.x, position.y])

        # sexpr.append(['size', node.size.x, node.size.y])

        # if node.type in [Pad.TYPE_THT, Pad.TYPE_NPTH]:

        #     if node.drill.x == node.drill.y:
        #         drill_config = ['drill', node.drill.x]
        #     else:
        #         drill_config = ['drill', 'oval', node.drill.x, node.drill.y]

        #     # append offset only if necessary
        #     if node.offset.x != 0 or node.offset.y != 0:
        #         drill_config.append(['offset', node.offset.x,  node.offset.y])

        #     sexpr.append(drill_config)

        # sexpr.append(['layers'] + node.layers)
        # if node.shape == Pad.SHAPE_ROUNDRECT:
        #     sexpr.append(['roundrect_rratio', node.radius_ratio])

        # if node.shape == Pad.SHAPE_CUSTOM:
        #     # gr_line, gr_arc, gr_circle or gr_poly
        #     sexpr.append(SexprSerializer.NEW_LINE)
        #     sexpr.append(['options',
        #                  ['clearance', node.shape_in_zone],
        #                  ['anchor', node.anchor_shape]
        #                 ])  # NOQA
        #     sexpr.append(SexprSerializer.NEW_LINE)
        #     sexpr_primitives = self._draw_node_CustomPadPrimitives(node)
        #     sexpr.append(['primitives', SexprSerializer.NEW_LINE] + sexpr_primitives)

        # if node.solder_paste_margin_ratio != 0 or node.solder_mask_margin != 0 or node.solder_paste_margin != 0:
        #     sexpr.append(SexprSerializer.NEW_LINE)
        #     if node.solder_mask_margin != 0:
        #         sexpr.append(['solder_mask_margin', node.solder_mask_margin])
        #     if node.solder_paste_margin_ratio != 0:
        #         sexpr.append(['solder_paste_margin_ratio', node.solder_paste_margin_ratio])
        #     if node.solder_paste_margin != 0:
        #         sexpr.append(['solder_paste_margin', node.solder_paste_margin])

        # return sexpr

    def _draw_node_PolygonPoints(self, node, newline_after_pts=False):
        print("_draw_node_PolygonPoints")
        # node_points = ['pts']
        # if newline_after_pts:
        #     node_points.append(SexprSerializer.NEW_LINE)
        # points_appended = 0
        # for n in node.nodes:
        #     if points_appended >= 4:
        #         points_appended = 0
        #         node_points.append(SexprSerializer.NEW_LINE)
        #     points_appended += 1

        #     n_pos = node.getRealPosition(n)
        #     node_points.append(['xy', n_pos.x, n_pos.y])

        # return node_points

    def _draw_node_Polygon(self, node):
        print("_draw_node_Polygon")
        node_points = self._draw_node_PolygonPoints(node)

        # sexpr = ['fp_poly',
        #          node_points,
        #          ['layer', node.layer],
        #          ['width', _get_layer_width(node.layer, node.width)]
        #         ]  # NOQA

        # return sexpr

    def draw_circle(self, center: tuple[int, int], radius: int, color: str, width: int | None = None) -> None:
        raise NotImplementedError

    def draw_arc(self, center: tuple[int, int], start: tuple[int, int], end: tuple[int, int], color: str, width: int):
        raise NotImplementedError

    def draw_line(self, start: tuple[int, int], end: tuple[int, int], color: str, width: int):
        raise NotImplementedError

    def draw_rect(self, start: tuple[int, int], end: tuple[int, int], color: str, width: int):
        raise NotImplementedError

    def draw_polygon(self, points: list[tuple[int, int]], color: str, width: int):
        raise NotImplementedError
