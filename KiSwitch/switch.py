#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

from os import path

from KiSwitch.deps_path import deps_path
from KiSwitch.keycap import Keycap
from KiSwitch.property import kiswitch_property
from KiSwitch.nodes import SwitchPad, SwitchMountHole
from KiSwitch.util import offset_poly

with deps_path():
    from KicadModTree.nodes.Footprint import Footprint
    from KicadModTree.nodes.Node import Node
    from KicadModTree.nodes.base import Text, Model, Pad, Line, Arc
    from KicadModTree.nodes.specialized import RectLine, PolygoneLine
    from KicadModTree.Vector import Vector2D as vector


class Switch(Footprint):
    DEFAULT_KEYS = []

    name = kiswitch_property(base_type=str)
    description = kiswitch_property(base_type=str, default="")
    tags = kiswitch_property(base_type=str)
    cutout = kiswitch_property(base_type=bool, default=False)
    annular_ring = kiswitch_property(base_type=float, default=1)
    path3d = kiswitch_property(
        base_type=str,
        default="${KICAD6_3RD_PARTY}/3dmodels/com_github_perigoso_keyswitch-kicad-library/3d-library.3dshapes/",
    )
    model3d = kiswitch_property(base_type=str, list_property=True)
    text_offset = kiswitch_property(base_type=float, default=8)
    switch_w = kiswitch_property(base_type=float, default=18)
    switch_h = kiswitch_property(base_type=float, default=18)
    switch_cut_w = kiswitch_property(base_type=float, default=16)
    switch_cut_h = kiswitch_property(base_type=float, default=16)

    def __init__(self, **kwargs):
        Footprint.__init__(self, None)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.name = self.name.replace(" ", "_")

    def add_generic_nodes(self):
        self._init_generic_nodes()

    def _init_generic_nodes(self):
        # add general values
        self.append(Text(type="reference", text="REF**", at=[0, -self.text_offset], layer="F.SilkS"))
        self.append(Text(type="value", text=self.name, at=[0, self.text_offset], layer="F.Fab"))
        self.append(Text(type="user", text="%R", at=[0, 0], layer="F.Fab"))

        # add model if available
        if self.path3d is not None and self.model3d is not None:
            for model in self.model3d:
                model_path = path.join(self.path3d, model)
                self.append(Model(filename=model_path, at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    def _init_cutout(self):
        self.append_tags("Cutout")
        self.append_center_rect(x=self.switch_cut_w, y=self.switch_cut_h, layer="Eco1.User", width=0.1)

    def _init_fab_outline(self):
        self.append_center_rect(layer="F.Fab")

    def _init_silkscreen(self):
        self.append_center_rect(layer="F.SilkS", offset=0.1)

    def _init_courtyard(self):
        self.append_center_rect(layer="F.CrtYd", offset=0.25)

    def _init_pcb_mount_holes(self):
        d = self.pcb_mount_hole_dia
        origin = vector(0, 0)
        offset = self.pcb_mount_hole_spacing

        self.append(SwitchMountHole(at=origin - offset, drill=d))
        self.append(SwitchMountHole(at=origin + offset, drill=d))

    def _init_center_hole(self):
        self.append(SwitchMountHole(at=[0, 0], drill=self.center_hole_dia))

    def _init_pads(self):
        self.append(
            SwitchPad(
                number=1,
                shape=Pad.SHAPE_CIRCLE,
                at=self.pin_1_pos,
                size=self.pin_dia + self.annular_ring,
                drill=self.pin_dia,
            )
        )
        self.append(
            SwitchPad(
                number=2,
                shape=Pad.SHAPE_CIRCLE,
                at=self.pin_2_pos,
                size=self.pin_dia + self.annular_ring,
                drill=self.pin_dia,
            )
        )

    def _init_switch(self):
        # Default switch init which should work for nearly any keyswitch. The
        # methods called cover each important feature/layer of a footprint, as
        # well as common switch feafures (pads, mount holes, center hole, etc).
        # Each of these methods has a default implementation in Switch that, in
        # the case of many switches, will only need to be customized by setting
        # class variables.
        self._init_fab_outline()
        self._init_silkscreen()
        self._init_courtyard()
        self._init_pads()
        self._init_center_hole()
        self._init_pcb_mount_holes()
        if self.cutout:
            self._init_cutout()

    def append_name(self, name: str):
        self.name += "_" + name.replace(" ", "_")

    def append_description(self, desc: str):
        if self.description != "":
            self.description += " "
        self.description += desc

    def append_tags(self, tags: str):
        self.tags += " " + tags

    def append_center_rect(self, layer, x=None, y=None, width=None, offset=0):
        x = x or self.switch_w
        y = y or self.switch_h

        self.append(RectLine(start=[-x / 2, -y / 2], end=[x / 2, y / 2], layer=layer, width=width, offset=offset))

    def append_component(self, component: Node):
        self.append_name(component.name)
        self.append_tags(component.tags)
        self.append_description(component.description)

        self.append(component)


class StabilizerCherryMX(Switch):
    LU_TABLE = {
        2: {"tags": ["2.00u", "2.25u", "2.50u", "2.75u"], "offset": 11.938},
        3: {"tags": ["3.00u"], "offset": 19.05},
        6: {"tags": ["6.00u"], "offset": 47.625},
        6.25: {"tags": ["6.25u"], "offset": 50},
        7: {"tags": ["7.00u"], "offset": 57.15},
        8: {"tags": ["8.00u", "9.00u", "10.00u"], "offset": 66.675},
    }

    DEFAULT_KEYS = LU_TABLE.keys()

    name = kiswitch_property(base_type=str, default="Stabilizer_Cherry_MX")
    description = kiswitch_property(base_type=str, default="Cherry MX PCB Stabilizer")
    tags = kiswitch_property(base_type=str, default="Cherry MX Keyboard Stabilizer")
    size = kiswitch_property(base_type=float, allowed_list=list(LU_TABLE.keys()))
    cutout = kiswitch_property(base_type=bool, default=True)
    text_offset = kiswitch_property(base_type=float, default=2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.append_name(f"{self.size:1.2f}u")
        self.append_description(" ".join(self.LU_TABLE[self.size]["tags"]))
        self.append_tags(" ".join(self.LU_TABLE[self.size]["tags"]))

        if self.model3d == None:
            self.model3d = [f"{self.name}.wrl"]

        self._init_base()

        if self.cutout is True:
            self._init_cutout()

    def _init_base(self):
        # set attributes
        self.setAttribute("virtual")

        # add pads
        small_hole_size = 3.048
        large_hole_size = 3.9878
        top_offset = -6.985
        bottom_offset = 8.225
        offset = self.LU_TABLE[self.size]["offset"]

        # create pads
        self.append(SwitchMountHole(at=[-offset, top_offset], drill=small_hole_size))
        self.append(SwitchMountHole(at=[offset, top_offset], drill=small_hole_size))
        self.append(SwitchMountHole(at=[-offset, bottom_offset], drill=large_hole_size))
        self.append(SwitchMountHole(at=[offset, bottom_offset], drill=large_hole_size))

        # create reference center point
        self.append(Line(start=[0, 2], end=[0, -2], layer="Dwgs.User", width=0.1))
        self.append(Line(start=[-2, 0], end=[2, 0], layer="Dwgs.User", width=0.1))

    def _init_cutout(self):
        offset = self.LU_TABLE[self.size]["offset"]

        # create cutout
        self.append(RectLine(start=[offset - 3.375, -5.53], end=[offset + 3.375, 6.77], layer="Eco1.User", width=0.1))
        self.append(RectLine(start=[-offset - 3.375, -5.53], end=[-offset + 3.375, 6.77], layer="Eco1.User", width=0.1))

        self.append_tags("Cutout")


# https://github.com/keyboardio/keyswitch_documentation/blob/master/datasheets/ALPS/SKCL.pdf
class SwitchAlpsMatias(Switch):
    DEFAULT_KEYS = [
        Keycap.KEYCAP_1U,
        Keycap.KEYCAP_1_25U,
        Keycap.KEYCAP_1_5U,
        Keycap.KEYCAP_1_75U,
        Keycap.KEYCAP_2U,
        Keycap.KEYCAP_2_25U,
        Keycap.KEYCAP_2_5U,
        Keycap.KEYCAP_2_75U,
        Keycap.KEYCAP_3U,
        Keycap.KEYCAP_4U,
        Keycap.KEYCAP_4_5U,
        Keycap.KEYCAP_5_5U,
        Keycap.KEYCAP_6U,
        Keycap.KEYCAP_6_25U,
        Keycap.KEYCAP_6_5U,
        Keycap.KEYCAP_7U,
        Keycap.KEYCAP_ISO_ENTER,
    ]

    name = kiswitch_property(base_type=str, default="SW_Alps_Matias")
    description = kiswitch_property(base_type=str, default="Alps/Matias keyswitch")
    tags = kiswitch_property(base_type=str, default="Alps Matias Keyboard Keyswitch Switch Plate")
    model3d = kiswitch_property(base_type=str, list_property=True, default=["SW_Alps_Matias.wrl"])
    cutout = kiswitch_property(base_type=bool, default=True)
    switch_w = kiswitch_property(base_type=float, default=15.5)
    switch_h = kiswitch_property(base_type=float, default=12.8)
    switch_cut_w = kiswitch_property(base_type=float, default=15.5)
    switch_cut_h = kiswitch_property(base_type=float, default=12.8)

    pin_1_pos = vector(-2.5, -4)
    pin_2_pos = vector(2.5, -4.5)
    pin_dia = 1.5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._init_switch()

    # disable default Switch features we don't use
    def _init_center_hole(self):
        pass

    def _init_pcb_mount_holes(self):
        pass


class CherryMXBase:
    CUTOUTS = ["simple", "relief", "none"]

    SWITCH_W = 14
    SWITCH_H = 14

    pcb_mount_hole_dia = 1.75
    pcb_mount_hole_spacing = vector(5.08, 0)

    pin_1_pos = vector(-3.81, -2.54)
    pin_2_pos = vector(2.54, -5.08)
    pin_dia = 1.5

    center_hole_dia = 4

    hotswap_pad_size = vector(2.55, 2.5)
    hotswap_pad_offset_1 = vector(3.275, 0)
    hotswap_pad_offset_2 = vector(3.302, 0)

    hotswap_bridge_pos_1 = vector(-6.585, -2.54)
    hotswap_bridge_pos_2 = vector(5.32, -5.08)
    hotswap_bridge_size = vector(3.55, 2.5)

    mx_relief_cutout_polyline = [
        [7, -7],
        [7, -6],
        [7.8, -6],
        [7.8, -2.9],
        [7, -2.9],
        [7, 2.9],
        [7.8, 2.9],
        [7.8, 6],
        [7, 6],
        [7, 7],
        [-7, 7],
        [-7, 6],
        [-7.8, 6],
        [-7.8, 2.9],
        [-7, 2.9],
        [-7, -2.9],
        [-7.8, -2.9],
        [-7.8, -6],
        [-7, -6],
        [-7, -7],
        [7, -7],
    ]

    def _init_relief_cutout(self):
        self.append_tags("Relief Cutout")
        self.append(PolygoneLine(polygone=self.mx_relief_cutout_polyline, layer="Eco1.User", width=0.1))

    def _init_cutout(self):
        if self.cutout == "simple":
            super()._init_cutout()
        elif self.cutout == "relief":
            self._init_relief_cutout()


# https://www.cherrymx.de/en/dev.html
class SwitchCherryMX(CherryMXBase, Switch):
    DEFAULT_KEYS = [
        Keycap.KEYCAP_1U,
        Keycap.KEYCAP_1_25U,
        Keycap.KEYCAP_1_25U_90,
        Keycap.KEYCAP_1_5U,
        Keycap.KEYCAP_1_5U_90,
        Keycap.KEYCAP_1_75U,
        Keycap.KEYCAP_1_75U_90,
        Keycap.KEYCAP_2U,
        Keycap.KEYCAP_2U_90,
        Keycap.KEYCAP_2_25U,
        Keycap.KEYCAP_2_25U_90,
        Keycap.KEYCAP_2_5U,
        Keycap.KEYCAP_2_5U_90,
        Keycap.KEYCAP_2_75U,
        Keycap.KEYCAP_2_75U_90,
        Keycap.KEYCAP_3U,
        Keycap.KEYCAP_3U_90,
        Keycap.KEYCAP_4U,
        Keycap.KEYCAP_4_5U,
        Keycap.KEYCAP_5_5U,
        Keycap.KEYCAP_6U,
        Keycap.KEYCAP_6U_OFFSET,
        Keycap.KEYCAP_6_25U,
        Keycap.KEYCAP_6_5U,
        Keycap.KEYCAP_7U,
        Keycap.KEYCAP_ISO_ENTER,
        Keycap.KEYCAP_ISO_ENTER_90,
        Keycap.KEYCAP_ISO_ENTER_180,
        Keycap.KEYCAP_ISO_ENTER_270,
    ]

    SWITCH_TYPES = ["PCB", "Plate"]

    name = kiswitch_property(base_type=str, default="SW_Cherry_MX")
    description = kiswitch_property(base_type=str, default="Cherry MX keyswitch")
    tags = kiswitch_property(base_type=str, default="Cherry MX Keyboard Keyswitch Switch")
    cutout = kiswitch_property(base_type=str, default="simple", allowed_list=CherryMXBase.CUTOUTS)
    switch_type = kiswitch_property(base_type=str, default="PCB", allowed_list=SWITCH_TYPES)
    switch_w = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_W)
    switch_h = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_H)
    switch_cut_w = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_W)
    switch_cut_h = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_H)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.append_name(self.switch_type)
        self.append_description(f"{self.switch_type} Mount")
        self.append_tags(self.switch_type)

        if self.model3d == None:
            self.model3d = [f"{self.name}.wrl"]

        self._init_switch()

    def _init_pcb_mount_holes(self):
        if self.switch_type == "PCB":
            super()._init_pcb_mount_holes()


