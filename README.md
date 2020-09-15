# KiCad Keyboard Switch Footprint Libraries

This repository contains libraries for various keyboard switches, these libraries are being merged to the official KiCad libraries [here](https://github.com/KiCad/kicad-footprints/issues/2416).

In the meantime, this being a large commit that will take time to approve, I decided to provide them as an independent library in order for the community to use, test, and give feedback.

## Supported footprints

- Cherry MX or equivalent, Plate and PCB mount.
- Alps/Matias or equivalent.
- Hybrid footprints for Cherry MX and Alps/Matias (accepts both).
- Kailh Choc low profile switches (version 1).
- Kailh Hotswap sockets for Cherry MX equivalent switches.

If you find any footprints missing or want another family of switches supported `please` open an issue about it!

## Stabilizers

Stabilizers are provided as seperate packages in order to offer more flexibility and reduce the total number of footprints.

Currently there are only footprints for Cherry MX PCB mount equivalent Stabilizers in 2u 6u 6.25u and 7u.

## Screenshots

All screenshots are of the 1u keycap switch.

![cherrymx_plate](https://user-images.githubusercontent.com/39195157/93152763-7811aa00-f6f7-11ea-83d1-0b2d516927cc.png)
![cherrymx_pcb](https://user-images.githubusercontent.com/39195157/93150026-f66a4e00-f6ef-11ea-809f-2e3a8dbe188a.png)
![alps_matias](https://user-images.githubusercontent.com/39195157/93150084-1c8fee00-f6f0-11ea-97b3-24e5e425479f.png)
![hybrids](https://user-images.githubusercontent.com/39195157/93150167-55c85e00-f6f0-11ea-9cce-6adc237570d0.png)
![kailh_Choc](https://user-images.githubusercontent.com/39195157/93150222-72649600-f6f0-11ea-8a22-b62f093f4c2d.png)
![kailh_hotswap](https://user-images.githubusercontent.com/39195157/93150276-8f996480-f6f0-11ea-9919-c952159f183f.png)

## Generators

These footprints are generated with [scripts](https://github.com/perigoso/kicad-footprint-generator/tree/keyboard_switch_scripts/scripts/Keyboard_Switches).

## Contribuitors and Acknowledgements

- [perigoso](https://github.com/perigoso) - All footprints included here and corresponding scripts
- [ai03](https://github.com/ai03-2725) - Baseline for all footprints included here
