#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Rafael Silva <perigoso@riseup.net>

import argparse
import os

from KiSwitch.generator import render_keycaps, render_switches, SWITCHES, KEYCAPS


def generate_stabilizer(output_path):
    group = "Mounting_Keyboard_Stabilizer"
    out_path = os.path.join(output_path, f"{group}.pretty")
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    sizes = [2, 3, 6, 6.25, 7, 8]
    for size in sizes:
        render_switches(out_path, "StabilizerCherryMX", args={"size": size})


def generate_switch_alps_matias(output_path):
    group = "Switch_Keyboard_Alps_Matias"
    out_path = os.path.join(output_path, f"{group}.pretty")
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    render_switches(out_path, "SwitchAlpsMatias", keycap="Keycap")


def generate_switch_cherry_mx(output_path):
    group = "Switch_Keyboard_Cherry_MX"
    out_path = os.path.join(output_path, f"{group}.pretty")
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    for switch_type in ["PCB", "Plate"]:
        render_switches(out_path, "SwitchCherryMX", args={"switch_type": switch_type}, keycap="Keycap")


def generate_switch_hybrid(output_path):
    group = "Switch_Keyboard_Hybrid"
    out_path = os.path.join(output_path, f"{group}.pretty")
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    render_switches(out_path, "SwitchHybridCherryMxAlps", keycap="Keycap")


def generate_switch_kailh(output_path):
    group = "Switch_Keyboard_Kailh"
    out_path = os.path.join(output_path, f"{group}.pretty")
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    render_switches(out_path, "SwitchKailhChocMini", keycap="KeycapChoc")
    render_switches(out_path, "SwitchKailhKH", keycap="Keycap")
    render_switches(out_path, "SwitchKailhNB", keycap="Keycap")

    for switch_type in ["V1", "V2", "V1V2"]:
        render_switches(out_path, "SwitchKailhChoc", args={"switch_type": switch_type}, keycap="KeycapChoc")


def generate_switch_hotswap_kailh(output_path):
    group = "Switch_Keyboard_Hotswap_Kailh"
    out_path = os.path.join(output_path, f"{group}.pretty")
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    for plated in [False, True]:
        render_switches(out_path, "SwitchHotswapKailh", args={"hotswap_plated": plated}, keycap="Keycap")
        for switch_type in ["V1", "V2", "V1V2"]:
            render_switches(
                out_path,
                "SwitchKailhChoc",
                args={"switch_type": switch_type, "hotswap": True, "hotswap_plated": plated},
                keycap="KeycapChoc",
            )


if __name__ == "__main__":
    # --------------------- Parser ---------------------
    parser = argparse.ArgumentParser(description="Generate keyswitch kicad library.", usage="%(prog)s [options]")

    parser.add_argument("-o", "--output", type=str, default="./output", help="output path " "(default: %(default)s)")

    args = parser.parse_args()

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    generate_stabilizer(args.output)
    generate_switch_alps_matias(args.output)
    generate_switch_cherry_mx(args.output)
    generate_switch_hybrid(args.output)
    generate_switch_kailh(args.output)
    generate_switch_hotswap_kailh(args.output)