# https://www.cherrymx.de/en/dev.html
# https://github.com/keyboardio/keyswitch_documentation/blob/master/datasheets/ALPS/SKCL.pdf
class SwitchHybridCherryMxAlps(Switch, CherryMXBase):
    DEFAULT_KEYS = SwitchAlpsMatias.DEFAULT_KEYS

    name = kiswitch_property(base_type=str, default="SW_Hybrid_Cherry_MX_Alps")
    description = kiswitch_property(base_type=str, default="Cherry MX / Alps keyswitch hybrid")
    tags = kiswitch_property(base_type=str, default="Cherry MX Alps Matias Hybrid Keyboard Keyswitch Switch PCB")
    model3d = kiswitch_property(
        base_type=str, list_property=True, default=["SW_Cherry_MX_PCB.wrl", "SW_Alps_Matias.wrl"]
    )
    cherry_w = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_W)
    cherry_h = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_H)
    alps_w = kiswitch_property(base_type=float, default=15.5)
    alps_h = kiswitch_property(base_type=float, default=12.8)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.base_polyline = [
            [-self.cherry_w / 2, -self.cherry_h / 2],
            [self.cherry_w / 2, -self.cherry_h / 2],
            [self.cherry_w / 2, -self.alps_h / 2],
            [self.alps_w / 2, -self.alps_h / 2],
            [self.alps_w / 2, self.alps_h / 2],
            [self.cherry_w / 2, self.alps_h / 2],
            [self.cherry_w / 2, self.cherry_h / 2],
            [-self.cherry_w / 2, self.cherry_h / 2],
            [-self.cherry_w / 2, self.alps_h / 2],
            [-self.alps_w / 2, self.alps_h / 2],
            [-self.alps_w / 2, -self.alps_h / 2],
            [-self.cherry_w / 2, -self.alps_h / 2],
            [-self.cherry_w / 2, -self.cherry_h / 2],
        ]

        self._init_switch()

    def _init_fab_outline(self):
        self.append(PolygoneLine(polygone=self.base_polyline, layer="F.Fab"))

    def _init_silkscreen(self):
        self.append(PolygoneLine(polygone=offset_poly(self.base_polyline, offset=0.1), layer="F.SilkS"))

    def _init_courtyard(self):
        self.append(PolygoneLine(polygone=offset_poly(self.base_polyline, offset=0.25), layer="F.CrtYd"))

    def _init_pads(self):
        self.append(
            SwitchPad(
                number=1,
                shape=Pad.SHAPE_CIRCLE,
                at=SwitchAlpsMatias.pin_1_pos,
                size=SwitchAlpsMatias.pin_dia + self.annular_ring,
                drill=SwitchAlpsMatias.pin_dia,
            )
        )
        self.append(
            SwitchPad(
                number=1,
                shape=Pad.SHAPE_OVAL,
                at=CherryMXBase.pin_1_pos,
                size=[4.46156, 2.5],
                rotation=48,
                offset=[0.980778, 0],
                drill=1.5,
            )
        )
        self.append(
            SwitchPad(
                number=2,
                shape=Pad.SHAPE_OVAL,
                at=[2.52, -4.79],
                size=[3.081378, 2.5],
                drill=[2.08137, 1.5],
                rotation=86,
            )
        )


