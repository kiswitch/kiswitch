#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Rafael Silva <perigoso@riseup.net>

from KiSwitch.deps_path import deps_path

with deps_path():
    from KicadModTree.nodes.Node import Node
    from KicadModTree.nodes.base import Pad
    from KicadModTree.Vector import Vector2D


class SwitchMountHole(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        kwargs.__setitem__("type", Pad.TYPE_NPTH)
        kwargs.__setitem__("shape", kwargs.get("shape", Pad.SHAPE_CIRCLE))
        kwargs.__setitem__("layers", Pad.LAYERS_NPTH)
        if kwargs.get("size", None) is None:
            drill = kwargs.get("drill")
            kwargs.__setitem__("size", Vector2D(drill, drill) if type(drill) in [int, float] else Vector2D(drill))
        self.virtual_childs = [Pad(**kwargs)]

    def getVirtualChilds(self):
        return self.virtual_childs


class SwitchPad(Node):
    TYPE_REGULAR = "regular"
    TYPE_MASKED = "masked"
    TYPE_SMALL_TOP = "small_top"

    _TYPES = [TYPE_REGULAR, TYPE_MASKED, TYPE_SMALL_TOP]

    LAYERS_FRONT = ["F.Cu", "F.Mask"]
    LAYERS_BACK = ["B.Cu", "B.Mask"]
    LAYERS_FRONT_MASK = ["F.Mask"]
    LAYERS_MASKED_FRONT = ["*.Cu", "B.Mask"]

    def __init__(self, **kwargs):
        Node.__init__(self)

        self.virtual_childs = []

        self.type = kwargs.get("pad_type", SwitchPad.TYPE_REGULAR)

        if self.type not in SwitchPad._TYPES:
            raise ValueError(f"{self.type} is an invalid type for SwitchPad")

        elif self.type == SwitchPad.TYPE_REGULAR:
            self._init_regular_pad(**kwargs)
        if self.type == SwitchPad.TYPE_MASKED:
            self._init_masked_pad(**kwargs)
        elif self.type == SwitchPad.TYPE_SMALL_TOP:
            self._init_small_top_pad(**kwargs)

    def _init_regular_pad(self, **kwargs):
        kwargs.__setitem__("type", Pad.TYPE_THT)
        kwargs.__setitem__("layers", Pad.LAYERS_THT)
        self.virtual_childs.append(Pad(**kwargs))

    def _init_masked_pad(self, **kwargs):
        self.mask_margin = kwargs.get("solder_mask_margin", 0.05)  # default 0.05mm
        self.drill_size = kwargs.get("drill")

        kwargs.__setitem__("type", Pad.TYPE_THT)
        kwargs.__setitem__("layers", SwitchPad.LAYERS_MASKED_FRONT)
        self.virtual_childs.append(Pad(**kwargs))

        size = (
            Vector2D(self.drill_size, self.drill_size)
            if type(self.drill_size) in [int, float]
            else Vector2D(self.drill_size)
        )

        kwargs.__setitem__("type", Pad.TYPE_SMT)
        kwargs.__setitem__("size", size + Vector2D(self.mask_margin, self.mask_margin))
        kwargs.__setitem__("layers", SwitchPad.LAYERS_FRONT_MASK)
        kwargs.__setitem__("offset", Vector2D(0, 0))
        self.virtual_childs.append(Pad(**kwargs))

    def _init_small_top_pad(self, **kwargs):
        self.annular_ring = kwargs.get("annular_ring", 0.13)  # default 0.13mm
        self.drill_size = kwargs.get("drill")

        kwargs.__setitem__("type", Pad.TYPE_THT)

        kwargs.__setitem__("layers", SwitchPad.LAYERS_BACK)
        self.virtual_childs.append(Pad(**kwargs))

        size = (
            Vector2D(self.drill_size, self.drill_size)
            if type(self.drill_size) in [int, float]
            else Vector2D(self.drill_size)
        )

        kwargs.__setitem__("size", size + Vector2D(self.annular_ring, self.annular_ring))
        kwargs.__setitem__("layers", SwitchPad.LAYERS_FRONT)
        kwargs.__setitem__("offset", Vector2D(0, 0))
        self.virtual_childs.append(Pad(**kwargs))

    def getVirtualChilds(self):
        return self.virtual_childs
