#!/usr/bin/env python3

# Generator for Cherry Mx PCB mount stabilizers

import sys
import os
import pathlib

sys.path.append(os.path.join(sys.path[0], "kicad-footprint-generator"))  # load parent path of KicadModTree

from KicadModTree import *

group_name = "Mounting_Keyboard_Stabilizer"
assetPath = os.path.join(pathlib.Path(sys.path[0]).parent, "library", "footprints", "{}.pretty/".format(group_name))
base_name = "Stabilizer_Cherry_MX"
base_tags = "Cherry MX Keyboard Stabilizer"
base_description = "Cherry MX PCB Stabilizer"
sized_description = {
	2   : "2u 2.25u 2.5u 2.75u",
	3   : "3u",
	6   : "6u",
	6.25: "6.25u",
	7   : "7u",
	8   : "8u 9u 10u"
}
offsets = {
	2   : 11.938,
	3   : 19.05,
	6   : 47.625,
	6.25: 50,
	7   : 57.15,
	8   : 66.675
}
small_hole_size = 3.048
large_hole_size = 3.9878
top_offset = -6.985
bottom_offset = 8.225

def generate_stabilizer(footprint_name, footprint_description, footprint_tags, stabilizer_size):
	location_3d = "${KICAD6_3RD_PARTY}/3dmodels/com_github_perigoso_keyswitch-kicad-library/3d-library.3dshapes/" + footprint_name + ".wrl"

	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	kicad_mod.setDescription(footprint_description)
	kicad_mod.setTags(footprint_tags)

	kicad_mod.setAttribute('virtual')

	# set general values
	kicad_mod.append(Text(type='reference', text='REF**', at=[0,-3], layer='F.SilkS'))
	kicad_mod.append(Text(type='value', text=footprint_name, at=[0,3.2], layer='F.Fab'))
	kicad_mod.append(Text(type='user', text='REF**', at=[0,0], layer='F.Fab'))

	# create pads
	offset = offsets.get(stabilizer_size)

	kicad_mod.append(Pad(number="~", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[-offset,top_offset], size=[small_hole_size,small_hole_size], drill=small_hole_size, layers=['*.Cu','*.Mask']))
	kicad_mod.append(Pad(number="~", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[offset,top_offset], size=[small_hole_size,small_hole_size], drill=small_hole_size, layers=['*.Cu','*.Mask']))
	kicad_mod.append(Pad(number="~", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[-offset,bottom_offset], size=[large_hole_size,large_hole_size], drill=large_hole_size, layers=['*.Cu','*.Mask']))
	kicad_mod.append(Pad(number="~", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[offset,bottom_offset], size=[large_hole_size,large_hole_size], drill=large_hole_size, layers=['*.Cu','*.Mask']))

	# create cutout
	kicad_mod.append(RectLine(
		start=[offset - 3.375, -5.53],
		end=[offset + 3.375 , 6.77], 
		layer='Eco1.User', 
		width=0.1
	))
	kicad_mod.append(RectLine(
		start=[-offset - 3.375, -5.53],
		end=[-offset + 3.375 , 6.77], 
		layer='Eco1.User', 
		width=0.1
	))

	# create reference center point
	kicad_mod.append(Line(start=[0,2], end=[0,-2], layer='Dwgs.User', width=0.1))
	kicad_mod.append(Line(start=[-2,0], end=[2,0], layer='Dwgs.User', width=0.1))

	# add model
	kicad_mod.append(Model(filename=location_3d ,at=[0,0,0] ,scale=[1,1,1] ,rotate=[0,0,0]))

	return kicad_mod

def generate_stabilizer_footprint(unit_size):

	footprint_name = "{}_{}u".format(base_name, unit_size)
	footprint_description = "{} {}".format(base_description, sized_description.get(unit_size))
	footprint_tags = "{} {}".format(base_tags, sized_description.get(unit_size))

	kicad_mod = generate_stabilizer(footprint_name, footprint_description, footprint_tags, unit_size)

	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile(assetPath + "{}.kicad_mod".format(footprint_name))


if __name__ == "__main__":

	for stabilizer_size in [2, 3, 6, 6.25, 7, 8]:
		generate_stabilizer_footprint(stabilizer_size)
