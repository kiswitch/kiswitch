# KiCad Keyboard Switch Footprint Libraries

This repository contains libraries for various keyboard switches, these libraries are being merged to the official KiCad libraries [here](https://github.com/KiCad/kicad-footprints/issues/2416).

In the meantime, this being a large commit that will take time to approve, I decided to provide them as an independent library in order for the community to use, test, and give feedback.

## Supported footprints

- Cherry MX or equivalent, Plate and PCB mount.
- Alps/Matias or equivalent.
- Hybrid footprints for Cherry MX and Alps/Matias (accepts both).
- Kailh Choc low profile switches (version 1).
- Kailh Hotswap sockets for Cherry MX equivalent switches.

If you find any issues, missing footprints or want another family of switches supported please [open an issue](https://github.com/perigoso/keyswitch-kicad-library/issues/new) about it!

## Stabilizers

Stabilizers are provided as seperate footprints in order to offer more flexibility and reduce the total number of switch footprints.

Currently there are only footprints for Cherry MX PCB mount equivalent Stabilizers in 2u 6u 6.25u 7u and 8u.

## 3D Models

The library includes 3d models for the following:

- Cherry MX plate mount switches.
- Cherry MX PCB mount switches.
- Cherry MX Stabilizers.
- Kailh hotswap sockets.
- Kailh Choc V1 switches.

We are looking for contributors for the missing 3d models.

These are located in the [packages3d](modules/packages3d/) directory.

They are linked based on the `KEYSWITCH_LIB_3D` enviorenment variable, this needs to be set by the user and should point to the `packages3d` directory of the library, this variable can be set by going to `Preferences -> Configure Path` and clicking od the plus sign button, name it `KEYSWITCH_LIB_3D` and navigate to the directory the 3d files are at (`packages3d`).

## Scripts

These footprints are generated with [kicad-footprint-generator](https://gitlab.com/kicad/libraries/kicad-footprint-generator.git) with the scripts located in [scripts](scripts/).

## Using the library

If you have access to git simply clone this repo to the directory where you want your library stored and include them manually on your footprints table `Preferences -> Manage Footprint Libraries... -> Project Specific Libraries (folder icon)` 

If you don't have access to git simply download the release (right `Releases`) and extract to the directory where you want your library stored and include them manually on your footprints table `Preferences -> Manage Footprint Libraries... -> Project Specific Libraries (folder icon)`

## Screenshots

All screenshots are of the 1u keycap switch.

![cherrymx_plate](https://user-images.githubusercontent.com/39195157/93152763-7811aa00-f6f7-11ea-83d1-0b2d516927cc.png)
![cherrymx_pcb](https://user-images.githubusercontent.com/39195157/93150026-f66a4e00-f6ef-11ea-809f-2e3a8dbe188a.png)
![alps_matias](https://user-images.githubusercontent.com/39195157/93150084-1c8fee00-f6f0-11ea-97b3-24e5e425479f.png)
![hybrids](https://user-images.githubusercontent.com/39195157/93150167-55c85e00-f6f0-11ea-9cce-6adc237570d0.png)
![kailh_Choc](https://user-images.githubusercontent.com/39195157/93150222-72649600-f6f0-11ea-8a22-b62f093f4c2d.png)
![kailh_hotswap](https://user-images.githubusercontent.com/39195157/93150276-8f996480-f6f0-11ea-9919-c952159f183f.png)

## Source

If you're reading this from outside GitHub, you can find the source for this library [here](https://github.com/perigoso/keyswitch-kicad-library):

`https://github.com/perigoso/keyswitch-kicad-library`

## Contribuitors and Acknowledgements

- [perigoso](https://github.com/perigoso) - All footprints included here and corresponding scripts
- [ai03](https://github.com/ai03-2725) - Rough baseline for some footprints

![views](https://views.whatilearened.today/views/github/perigoso/Switch_Keyboard.svg)
