import argparse
import os

from KicadModTree.KicadFileHandler import KicadFileHandler

from keycap import Keycap

from switch import StabilizerCherryMX, SwitchAlpsMatias, SwitchCherryMX, \
                   SwitchHybridCherryMxAlps, SwitchKailhChocV1, \
                   SwitchHotswapKailh, SwitchHotswapKailhChocV1, SwitchKailhKH, \
                   SwitchKailhNB, SwitchKailhChocMini

path3d = '${KICAD6_3RD_PARTY}/3dmodels/' \
         'com_github_perigoso_keyswitch-kicad-library/' \
         '3d-library.3dshapes/'

keycaps = {
    '1u': {'keycap_type': 'regular', 'width': 1},
    '1.25u': {'keycap_type': 'regular', 'width': 1.25},
    '1.25u90': {'keycap_type': 'regular', 'width': 1.25, 'rotation': 90},
    '1.5u': {'keycap_type': 'regular', 'width': 1.5},
    '1.5u90': {'keycap_type': 'regular', 'width': 1.5, 'rotation': 90},
    '1.75u': {'keycap_type': 'regular', 'width': 1.75},
    '1.75u90': {'keycap_type': 'regular', 'width': 1.75, 'rotation': 90},
    '2u': {'keycap_type': 'regular', 'width': 2},
    '2u90': {'keycap_type': 'regular', 'width': 2, 'rotation': 90},
    '2.25u': {'keycap_type': 'regular', 'width': 2.25},
    '2.25u90': {'keycap_type': 'regular', 'width': 2.25, 'rotation': 90},
    '2.5u': {'keycap_type': 'regular', 'width': 2.5},
    '2.5u90': {'keycap_type': 'regular', 'width': 2.5, 'rotation': 90},
    '2.75u': {'keycap_type': 'regular', 'width': 2.75},
    '2.75u90': {'keycap_type': 'regular', 'width': 2.75, 'rotation': 90},
    '3u': {'keycap_type': 'regular', 'width': 3},
    '3u90': {'keycap_type': 'regular', 'width': 3, 'rotation': 90},
    '4u': {'keycap_type': 'regular', 'width': 4},
    '4.5u': {'keycap_type': 'regular', 'width': 4.5},
    '5.5u': {'keycap_type': 'regular', 'width': 5.5},
    '6u': {'keycap_type': 'regular', 'width': 6},
    '6uOffset': {'keycap_type': 'regular', 'width': 6, 'x_offset': -9.525},
    '6.25u': {'keycap_type': 'regular', 'width': 6.25},
    '6.5u': {'keycap_type': 'regular', 'width': 6.5},
    '7u': {'keycap_type': 'regular', 'width': 7},
    'ISOEnter': {'keycap_type': 'ISOEnter'},
    'ISOEnter90': {'keycap_type': 'ISOEnter', 'rotation': 90},
    'ISOEnter180': {'keycap_type': 'ISOEnter', 'rotation': 180},
    'ISOEnter270': {'keycap_type': 'ISOEnter', 'rotation': 270}
}


def generate_stabilizer_cherry_mx(output_path):
    group = 'Mounting_Keyboard_Stabilizer'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    sizes = [2, 3, 6, 6.25, 7, 8]
    for size in sizes:
        stab = StabilizerCherryMX(size=size, path3d=path3d)
        file_handler = KicadFileHandler(stab)
        file_handler.writeFile(os.path.join(out_path, f'{stab.name}.kicad_mod'), timestamp=0)


