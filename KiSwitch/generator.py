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
    from KicadModTree.KicadFileHandler import KicadFileHandler

KEYCAPS = [Keycap, KeycapChoc]

SWITCHES = [
    StabilizerCherryMX,
    SwitchAlpsMatias,
    SwitchCherryMX,
    SwitchHybridCherryMxAlps,
    SwitchKailhChoc,
    SwitchHotswapKailh,
    SwitchKailhKH,
    SwitchKailhNB,
    SwitchKailhChocMini,
]


def render_switches(output_path, switches):
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    for switch in switches:
        file_path = os.path.join(output_path, f"{switch.name}.kicad_mod")
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(file_path, timestamp=0)


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
        "-s",
        "--switch",
        type=str,
        choices=[switch.__name__ for switch in SWITCHES],
        required=True,
        help="switch to generate",
    )
    parser.add_argument(
        "-a",
        "--switch-arg",
        type=str,
        nargs="+",
        action=ParseKwargs,
        default={},
        help="switch arguments (default: %(default)s)",
    )

    parser.add_argument(
        "-k", "--keycap", type=str, choices=[keycap.__name__ for keycap in KEYCAPS], help="keycap to generate"
    )
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

    args = parser.parse_args()

    switch_class = eval(args.switch)

    switch_queue = []

    switch = switch_class(**args.switch_arg)
    switch_queue.append(switch)

    if args.keycap is not None:
        if args.keycap_sizes is None:
            keycap_sizes = switch_class.DEFAULT_KEYS
        else:
            keycap_sizes = args.keycap_sizes

        keycap_class = eval(args.keycap)

        for keycap_size in keycap_sizes:
            keycap_args = args.keycap_arg
            keycap_args.update(keycap_class.KEYCAP_DEFAULT_SHAPES[keycap_size])

            keycap_switch = copy.deepcopy(switch)

            keycap = keycap_class(**keycap_args)

            keycap_switch.append_component(keycap)

            switch_queue.append(keycap_switch)

    render_switches(args.output, switch_queue)


if __name__ == "__main__":
    tui()
