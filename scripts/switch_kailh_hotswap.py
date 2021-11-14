#!/usr/bin/env python3

# Generator for Kailh keyboard switch hotswap socket

import sys
import os

# sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "kicad-footprint-generator"))  # load parent path of KicadModTree

import argparse
import yaml
import math

from KicadModTree import *

base_name = "SW_Hotswap_Kailh"
base_tags = "Kailh Keyboard Keyswitch Switch Hotswap Socket"
base_description = "Kailh keyswitch Hotswap Socket, "

# location_3d = "${KISYS3DMOD}/Switch_Keyboard_Kailh.3dshapes/" + base_name + ".wrl"
location_3d = "${KEYSWITCH_LIB_3D}/Switch_Keyboard_Kailh.3dshapes/" + base_name + ".wrl"

unit_value = 19.05

kailh_hs_w = 14
kailh_hs_h = 14

def generate_switch(footprint_name, footprint_description, footprint_tags):
	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	kicad_mod.setDescription(footprint_description)
	kicad_mod.setTags(footprint_tags)
	kicad_mod.setAttribute('smd')

	# set general values
	kicad_mod.append(Text(type='reference', text='REF**', at=[0,-8], mirror=True, layer='B.SilkS'))
	kicad_mod.append(Text(type='value', text=footprint_name, at=[0,0], mirror=True, layer='B.Fab'))
	kicad_mod.append(Text(type='user', text='%R', at=[0,-4.75], mirror=True, layer='B.Fab'))

	# create fab outline (keyswitch)
	kicad_mod.append(RectLine(start=[-kailh_hs_w/2,-kailh_hs_h/2], end=[kailh_hs_w/2,kailh_hs_h/2], layer='F.Fab', width=0.1))

	# create fab outline (socket)
	kicad_mod.append(Line(start=[-4,-6.8], end=[4.8,-6.8], layer='B.Fab', width=0.12))
	kicad_mod.append(Line(start=[4.8,-6.8], end=[4.8,-2.8], layer='B.Fab', width=0.12))
	kicad_mod.append(Line(start=[-0.3,-2.8], end=[4.8,-2.8], layer='B.Fab', width=0.12))
	kicad_mod.append(Line(start=[-6,-0.8], end=[-2.3,-0.8], layer='B.Fab', width=0.12))
	kicad_mod.append(Line(start=[-6,-0.8], end=[-6,-4.8], layer='B.Fab', width=0.12))
	kicad_mod.append(Arc(center=[-4,-4.8], start=[-4,-6.8], angle=-90, layer='B.Fab', width=0.12))
	kicad_mod.append(Arc(center=[-0.3,-0.8], start=[-0.3,-2.8], angle=-90, layer='B.Fab', width=0.12))

	# create silscreen (keyswitch)
	kicad_mod.append(RectLine(start=[-kailh_hs_w/2,-kailh_hs_h/2], end=[kailh_hs_w/2,kailh_hs_h/2], layer='F.SilkS', width=0.12, offset=0.1))

	# create silscreen (socket)
	kicad_mod.append(Line(start=[-4.1,-6.9], end=[1,-6.9], layer='B.SilkS', width=0.12))
	kicad_mod.append(Line(start=[-0.2,-2.7], end=[4.9,-2.7], layer='B.SilkS', width=0.12))
	kicad_mod.append(Arc(center=[-4.1,-4.9], start=[-4.1,-6.9], angle=-90, layer='B.SilkS', width=0.12))
	kicad_mod.append(Arc(center=[-0.2,-0.7], start=[-0.2,-2.7], angle=-90, layer='B.SilkS', width=0.12))

	# create courtyard (keyswitch)
	kicad_mod.append(RectLine(start=[-kailh_hs_w/2,-kailh_hs_h/2], end=[kailh_hs_w/2,kailh_hs_h/2], layer='F.CrtYd', width=0.05, offset=0.25))

	# create courtyard (socket)
	kicad_mod.append(RectLine(start=[-8.61,-7.05], end=[7.37,-0.55], layer='B.CrtYd', width=0.05))

	# create pads
	kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[-3.81,-2.54], size=[3,3], drill=3, layers=['*.Cu', '*.Mask']))
	kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[2.54,-5.08], size=[3,3], drill=3, layers=['*.Cu', '*.Mask']))
	kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[0,0], size=[4,4], drill=4, layers=['*.Cu', '*.Mask']))
	kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[-5.08,0], size=[1.75,1.75], drill=1.75, layers=['*.Cu', '*.Mask']))
	kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[5.08,0], size=[1.75,1.75], drill=1.75, layers=['*.Cu', '*.Mask']))

	kicad_mod.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[-7.085,-2.54], size=[2.55,2.5], layers=['B.Cu', 'B.Mask', 'B.Paste']))
	kicad_mod.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[5.842,-5.08], size=[2.55,2.5], layers=['B.Cu', 'B.Mask', 'B.Paste']))

	# add model
	kicad_mod.append(Model(filename=location_3d ,at=[0,0,0] ,scale=[1,1,1] ,rotate=[0,0,0]))

	return kicad_mod