def generate_switch_alps_matias(output_path):
    spacing = 19.05
    group = 'Switch_Keyboard_Alps_Matias'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.5u', '1.75u', '2u', '2.25u', '2.5u', '2.75u',
            '3u', '4u', '4.5u', '5.5u', '6u', '6.25u', '6.5u', '7u',
            'ISOEnter']

    switches = []

    switches.append(SwitchAlpsMatias(path3d=path3d))

    for key in keys:
        switches.append(SwitchAlpsMatias(path3d=path3d,
                                         keycap=Keycap(spacing=spacing,
                                                       **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


def generate_switch_cherry_mx(output_path):
    spacing = 19.05
    group = 'Switch_Keyboard_Cherry_MX'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.25u90', '1.5u', '1.5u90', '1.75u', '1.75u90',
            '2u', '2u90', '2.25u', '2.25u90', '2.5u', '2.5u90', '2.75u',
            '2.75u90', '3u', '3u90', '4u', '4.5u', '5.5u', '6u', '6uOffset',
            '6.25u', '6.5u', '7u', 'ISOEnter', 'ISOEnter90', 'ISOEnter180',
            'ISOEnter270']

    switches = []

    for switch_type in ['PCB', 'Plate']:
        switches.append(SwitchCherryMX(switch_type=switch_type, path3d=path3d))

        for key in keys:
            switches.append(SwitchCherryMX(switch_type=switch_type,
                                           path3d=path3d,
                                           keycap=Keycap(spacing=spacing,
                                                         **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


def generate_switch_hybrid_cherry_mx_alps(output_path):
    spacing = 19.05
    group = 'Switch_Keyboard_Hybrid'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.5u', '1.75u', '2u', '2.25u', '2.5u', '2.75u',
            '3u', '4u', '4.5u', '5.5u', '6u', '6.25u', '6.5u', '7u',
            'ISOEnter']

    switches = []

    switches.append(SwitchHybridCherryMxAlps(path3d=path3d))

    for key in keys:
        switches.append(
            SwitchHybridCherryMxAlps(path3d=path3d,
                                     keycap=Keycap(spacing=spacing,
                                                   **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


def generate_switch_kailh_choc_v1(output_path):
    x_spacing = 18
    y_spacing = 17
    group = 'Switch_Keyboard_Kailh'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.25u90', '1.5u', '1.5u90', '1.75u', '1.75u90',
            '2u', '2u90', '2.25u', '2.25u90', '2.5u', '2.5u90', '2.75u',
            '2.75u90', '3u', '3u90', '4u', '4.5u', '5.5u', '6u', '6uOffset',
            '6.25u', '6.5u', '7u', 'ISOEnter', 'ISOEnter90', 'ISOEnter180',
            'ISOEnter270']

    switches = []

    switches.append(SwitchKailhChocV1(path3d=path3d))

    for key in keys:
        switches.append(SwitchKailhChocV1(path3d=path3d,
                                          keycap=Keycap(x_spacing=x_spacing,
                                                        y_spacing=y_spacing,
                                                        **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


def generate_switch_kailh_choc_mini(output_path):
    x_spacing = 18
    y_spacing = 17
    group = 'Switch_Keyboard_Kailh'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.25u90', '1.5u', '1.5u90', '1.75u', '1.75u90',
            '2u', '2u90', '2.25u', '2.25u90', '2.5u', '2.5u90', '2.75u',
            '2.75u90', '3u', '3u90', '4u', '4.5u', '5.5u', '6u', '6uOffset',
            '6.25u', '6.5u', '7u', 'ISOEnter', 'ISOEnter90', 'ISOEnter180',
            'ISOEnter270']

    switches = []

    switches.append(SwitchKailhChocMini(path3d=path3d))

    for key in keys:
        switches.append(SwitchKailhChocMini(path3d=path3d,
                                          keycap=Keycap(x_spacing=x_spacing,
                                                        y_spacing=y_spacing,
                                                        **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


def generate_switch_kailh_kh(output_path):
    spacing = 19.05
    group = 'Switch_Keyboard_Kailh'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.25u90', '1.5u', '1.5u90', '1.75u', '1.75u90',
            '2u', '2u90', '2.25u', '2.25u90', '2.5u', '2.5u90', '2.75u',
            '2.75u90', '3u', '3u90', '4u', '4.5u', '5.5u', '6u', '6uOffset',
            '6.25u', '6.5u', '7u', 'ISOEnter', 'ISOEnter90', 'ISOEnter180',
            'ISOEnter270']

    switches = []

    switches.append(SwitchKailhKH(path3d=path3d))

    for key in keys:
        switches.append(SwitchKailhKH(path3d=path3d,
                                      keycap=Keycap(spacing=spacing,
                                                    **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


def generate_switch_kailh_nb(output_path):
    spacing = 19.05
    group = 'Switch_Keyboard_Kailh'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.5u', '1.75u', '2u', '2.25u', '2.5u', '2.75u',
            '3u', '4u', '4.5u', '5.5u', '6u', '6.25u', '6.5u', '7u',
            'ISOEnter']

    switches = []

    switches.append(SwitchKailhNB(path3d=path3d))

    for key in keys:
        switches.append(SwitchKailhNB(path3d=path3d,
                                      keycap=Keycap(spacing=spacing,
                                                    **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


def generate_switch_hotswap_kailh(output_path):
    spacing = 19.05
    group = 'Switch_Keyboard_Hotswap_Kailh'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.25u90', '1.5u', '1.5u90', '1.75u', '1.75u90',
            '2u', '2u90', '2.25u', '2.25u90', '2.5u', '2.5u90', '2.75u',
            '2.75u90', '3u', '3u90', '4u', '4.5u', '5.5u', '6u', '6uOffset',
            '6.25u', '6.5u', '7u', 'ISOEnter', 'ISOEnter90', 'ISOEnter180',
            'ISOEnter270']

    switches = []

    for plated in [False, True]:

        switches.append(SwitchHotswapKailh(path3d=path3d, plated_th=plated))

        for key in keys:
            switches.append(SwitchHotswapKailh(path3d=path3d,
                                               plated_th=plated,
                                               keycap=Keycap(spacing=spacing,
                                                             **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


def generate_switch_hotswap_kailh_choc_v1(output_path):
    x_spacing = 18
    y_spacing = 17
    group = 'Switch_Keyboard_Hotswap_Kailh'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.25u90', '1.5u', '1.5u90', '1.75u', '1.75u90',
            '2u', '2u90', '2.25u', '2.25u90', '2.5u', '2.5u90', '2.75u',
            '2.75u90', '3u', '3u90', '4u', '4.5u', '5.5u', '6u', '6uOffset',
            '6.25u', '6.5u', '7u', 'ISOEnter', 'ISOEnter90', 'ISOEnter180',
            'ISOEnter270']

    switches = []

    for plated in [False, True]:

        switches.append(SwitchHotswapKailhChocV1(path3d=path3d, plated_th=plated))

        for key in keys:
            switches.append(SwitchHotswapKailhChocV1(path3d=path3d,
                                                     plated_th=plated,
                                                     keycap=Keycap(x_spacing=x_spacing,
                                                                   y_spacing=y_spacing,
                                                                   **keycaps[key])))

        for switch in switches:
            file_handler = KicadFileHandler(switch)
            file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


if __name__ == '__main__':
    # --------------------- Parser ---------------------
    parser = argparse.ArgumentParser(
        description='Generate keyswitch kicad library.',
        usage='%(prog)s [options]')

    parser.add_argument('-o', '--output',
                        type=str, default='./output',
                        help='output path '
                             '(default: %(default)s)')

    args = parser.parse_args()

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    generate_stabilizer_cherry_mx(args.output)
    generate_switch_alps_matias(args.output)
    generate_switch_cherry_mx(args.output)
    generate_switch_hybrid_cherry_mx_alps(args.output)
    generate_switch_kailh_choc_v1(args.output)
    generate_switch_kailh_choc_mini(args.output)
    generate_switch_kailh_kh(args.output)
    generate_switch_kailh_nb(args.output)
    generate_switch_hotswap_kailh(args.output)
    generate_switch_hotswap_kailh_choc_v1(args.output)
