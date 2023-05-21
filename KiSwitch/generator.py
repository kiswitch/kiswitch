#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

import argparse
import os
import sys
import copy

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from KiSwitch.deps_path import deps_path

from KiSwitch.keycap import Keycap, KeycapChoc

from KiSwitch.switch import (
    StabilizerCherryMX,
    SwitchAlpsMatias,
    SwitchCherryMX,
    SwitchHybridCherryMxAlps,
    SwitchKailhChoc,
    SwitchHotswapKailh,
    SwitchKailhKH,
    SwitchKailhNB,
    SwitchKailhChocMini,
)

with deps_path():
    from KicadModTree.nodes.Node import Node
    from KicadModTree.KicadFileHandler import KicadFileHandler

KEYCAPS = {
    "Keycap": Keycap,
    "KeycapChoc": KeycapChoc,
}


SWITCHES = {
    "StabilizerCherryMX": StabilizerCherryMX,
    "SwitchAlpsMatias": SwitchAlpsMatias,
    "SwitchCherryMX": SwitchCherryMX,
    "SwitchHybridCherryMxAlps": SwitchHybridCherryMxAlps,
    "SwitchKailhChoc": SwitchKailhChoc,
    "SwitchHotswapKailh": SwitchHotswapKailh,
    "SwitchKailhKH": SwitchKailhKH,
    "SwitchKailhNB": SwitchKailhNB,
    "SwitchKailhChocMini": SwitchKailhChocMini,
}


def render_switches(
    output_path: str,
    switch: str,
    args: dict = {},
    keycap: str = None,
    keycap_sizes: list[str] = None,
    keycap_args: dict = {},
) -> None:
    if switch not in SWITCHES:
        raise ValueError(f"{switch} is an invalid switch, valid switches are {SWITCHES.keys()}")

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    switch_class = SWITCHES.get(switch)

    base_switch = switch_class(**args)

    switches = list()
    switches.append(base_switch)

    if keycap is not None:
        if keycap_sizes is None or len(keycap_sizes) == 0:
            keycap_sizes = switch_class.DEFAULT_KEYS

        for keycap_node in render_keycaps(keycap, keycap_sizes, keycap_args):
            keycap_switch = copy.deepcopy(base_switch)
            keycap_switch.append_component(keycap_node)

            switches.append(keycap_switch)

    for switch_footprint in switches:
        switch_footprint.add_generic_nodes()
        file_path = os.path.join(output_path, f"{switch_footprint.name}.kicad_mod")
        file_handler = KicadFileHandler(switch_footprint)
        file_handler.writeFile(file_path, timestamp=0)


def render_keycaps(keycap: str, sizes: list[str], args: dict = {}) -> list[Node]:
    if keycap not in KEYCAPS:
        raise ValueError(f"{keycap} is an invalid keycap, valid keycaps are {KEYCAPS.keys()}")

    if sizes is None or len(sizes) == 0:
        raise ValueError(f"sizes cannot be empty")

    keycap_class = KEYCAPS.get(keycap)

    for size in sizes:
        keycap_args = copy.deepcopy(args)
        keycap_args.update(Keycap.KEYCAP_DEFAULT_SHAPES[size])

        yield keycap_class(**keycap_args)


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            setattr(namespace, self.dest, dict())
            for value in values:
                key, value = value.split("=")
                getattr(namespace, self.dest)[key] = value
        except ValueError:
            raise argparse.ArgumentError(self, f'Invalid format for kwargs {value if value else ""}')


def tui():
    # --------------------- Parser ---------------------
    parser = argparse.ArgumentParser(description="Generate keyswitch kicad library.", usage="%(prog)s [options]")

    parser.add_argument("-o", "--output", type=str, default="./output", help="output path (default: %(default)s)")

    parser.add_argument(
        "-a",
        "--switch-arg",
        type=str,
        nargs="+",
        action=ParseKwargs,
        default={},
        help="switch arguments (default: %(default)s)",
    )

    parser.add_argument("-k", "--keycap", type=str, choices=KEYCAPS.keys(), help="keycap to generate")
    parser.add_argument(
        "-z",
        "--keycap-sizes",
        type=str,
        choices=Keycap.KEYCAP_DEFAULT_SHAPES.keys(),
        nargs="+",
        help="keycap to generate",
    )
    parser.add_argument(
        "-b",
        "--keycap-arg",
        type=str,
        nargs="+",
        action=ParseKwargs,
        default={},
        help="keycap arguments (default: %(default)s)",
    )

    parser.add_argument(
        "switch",
        type=str,
        choices=SWITCHES.keys(),
        help="switch to generate",
    )

    args = parser.parse_args()

    # --------------------- Generate ---------------------
    render_switches(args.output, args.switch, args.switch_arg, args.keycap, args.keycap_sizes, args.keycap_arg)


if __name__ == "__main__":
    tui()