class HotswapBase:
    hotswap_dia = 3.05
    hotswap_plated_dia = 3.6
    hotswap_th_offset = vector(0, 0)

    def _init_hotswap_th(self):
        pin_1_pos = self.pin_1_pos - self.hotswap_th_offset
        pin_2_pos = self.pin_2_pos + self.hotswap_th_offset

        if self.hotswap_plated:
            # plated th
            self.append(
                SwitchPad(
                    number=1, shape=Pad.SHAPE_CIRCLE, at=pin_1_pos, size=self.hotswap_plated_dia, drill=self.hotswap_dia
                )
            )
            self.append(
                SwitchPad(
                    number=2, shape=Pad.SHAPE_CIRCLE, at=pin_2_pos, size=self.hotswap_plated_dia, drill=self.hotswap_dia
                )
            )
        else:
            # unplated th
            self.append(SwitchMountHole(at=pin_1_pos, drill=self.hotswap_dia))
            self.append(SwitchMountHole(at=pin_2_pos, drill=self.hotswap_dia))

    def _init_hotswap_smt(self):
        pad_1_pos = self.pin_1_pos - self.hotswap_pad_offset_1
        pad_2_pos = self.pin_2_pos + self.hotswap_pad_offset_2

        if self.hotswap_plated is True:
            # not a pad, just mask cutout and paste
            self.append(
                Pad(
                    type=Pad.TYPE_SMT,
                    shape=Pad.SHAPE_ROUNDRECT,
                    at=pad_1_pos,
                    size=self.hotswap_pad_size,
                    round_radius_exact=0.25,
                    layers=["B.Mask", "B.Paste"],
                )
            )
            self.append(
                Pad(
                    type=Pad.TYPE_SMT,
                    shape=Pad.SHAPE_ROUNDRECT,
                    at=pad_2_pos,
                    size=self.hotswap_pad_size,
                    round_radius_exact=0.25,
                    layers=["B.Mask", "B.Paste"],
                )
            )
            # pad bridges between th and mask cutout
            # TODO: Use position of the smt and tht pads to calculate the hotswap_bridge_pos
            #       and hotswap_bridge_size here, and delete stored values
            self.append(
                Pad(
                    number=1,
                    type=Pad.TYPE_SMT,
                    shape=Pad.SHAPE_ROUNDRECT,
                    at=self.hotswap_bridge_pos_1,
                    size=self.hotswap_bridge_size,
                    round_radius_exact=0.25,
                    layers=["B.Cu"],
                )
            )
            self.append(
                Pad(
                    number=2,
                    type=Pad.TYPE_SMT,
                    shape=Pad.SHAPE_ROUNDRECT,
                    at=self.hotswap_bridge_pos_2,
                    size=self.hotswap_bridge_size,
                    round_radius_exact=0.25,
                    layers=["B.Cu"],
                )
            )
        else:  # non-plated hotswap
            self.append(
                Pad(
                    number=1,
                    type=Pad.TYPE_SMT,
                    shape=Pad.SHAPE_ROUNDRECT,
                    at=pad_1_pos,
                    size=self.hotswap_pad_size,
                    round_radius_exact=0.25,
                    layers=["B.Cu", "B.Mask", "B.Paste"],
                )
            )
            self.append(
                Pad(
                    number=2,
                    type=Pad.TYPE_SMT,
                    shape=Pad.SHAPE_ROUNDRECT,
                    at=pad_2_pos,
                    size=self.hotswap_pad_size,
                    round_radius_exact=0.25,
                    layers=["B.Cu", "B.Mask", "B.Paste"],
                )
            )

    def _init_pads(self):
        self._init_hotswap_th()
        self._init_hotswap_smt()


