# Keyswitch Kicad Library

![views](https://views.whatilearened.today/views/github/perigoso/Switch_Keyboard.svg)

This is a footprint library for [KiCad](https://www.kicad.org), a Cross Platform and Open Source EDA.

It has footprints for most popular keyboard switches.

![Banner](assets/banner.png)

```
Warning!

Versions prior to v2.1.2 have incorrect dimensions for Kailh choc V1 switches (as well as wrong name as it's actually V1 and V2 compatible), so please use the latest version if you want to use these. see issue #26.
```

## Supported footprints

|                                                                 |
|-----------------------------------------------------------------|
| Cherry MX and equivalent, Plate and PCB mount.                  |
| Alps/Matias or equivalent.                                      |
| Hybrid footprints for Cherry MX and Alps/Matias (accepts both). |
| Kailh Choc low profile switches V1 (CPG1350).                   |
| Kailh Choc low profile switches V2 (CPG1353).                   |
| Kailh Hotswap sockets for Cherry MX equivalent switches.        |
| Kailh Hotswap sockets for Choc low profile switches             |
| Kailh KH CPG1280                                                |
| Kailh CPG1425                                                   |
| Kailh Choc Mini CPG1232                                         |

If you find any issues, missing footprints or want another family of switches supported please [open an issue](https://github.com/perigoso/keyswitch-kicad-library/issues/new) about it!

## Stabilizers

Stabilizers are provided as seperate footprints in order to offer more flexibility and reduce the total number of switch footprint variants.

Currently there are footprints for Cherry MX PCB mount equivalent stabilizers in 2u 6u 6.25u 7u and 8u.

## 3D Models

The library includes the following 3d models:

|                          |
|--------------------------|
| SW_Cherry_MX_PCB         |
| SW_Cherry_MX_Plate       |
| Stabilizer_Cherry_MX     |
| SW_Hotswap_Kailh (MX)    |
| SW_Hotswap_Kailh_Choc_v1 |
| SW_Kailh_Choc_V1         |

We are looking for contributors for the missing 3d models.

## Scripts

These footprints are generated with [kicad-footprint-generator](https://gitlab.com/kicad/libraries/kicad-footprint-generator.git) with the scripts located in [scripts](scripts/).

## Using the library

As of v2.0  the library is meant to be installed via kicads `Plugin and Content Manager`, this is only available in the nightly builds of kicad (aka Kicad v6), if you are using kicad v5, please head to the [old version of this library (v1.0.0)](https://github.com/perigoso/keyswitch-kicad-library/tree/e56f74e93c850e60e04023563835b5fe031fd638)

If you want to use git simply clone this repo to the directory where you want your library stored and include them manually on your footprints table `Preferences -> Manage Footprint Libraries...` (Note: with this method the 3d models will not be linked automatically/correctly)

If you want to use the RECOMMENDED method, open the content manager, where you will find this library in the libraries tab (you can also download the arquive from the releases and `install from file...`) Note that you need to add the libraries to the library table manually.

The following entries needs to be added:

Name | Location
---|---
Mounting_Keyboard_Stabilizer | ${KICAD6_3RD_PARTY}/footprints/com_github_perigoso_keyswitch-kicad-library/Mounting_Keyboard_Stabilizer.pretty
Switch_Keyboard_Alps_Matias | ${KICAD6_3RD_PARTY}/footprints/com_github_perigoso_keyswitch-kicad-library/Switch_Keyboard_Alps_Matias.pretty
Switch_Keyboard_Cherry_MX | ${KICAD6_3RD_PARTY}/footprints/com_github_perigoso_keyswitch-kicad-library/Switch_Keyboard_Cherry_MX.pretty
Switch_Keyboard_Hotswap_Kailh | ${KICAD6_3RD_PARTY}/footprints/com_github_perigoso_keyswitch-kicad-library/Switch_Keyboard_Hotswap_Kailh.pretty
Switch_Keyboard_Hybrid | ${KICAD6_3RD_PARTY}/footprints/com_github_perigoso_keyswitch-kicad-library/Switch_Keyboard_Hybrid.pretty
Switch_Keyboard_Kailh | ${KICAD6_3RD_PARTY}/footprints/com_github_perigoso_keyswitch-kicad-library/Switch_Keyboard_Kailh.pretty

## Screenshots

All screenshots are of the 1u keycap switch.

`Warning: some footprints are missing or may have changed, this is out of date`

![cherrymx_plate](https://user-images.githubusercontent.com/39195157/93152763-7811aa00-f6f7-11ea-83d1-0b2d516927cc.png)
![cherrymx_pcb](https://user-images.githubusercontent.com/39195157/93150026-f66a4e00-f6ef-11ea-809f-2e3a8dbe188a.png)
![alps_matias](https://user-images.githubusercontent.com/39195157/93150084-1c8fee00-f6f0-11ea-97b3-24e5e425479f.png)
![hybrids](https://user-images.githubusercontent.com/39195157/93150167-55c85e00-f6f0-11ea-9cce-6adc237570d0.png)
![kailh_Choc](https://user-images.githubusercontent.com/39195157/93150222-72649600-f6f0-11ea-8a22-b62f093f4c2d.png)
![kailh_hotswap](https://user-images.githubusercontent.com/39195157/93150276-8f996480-f6f0-11ea-9919-c952159f183f.png)

Demo board for real life testing

![demo](https://user-images.githubusercontent.com/39195157/158739962-f45acbd3-4a3d-4613-8eca-4cfa36f55d0c.png)

## Source

If you're reading this from outside GitHub, you can find the source for this library [here](https://github.com/perigoso/keyswitch-kicad-library):

`https://github.com/perigoso/keyswitch-kicad-library`

## Contribuitors and Acknowledgements

- [Rafael Silva (perigoso)](https://github.com/perigoso) - Author and maintainer
- [Jesse Vincent (obra)](https://github.com/obra) - Production tested footprints and others from [keyboardio](https://github.com/keyboardio)
- [Lotier](https://github.com/Lotier) - Wrote the script for automating the generation of stabilizers
- [ai03](https://github.com/ai03-2725) - Original library that served as motivation and baseline

## License

The library is dual licensed under [MIT](LICENSE-MIT) and [CC-BY-4.0](LICENSE-CC-BY).