def generate_switch_footprint():
	kicad_mod = generate_switch(base_name, base_description, base_tags)
	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile("{}.kicad_mod".format(base_name))

def generate_isoenter_key_footprint(orientation):
	footprint_name = ""

	if orientation == 0:
		footprint_name = "{}_ISOEnter".format(base_name)
	elif orientation == 1:
		footprint_name = "{}_ISOEnter_Rotated90".format(base_name)
	elif orientation == 2:
		footprint_name = "{}_ISOEnter_Rotated180".format(base_name)
	elif orientation == 3:
		footprint_name = "{}_ISOEnter_Rotated270".format(base_name)

	footprint_description = base_description
	footprint_tags = base_tags + " ISOEnter"

	kicad_mod = generate_switch(footprint_name, footprint_description, footprint_tags)

	if orientation == 0: # normal orientation
		polygone_line = [[(unit_value*1.25)/2, unit_value],
					 	 [(unit_value*1.25)/2, -unit_value],
					 	 [-(unit_value*1.75)/2, -unit_value],
					 	 [-(unit_value*1.75)/2, 0],
					 	 [-(unit_value*1.25)/2, 0],
						 [-(unit_value*1.25)/2, unit_value],
						 [(unit_value*1.25)/2, unit_value]]
	elif orientation == 1: # rotated 90 deg
		polygone_line = [[unit_value, -(unit_value*1.25)/2],
					 	 [-unit_value, -(unit_value*1.25)/2],
					 	 [-unit_value, (unit_value*1.75)/2],
					 	 [0, (unit_value*1.75)/2],
					 	 [0, (unit_value*1.25)/2],
						 [unit_value, (unit_value*1.25)/2],
						 [unit_value, -(unit_value*1.25)/2]]
	elif orientation == 2: # rotated 180 deg
		polygone_line = [[-(unit_value*1.25)/2, -unit_value],
					 	 [-(unit_value*1.25)/2, unit_value],
					 	 [(unit_value*1.75)/2, unit_value],
					 	 [(unit_value*1.75)/2, 0],
					 	 [(unit_value*1.25)/2, 0],
						 [(unit_value*1.25)/2, -unit_value],
						 [-(unit_value*1.25)/2, -unit_value]]
	elif orientation == 3: # rotated 270 deg
		polygone_line = [[-unit_value, (unit_value*1.25)/2],
					 	 [unit_value, (unit_value*1.25)/2],
					 	 [unit_value, -(unit_value*1.75)/2],
					 	 [0, -(unit_value*1.75)/2],
					 	 [0, -(unit_value*1.25)/2],
						 [-unit_value, -(unit_value*1.25)/2],
						 [-unit_value, (unit_value*1.25)/2]]

	# Generate user layout guides
	kicad_mod.append(PolygoneLine(polygone=polygone_line, layer='Dwgs.User', width=0.1))

	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile("{}.kicad_mod".format(footprint_name))

def generate_standard_key_footprint(unit_size, rotated, offset):
	footprint_name = ""
	footprint_description = ""
	footprint_tags = ""

	if rotated:
		footprint_name = "{}_{:4.2f}u_Rotated".format(base_name, unit_size)
		footprint_description = base_description
		footprint_tags = base_tags + " {:4.2f}u".format(unit_size) + " Rotated"
	else:
		footprint_name = "{}_{:4.2f}u".format(base_name, unit_size)
		footprint_description = base_description
		footprint_tags = base_tags + " {:4.2f}u".format(unit_size)

	if offset != 0:
		footprint_name += "_Offset"
		footprint_tags += " Offset"

	kicad_mod = generate_switch(footprint_name, footprint_description, footprint_tags)

	# Generate user layout guides
	if rotated:
		kicad_mod.append(RectLine(start=[-unit_value / 2, (-(unit_size * unit_value) / 2) + offset], end=[unit_value / 2, ((unit_size * unit_value) / 2) + offset], layer='Dwgs.User', width=0.1))
	else:
		kicad_mod.append(RectLine(start=[(-(unit_size * unit_value) / 2) + offset, -unit_value / 2], end=[((unit_size * unit_value) / 2) + offset, unit_value / 2], layer='Dwgs.User', width=0.1))

	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile("{}.kicad_mod".format(footprint_name))


if __name__ == "__main__":

	generate_switch_footprint()

	for orientation in range(0, 4):
		generate_isoenter_key_footprint(orientation)

	for key in [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 4, 4.5, 5.5, 6, 6.25, 6.50, 7]:
		generate_standard_key_footprint(key, False, 0)

	for key in [1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]:
		generate_standard_key_footprint(key, True, 0)

	generate_standard_key_footprint(6, False, -9.525)