# http://www.kailh.com/en/Products/Ks/CS/
class SwitchKailhChoc(HotswapBase, Switch):
    DEFAULT_KEYS = [
        Keycap.KEYCAP_1U,
        Keycap.KEYCAP_1_25U,
        Keycap.KEYCAP_1_25U_90,
        Keycap.KEYCAP_1_5U,
        Keycap.KEYCAP_1_5U_90,
        Keycap.KEYCAP_1_75U,
        Keycap.KEYCAP_1_75U_90,
        Keycap.KEYCAP_2U,
        Keycap.KEYCAP_2U_90,
        Keycap.KEYCAP_2_25U,
        Keycap.KEYCAP_2_25U_90,
        Keycap.KEYCAP_2_5U,
        Keycap.KEYCAP_2_5U_90,
        Keycap.KEYCAP_2_75U,
        Keycap.KEYCAP_2_75U_90,
        Keycap.KEYCAP_3U,
        Keycap.KEYCAP_3U_90,
        Keycap.KEYCAP_4U,
        Keycap.KEYCAP_4_5U,
        Keycap.KEYCAP_5_5U,
        Keycap.KEYCAP_6U,
        Keycap.KEYCAP_6U_OFFSET,
        Keycap.KEYCAP_6_25U,
        Keycap.KEYCAP_6_5U,
        Keycap.KEYCAP_7U,
        Keycap.KEYCAP_ISO_ENTER,
        Keycap.KEYCAP_ISO_ENTER_90,
        Keycap.KEYCAP_ISO_ENTER_180,
        Keycap.KEYCAP_ISO_ENTER_270,
    ]

    SWITCH_TYPES = ["V1", "V2", "V1V2"]

    name = kiswitch_property(base_type=str, default="SW_Kailh_Choc")
    description = kiswitch_property(base_type=str, default="Kailh Choc keyswitch")
    tags = kiswitch_property(base_type=str, default="Kailh Choc Keyswitch Switch")
    switch_type = kiswitch_property(base_type=str, default="V1V2", allowed_list=SWITCH_TYPES)
    hotswap = kiswitch_property(base_type=bool, default=False)
    hotswap_plated = kiswitch_property(base_type=bool, default=False)
    cutout = kiswitch_property(base_type=bool, default=True)
    switch_w = kiswitch_property(base_type=float, default=15)
    switch_h = kiswitch_property(base_type=float, default=15)
    switch_cut_w = kiswitch_property(base_type=float, default=14.5)
    switch_cut_h = kiswitch_property(base_type=float, default=14.5)
    text_offset = kiswitch_property(base_type=float, default=9)

    pcb_mount_hole_dia = 1.9
    pcb_mount_hole_spacing = vector(5.5, 0)

    pin_1_pos = vector(0, -5.9)
    pin_2_pos = vector(5, -3.8)

    v2_mount_pos = vector(-5, 5.15)
    v2_mount_dia = 1.6

    pin_dia = 1.2

    # TODO: Choc Hotswap pad size and locations do not match datasheet
    hotswap_pad_size = vector(2.55, 2.5)
    hotswap_th_offset = vector(0, 0)
    hotswap_pad_offset_1 = vector(3.5, 0.1)
    hotswap_pad_offset_2 = vector(3.5, 0)

    hotswap_bridge_pos_1 = vector(-2.85, -6)
    hotswap_bridge_pos_2 = vector(7.85, -3.8)
    hotswap_bridge_size = vector(3.85, 2.5)

    polyline_base = [
        [7.275, -2.225],
        [7.575, -2.225],
        [7.575, -1.425],
        [3.567, -1.425],
        [3.276, -1.48],
        [3.025, -1.636],
        [2.848, -1.873],
        [2.769, -2.158],
        [2.612, -2.729],
        [2.258, -3.203],
        [1.756, -3.516],
        [1.175, -3.625],
        [-1.45, -3.625],
        [-2.275, -4.45],
    ]

    polyline_base2 = [
        [-2.275, -7.45],
        [-1.45, -8.275],
        [1.261, -8.275],
        [1.643, -8.199],
        [1.968, -7.982],
        [2.475, -7.475],
        [2.475, -7.275],
        [2.566, -6.816],
        [2.826, -6.426],
        [3.216, -6.166],
        [3.675, -6.075],
        [6.475, -6.075],
        [6.781, -6.014],
        [7.041, -5.841],
        [7.214, -5.581],
        [7.275, -5.275],
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # validate and record subclass local instance variables
        if self.switch_type == "V1":
            self.support_v1 = True
            self.support_v2 = False
        elif self.switch_type == "V2":
            self.support_v1 = False
            self.support_v2 = True
        else:  # self.switch_type == 'V1V2':
            self.support_v1 = True
            self.support_v2 = True

        if self.hotswap_plated is True and self.hotswap is False:
            raise ValueError("Hotswap plated switch must be hotswap.")

        # generate defaults for parent constructor
        if self.name == "SW_Kailh_Choc":
            if self.hotswap is True:
                self.name = "SW_Hotswap_Kailh_Choc"

            if self.model3d == None:
                self.model3d = [f"{self.name}_V1.wrl"]

        self.append_name(self.switch_type)
        self.append_description(self.switch_type)

        if self.support_v1:
            self.append_description("CPG1350 V1")
            self.append_tags("CPG1350 V1")

        if self.support_v2:
            self.append_description("CPG1353 V2")
            self.append_tags("CPG1353 V2")

        if self.hotswap is True:
            self.append_description("Hotswap")
            self.append_tags("Hotswap")

        if self.hotswap_plated is True:
            self.append_description("Plated")
            self.append_tags("Plated")
            self.append_name("Plated")

        if self.hotswap is True:
            self.setAttribute("smd")

        # center hole is larger on V2
        if self.support_v2:
            self.center_hole_dia = 5.05
        else:
            self.center_hole_dia = 3.45

        self._init_switch()

    def _init_fab_outline(self):
        super()._init_fab_outline()
        if self.hotswap:
            # create fab outline (socket)
            self.append(PolygoneLine(polygone=self.polyline_base, layer="B.Fab"))
            self.append(PolygoneLine(polygone=self.polyline_base2, layer="B.Fab"))

    def _init_silkscreen(self):
        super()._init_silkscreen()
        if self.hotswap:
            # create silkscreen (socket)
            self.append(PolygoneLine(polygone=offset_poly(self.polyline_base, offset=0.1), layer="B.SilkS"))
            self.append(PolygoneLine(polygone=offset_poly(self.polyline_base2, offset=0.1), layer="B.SilkS"))

    def _init_courtyard(self):
        super()._init_courtyard()
        if self.hotswap:
            # create courtyard (socket)
            polyline = self.polyline_base + self.polyline_base2
            polyline.append(polyline[0])
            self.append(PolygoneLine(polygone=offset_poly(polyline, offset=0.25), layer="B.CrtYd"))

    def _init_pads(self):
        if self.hotswap:
            HotswapBase._init_pads(self)
        else:
            Switch._init_pads(self)

    def _init_pcb_mount_holes(self):
        if self.support_v1:
            super()._init_pcb_mount_holes()
        # V2 mount hole
        if self.support_v2:
            if self.hotswap is False or self.hotswap_plated is True:
                self.append(
                    SwitchPad(
                        shape=Pad.SHAPE_CIRCLE,
                        at=self.v2_mount_pos,
                        size=self.v2_mount_dia + self.annular_ring,
                        drill=self.v2_mount_dia,
                    )
                )
            else:
                self.append(SwitchMountHole(at=self.v2_mount_pos, drill=self.v2_mount_dia))


# https://www.kailhswitch.com/mechanical-keyboard-switches/mini-keyboard-push-button-switches.html
class SwitchKailhChocMini(Switch):
    DEFAULT_KEYS = SwitchKailhChoc.DEFAULT_KEYS

    name = kiswitch_property(base_type=str, default="SW_Kailh_Choc_Mini")
    description = kiswitch_property(base_type=str, default="Kailh Choc Mini CPG1232 low profile keyswitch")
    tags = kiswitch_property(base_type=str, default="Kailh Choc Mini CPG1232 Keyboard Low Profile Keyswitch Switch")
    model3d = kiswitch_property(base_type=str, list_property=True, default=["SW_Kailh_Choc_Mini.wrl"])
    cutout = kiswitch_property(base_type=bool, default=True)
    switch_w = kiswitch_property(base_type=float, default=14.5)
    switch_h = kiswitch_property(base_type=float, default=13.5)
    switch_cut_w = kiswitch_property(base_type=float, default=13.7)
    switch_cut_h = kiswitch_property(base_type=float, default=12.7)
    text_offset = kiswitch_property(base_type=float, default=8.5)

    pin_1_pos = vector(2, 5.4)
    pin_2_pos = vector(-4.58, 5.1)
    pin_dia = 1.2
    annular_ring = 0.3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._init_switch()

    def _init_center_hole(self):
        polyline = [
            [5.95, -2.9],
            [-5.9, -2.9],
            [-5.9, 3],
            [-2.5, 3],
            [-2.5, 4.05],
            [2.05, 4.05],
            [2.05, 3],
            [5.95, 3],
            [5.95, -2.9],
        ]
        self.append(PolygoneLine(polygone=polyline, layer="Edge.Cuts", width=0.05))

    def _init_pcb_mount_holes(self):
        self.append(SwitchMountHole(shape=Pad.SHAPE_OVAL, at=[-5.29, -4.75], size=[1.2, 1.6], drill=[0.8, 1.2]))
        self.append(SwitchMountHole(shape=Pad.SHAPE_OVAL, at=[5.29, -4.75], size=[1.2, 1.6], drill=[0.8, 1.2]))


# http://www.kailh.com/en/Products/Ks/KHS
class SwitchKailhKH(Switch):
    DEFAULT_KEYS = SwitchCherryMX.DEFAULT_KEYS

    name = kiswitch_property(base_type=str, default="SW_Kailh_KH")
    description = kiswitch_property(base_type=str, default="Kailh KH CPG1280 keyswitch")
    tags = kiswitch_property(base_type=str, default="Kailh KH CPG1280 Keyboard Keyswitch Switch")
    model3d = kiswitch_property(base_type=str, list_property=True, default=["SW_Kailh_KH.wrl"])
    cutout = kiswitch_property(base_type=bool, default=True)
    switch_w = kiswitch_property(base_type=float, default=13)
    switch_h = kiswitch_property(base_type=float, default=13)
    switch_cut_w = kiswitch_property(base_type=float, default=12.2)
    switch_cut_h = kiswitch_property(base_type=float, default=12.2)

    pin_1_pos = vector(-3.8, -2.55)
    pin_2_pos = vector(3, -5.12)
    pin_dia = 1.5
    center_hole_dia = 4

    pcb_mount_hole_dia = 1.5
    pcb_mount_hole_spacing = vector(4.5, 0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._init_switch()


# http://www.kailh.com/en/Products/Ks/NotebookS/
class SwitchKailhNB(Switch):
    DEFAULT_KEYS = [
        Keycap.KEYCAP_1U,
        Keycap.KEYCAP_1_25U,
        Keycap.KEYCAP_1_5U,
        Keycap.KEYCAP_1_75U,
        Keycap.KEYCAP_2U,
        Keycap.KEYCAP_2_25U,
        Keycap.KEYCAP_2_5U,
        Keycap.KEYCAP_2_75U,
        Keycap.KEYCAP_3U,
        Keycap.KEYCAP_4U,
        Keycap.KEYCAP_4_5U,
        Keycap.KEYCAP_5_5U,
        Keycap.KEYCAP_6U,
        Keycap.KEYCAP_6_25U,
        Keycap.KEYCAP_6_5U,
        Keycap.KEYCAP_7U,
        Keycap.KEYCAP_ISO_ENTER,
    ]

    name = kiswitch_property(base_type=str, default="SW_Kailh_NB")
    description = kiswitch_property(base_type=str, default="Kailh KH CPG1425 low profile notebook keyswitch")
    tags = kiswitch_property(base_type=str, default="Kailh KH CPG1425 Keyboard Low Profile Notebook Keyswitch Switch")
    model3d = kiswitch_property(base_type=str, list_property=True, default=["SW_Kailh_NB.wrl"])
    cutout = kiswitch_property(base_type=bool, default=True)
    switch_w = kiswitch_property(base_type=float, default=14)
    switch_h = kiswitch_property(base_type=float, default=14.8)
    text_offset = kiswitch_property(base_type=float, default=8.5)
    annular_ring = kiswitch_property(base_type=float, default=0.3)

    pin_1_pos = vector(-2, -3.4)
    pin_2_pos = vector(2.9, -3.4)
    pin_dia = 1.1

    pcb_mount_hole_dia = 1.3
    pcb_mount_hole_spacing = vector(-5.5, 5.5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._init_switch()

    def _init_center_hole(self):
        self.append(RectLine(start=[1.1, -2.5], end=[-2.9, 2.5], layer="Edge.Cuts", width=0.05))


class SwitchHotswapKailh(HotswapBase, CherryMXBase, Switch):
    DEFAULT_KEYS = SwitchCherryMX.DEFAULT_KEYS

    name = kiswitch_property(base_type=str, default="SW_Hotswap_Kailh_MX")
    description = kiswitch_property(base_type=str, default="Kailh keyswitch Hotswap Socket")
    tags = kiswitch_property(base_type=str, default="Kailh Keyboard Keyswitch Switch Hotswap Socket")
    model3d = kiswitch_property(base_type=str, list_property=True, default=["SW_Hotswap_Kailh_MX.wrl"])
    cutout = kiswitch_property(base_type=str, default="relief", allowed_list=CherryMXBase.CUTOUTS)
    hotswap_plated = kiswitch_property(base_type=bool, default=False)
    switch_w = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_W)
    switch_h = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_H)
    switch_cut_w = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_W)
    switch_cut_h = kiswitch_property(base_type=float, default=CherryMXBase.SWITCH_H)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.hotswap_plated is True:
            self.append_name("Plated")
            self.append_tags("Plated")
            self.append_description("plated holes")

        self.setAttribute("smd")

        self._init_switch()

    def _init_fab_outline(self):
        super()._init_fab_outline()

        # create fab outline (socket)
        self.append(Line(start=[-4, -6.8], end=[4.8, -6.8], layer="B.Fab", width=0.12))
        self.append(Line(start=[4.8, -6.8], end=[4.8, -2.8], layer="B.Fab", width=0.12))
        self.append(Line(start=[-0.3, -2.8], end=[4.8, -2.8], layer="B.Fab", width=0.12))
        self.append(Line(start=[-6, -0.8], end=[-2.3, -0.8], layer="B.Fab", width=0.12))
        self.append(Line(start=[-6, -0.8], end=[-6, -4.8], layer="B.Fab", width=0.12))
        self.append(Arc(center=[-4, -4.8], start=[-4, -6.8], angle=-90, layer="B.Fab", width=0.12))
        self.append(Arc(center=[-0.3, -0.8], start=[-0.3, -2.8], angle=-90, layer="B.Fab", width=0.12))

    def _init_silkscreen(self):
        super()._init_silkscreen()

        # create silkscreen (socket)
        self.append(Line(start=[-4.1, -6.9], end=[1, -6.9], layer="B.SilkS", width=0.12))
        self.append(Line(start=[-0.2, -2.7], end=[4.9, -2.7], layer="B.SilkS", width=0.12))
        self.append(Arc(center=[-4.1, -4.9], start=[-4.1, -6.9], angle=-90, layer="B.SilkS", width=0.12))
        self.append(Arc(center=[-0.2, -0.7], start=[-0.2, -2.7], angle=-90, layer="B.SilkS", width=0.12))

    def _init_courtyard(self):
        super()._init_courtyard()

        # create courtyard (socket)
        # !TODO: add KLC correct offset (0.25)
        self.append(Line(start=[-4, -6.8], end=[4.8, -6.8], layer="B.CrtYd", width=0.05))
        self.append(Line(start=[4.8, -6.8], end=[4.8, -2.8], layer="B.CrtYd", width=0.05))
        self.append(Line(start=[-0.3, -2.8], end=[4.8, -2.8], layer="B.CrtYd", width=0.05))
        self.append(Line(start=[-6, -0.8], end=[-2.3, -0.8], layer="B.CrtYd", width=0.05))
        self.append(Line(start=[-6, -0.8], end=[-6, -4.8], layer="B.CrtYd", width=0.05))
        self.append(Arc(center=[-4, -4.8], start=[-4, -6.8], angle=-90, layer="B.CrtYd", width=0.05))
        self.append(Arc(center=[-0.3, -0.8], start=[-0.3, -2.8], angle=-90, layer="B.CrtYd", width=0.05))
