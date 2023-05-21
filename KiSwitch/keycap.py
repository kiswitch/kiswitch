#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

from KiSwitch.deps_path import deps_path
from KiSwitch.property import kiswitch_property

with deps_path():
    from KicadModTree.Vector import Vector2D
    from KicadModTree.nodes.Node import Node
    from KicadModTree.nodes.specialized import RectLine, PolygoneLine


class Keycap(Node):
    KEYCAP_TYPE_REGULAR = "regular"
    KEYCAP_TYPE_ISO_ENTER = "ISOEnter"

    KEYCAP_1U = "1u"
    KEYCAP_1_25U = "1.25u"
    KEYCAP_1_25U_90 = "1.25u90"
    KEYCAP_1_5U = "1.5u"
    KEYCAP_1_5U_90 = "1.5u90"
    KEYCAP_1_75U = "1.75u"
    KEYCAP_1_75U_90 = "1.75u90"
    KEYCAP_2U = "2u"
    KEYCAP_2U_90 = "2u90"
    KEYCAP_2_25U = "2.25u"
    KEYCAP_2_25U_90 = "2.25u90"
    KEYCAP_2_5U = "2.5u"
    KEYCAP_2_5U_90 = "2.5u90"
    KEYCAP_2_75U = "2.75u"
    KEYCAP_2_75U_90 = "2.75u90"
    KEYCAP_3U = "3u"
    KEYCAP_3U_90 = "3u90"
    KEYCAP_4U = "4u"
    KEYCAP_4_5U = "4.5u"
    KEYCAP_5_5U = "5.5u"
    KEYCAP_6U = "6u"
    KEYCAP_6U_OFFSET = "6uOffset"
    KEYCAP_6_25U = "6.25u"
    KEYCAP_6_5U = "6.5u"
    KEYCAP_7U = "7u"
    KEYCAP_ISO_ENTER = "ISOEnter"
    KEYCAP_ISO_ENTER_90 = "ISOEnter90"
    KEYCAP_ISO_ENTER_180 = "ISOEnter180"
    KEYCAP_ISO_ENTER_270 = "ISOEnter270"

    KEYCAP_DEFAULT_SHAPES = {
        KEYCAP_1U: {"type": KEYCAP_TYPE_REGULAR, "width": 1},
        KEYCAP_1_25U: {"type": KEYCAP_TYPE_REGULAR, "width": 1.25},
        KEYCAP_1_25U_90: {"type": KEYCAP_TYPE_REGULAR, "width": 1.25, "rotation": 90},
        KEYCAP_1_5U: {"type": KEYCAP_TYPE_REGULAR, "width": 1.5},
        KEYCAP_1_5U_90: {"type": KEYCAP_TYPE_REGULAR, "width": 1.5, "rotation": 90},
        KEYCAP_1_75U: {"type": KEYCAP_TYPE_REGULAR, "width": 1.75},
        KEYCAP_1_75U_90: {"type": KEYCAP_TYPE_REGULAR, "width": 1.75, "rotation": 90},
        KEYCAP_2U: {"type": KEYCAP_TYPE_REGULAR, "width": 2},
        KEYCAP_2U_90: {"type": KEYCAP_TYPE_REGULAR, "width": 2, "rotation": 90},
        KEYCAP_2_25U: {"type": KEYCAP_TYPE_REGULAR, "width": 2.25},
        KEYCAP_2_25U_90: {"type": KEYCAP_TYPE_REGULAR, "width": 2.25, "rotation": 90},
        KEYCAP_2_5U: {"type": KEYCAP_TYPE_REGULAR, "width": 2.5},
        KEYCAP_2_5U_90: {"type": KEYCAP_TYPE_REGULAR, "width": 2.5, "rotation": 90},
        KEYCAP_2_75U: {"type": KEYCAP_TYPE_REGULAR, "width": 2.75},
        KEYCAP_2_75U_90: {"type": KEYCAP_TYPE_REGULAR, "width": 2.75, "rotation": 90},
        KEYCAP_3U: {"type": KEYCAP_TYPE_REGULAR, "width": 3},
        KEYCAP_3U_90: {"type": KEYCAP_TYPE_REGULAR, "width": 3, "rotation": 90},
        KEYCAP_4U: {"type": KEYCAP_TYPE_REGULAR, "width": 4},
        KEYCAP_4_5U: {"type": KEYCAP_TYPE_REGULAR, "width": 4.5},
        KEYCAP_5_5U: {"type": KEYCAP_TYPE_REGULAR, "width": 5.5},
        KEYCAP_6U: {"type": KEYCAP_TYPE_REGULAR, "width": 6},
        KEYCAP_6U_OFFSET: {"type": KEYCAP_TYPE_REGULAR, "width": 6, "offset_x": -9.525},
        KEYCAP_6_25U: {"type": KEYCAP_TYPE_REGULAR, "width": 6.25},
        KEYCAP_6_5U: {"type": KEYCAP_TYPE_REGULAR, "width": 6.5},
        KEYCAP_7U: {"type": KEYCAP_TYPE_REGULAR, "width": 7},
        KEYCAP_ISO_ENTER: {"type": KEYCAP_TYPE_ISO_ENTER},
        KEYCAP_ISO_ENTER_90: {"type": KEYCAP_TYPE_ISO_ENTER, "rotation": 90},
        KEYCAP_ISO_ENTER_180: {"type": KEYCAP_TYPE_ISO_ENTER, "rotation": 180},
        KEYCAP_ISO_ENTER_270: {"type": KEYCAP_TYPE_ISO_ENTER, "rotation": 270},
    }

    # keycap parameters
    name = kiswitch_property(base_type=str, default="")
    description = kiswitch_property(base_type=str, default="")
    tags = kiswitch_property(base_type=str, default="Keycap")
    type = kiswitch_property(base_type=str, allowed_list=[KEYCAP_TYPE_REGULAR, KEYCAP_TYPE_ISO_ENTER])
    spacing_x = kiswitch_property(base_type=float, default=19.05)
    spacing_y = kiswitch_property(base_type=float)
    width = kiswitch_property(base_type=float, default=1)
    rotation = kiswitch_property(base_type=float, default=0)
    offset_x = kiswitch_property(base_type=float, default=0)
    offset_y = kiswitch_property(base_type=float, default=0)

    def __init__(self, **kwargs):
        super().__init__()

        for key, value in kwargs.items():
            setattr(self, key, value)

        if self.spacing_y == None:
            self.spacing_y = self.spacing_x

        if self.type == self.KEYCAP_TYPE_REGULAR:
            self.virtual_childs = self._init_regular_keycap()
        elif self.type == self.KEYCAP_TYPE_ISO_ENTER:
            self.virtual_childs = self._init_ISOEnter_keycap()

        self.description += self.tags

    def _init_regular_keycap(self):
        nodes = []

        if self.width is None:
            raise Exception("Keycap width not specified")

        self.tags += f" {self.width:3.2f}u"
        self.name += f"{self.width:3.2f}u"
        if self.rotation != 0:
            self.tags += f" {int(self.rotation)}deg"
            self.name += f"_{int(self.rotation)}deg"
        if self.offset_x != 0 or self.offset_y != 0:
            self.tags += " Offset"
            self.name += "_Offset"

        start = Vector2D(-(self.spacing_x * self.width) / 2 + self.offset_x, -self.spacing_y / 2 + self.offset_y)
        end = Vector2D((self.spacing_x * self.width) / 2 + self.offset_x, self.spacing_y / 2 + self.offset_y)

        if self.rotation:
            start = start.rotate(self.rotation)
            end = end.rotate(self.rotation)

        nodes.append(RectLine(start=start, end=end, layer="Dwgs.User", width=0.1))

        return nodes

    def _init_ISOEnter_keycap(self):
        nodes = []

        self.tags += " ISOEnter"
        self.name += f"ISOEnter"
        if self.rotation != 0:
            self.tags += f" {int(self.rotation)}deg"
            self.name += f"_{int(self.rotation)}deg"

        polyline = [
            Vector2D((self.spacing_x * 1.25) / 2 + self.offset_x, self.spacing_y + self.offset_y),
            Vector2D((self.spacing_x * 1.25) / 2 + self.offset_x, -self.spacing_y + self.offset_y),
            Vector2D(-(self.spacing_x * 1.75) / 2 + self.offset_x, -self.spacing_y + self.offset_y),
            Vector2D(-(self.spacing_x * 1.75) / 2 + self.offset_x, 0 + self.offset_y),
            Vector2D(-(self.spacing_x * 1.25) / 2 + self.offset_x, 0 + self.offset_y),
            Vector2D(-(self.spacing_x * 1.25) / 2 + self.offset_x, self.spacing_y + self.offset_y),
            Vector2D((self.spacing_x * 1.25) / 2 + self.offset_x, self.spacing_y + self.offset_y),
        ]

        if self.rotation:
            for point in polyline:
                point = point.rotate(self.rotation)

        nodes.append(PolygoneLine(polygone=polyline, layer="Dwgs.User", width=0.1))

        return nodes

    def getVirtualChilds(self):
        return self.virtual_childs


class KeycapChoc(Keycap):
    spacing_x = kiswitch_property(base_type=float, default=18)
    spacing_y = kiswitch_property(base_type=float, default=17)
