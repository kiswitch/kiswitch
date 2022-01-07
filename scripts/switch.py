from os import path

from KicadModTree.nodes.Footprint import Footprint
from KicadModTree.nodes.base import Text, Model, Pad, Line, Arc
from KicadModTree.nodes.specialized import RectLine, PolygoneLine

from keycap import Keycap
import util


class Switch(Footprint):
    def __init__(self, name: str, description: str, tags: str,
                 cutout: bool = False, keycap: Keycap = None,
                 path3d: str = None, model3d: str = None,
                 text_offset: float = 8):

        Footprint.__init__(self, None)

        self.name = name
        self.description = description
        self.tags = tags
        self.text_offset = text_offset
        self.path3d = None

        if model3d is not None:
            self.path3d = model3d
            if path3d is not None:
                self.path3d = path.join(path3d, self.path3d)

        if cutout is True:
            self.tags += ' Cutout'

        if keycap is not None:
            self.name += '_' + keycap.name
            self.description += f' with {keycap.tags} keycap'
            self.tags += ' ' + keycap.tags

        self.name.replace(' ', '_')

        self._init_generic_nodes()

    def _init_generic_nodes(self):
        # add general values
        self.append(Text(type='reference', text='REF**',
                         at=[0, -self.text_offset], layer='F.SilkS'))
        self.append(Text(type='value', text=self.name,
                         at=[0, self.text_offset], layer='F.Fab'))
        self.append(Text(type='user', text='%R',
                         at=[0, 0], layer='F.Fab'))

        # add model if available
        if self.path3d is not None:
            self.append(Model(filename=self.path3d,
                        at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))


class StabilizerCherryMX(Switch):

    lu_table = {
        2: {'desc': '2.00u 2.25u 2.50u 2.75u', 'offset': 11.938},
        3: {'desc': '3.00u', 'offset': 19.05},
        6: {'desc': '6.00u', 'offset': 47.625},
        6.25: {'desc': '6.25u', 'offset': 50},
        7: {'desc': '7.00u', 'offset': 57.15},
        8: {'desc': '8.00u 9.00u 10.00u', 'offset': 66.675},
    }

    def __init__(self,
                 size: float = None,
                 name: str = 'Stabilizer_Cherry_MX',
                 description: str = 'Cherry MX PCB Stabilizer',
                 tags: str = 'Cherry MX Keyboard Stabilizer',
                 cutout: bool = True, keycap: Keycap = None,
                 path3d: str = None, model3d: str = None):

        if size is None or size not in self.lu_table:
            raise Exception(f'{size} is not a valid size')

        self.size = size

        _name = name + f'_{size:1.2f}u'
        _description = description + ' ' + self.lu_table[size]['desc']
        _tags = tags + ' ' + self.lu_table[size]['desc']

        Switch.__init__(self,
                        name=_name,
                        description=_description,
                        tags=_tags,
                        cutout=cutout,
                        path3d=path3d,
                        model3d=model3d if model3d is not None
                        else f'{_name}.wrl',
                        text_offset=2)

        self._init_base()

        if cutout is True:
            self._init_cutout()

    def _init_base(self):

        # set attributes
        self.setAttribute('virtual')

        # add pads
        small_hole_size = 3.048
        large_hole_size = 3.9878
        top_offset = -6.985
        bottom_offset = 8.225
        offset = self.lu_table[self.size]['offset']
        layers = ['*.Cu', '*.Mask']

        # create pads
        self.append(Pad(number="~", type=Pad.TYPE_NPTH,
                        shape=Pad.SHAPE_CIRCLE, at=[-offset, top_offset],
                        size=small_hole_size,
                        drill=small_hole_size, layers=layers))
        self.append(Pad(number="~", type=Pad.TYPE_NPTH,
                        shape=Pad.SHAPE_CIRCLE, at=[offset, top_offset],
                        size=small_hole_size,
                        drill=small_hole_size, layers=layers))
        self.append(Pad(number="~", type=Pad.TYPE_NPTH,
                        shape=Pad.SHAPE_CIRCLE, at=[-offset, bottom_offset],
                        size=large_hole_size,
                        drill=large_hole_size, layers=layers))
        self.append(Pad(number="~", type=Pad.TYPE_NPTH,
                        shape=Pad.SHAPE_CIRCLE, at=[offset, bottom_offset],
                        size=large_hole_size,
                        drill=large_hole_size, layers=layers))

        # create reference center point
        self.append(Line(start=[0, 2], end=[0, -2],
                         layer='Dwgs.User', width=0.1))
        self.append(Line(start=[-2, 0], end=[2, 0],
                         layer='Dwgs.User', width=0.1))

    def _init_cutout(self):

        offset = self.lu_table[self.size]['offset']

        # create cutout
        self.append(RectLine(
            start=[offset - 3.375, -5.53],
            end=[offset + 3.375, 6.77],
            layer='Eco1.User', width=0.1))
        self.append(RectLine(
            start=[-offset - 3.375, -5.53],
            end=[-offset + 3.375, 6.77],
            layer='Eco1.User', width=0.1))


# https://github.com/keyboardio/keyswitch_documentation/blob/master/datasheets/ALPS/SKCL.pdf
class SwitchAlpsMatias(Switch):

    def __init__(self,
                 name: str = 'SW_Alps_Matias',
                 description: str = 'Alps/Matias keyswitch',
                 tags: str = 'Alps Matias Keyboard Keyswitch Switch Plate',
                 cutout: bool = True, keycap: Keycap = None,
                 path3d: str = None, model3d: str = 'SW_Alps_Matias.wrl'):

        Switch.__init__(self,
                        name=name,
                        description=description,
                        tags=tags,
                        cutout=cutout,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d)

        self._init_switch()

        if cutout is True:
            self._init_cutout()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):
        # create fab outline
        self.append(RectLine(start=[-7.75, -6.4], end=[7.75, 6.4],
                    layer='F.Fab', width=0.1))

        # create silkscreen
        self.append(RectLine(start=[-7.75, -6.4], end=[7.75, 6.4],
                    layer='F.SilkS', width=0.12, offset=0.1))

        # create courtyard
        self.append(RectLine(start=[-7.75, -6.4], end=[7.75, 6.4],
                    layer='F.CrtYd', width=0.05, offset=0.25))

        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                    at=[-2.5, -4], size=[2.5, 2.5], drill=1.5,
                    layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                    at=[2.5, -4.5], size=[2.5, 2.5], drill=1.5,
                    layers=['*.Cu', 'B.Mask']))

    def _init_cutout(self):

        width = 15.5
        height = 12.8

        # create cutout
        self.append(RectLine(start=[-width/2, -height/2],
                             end=[width/2, height/2],
                             layer='Eco1.User', width=0.1))


# https://www.cherrymx.de/en/dev.html
class SwitchCherryMX(Switch):

    cherry_w = 14
    cherry_h = 14

    def __init__(self,
                 switch_type: str = 'PCB',
                 name: str = 'SW_Cherry_MX',
                 description: str = 'Cherry MX keyswitch',
                 tags: str = 'Cherry MX Keyboard Keyswitch Switch',
                 cutout: str = 'simple', keycap: Keycap = None,
                 path3d: str = None, model3d: str = None):

        if switch_type not in ['PCB', 'Plate']:
            raise ValueError(f'Switch type {switch_type} not supported.')

        if cutout not in ['simple', 'relief', None]:
            raise ValueError(f'Cutout type {cutout} not supported.')

        self.switch_type = switch_type
        self.cutout = cutout

        _name = name + '_' + switch_type
        _description = description + ' ' + switch_type + ' Mount'
        _tags = tags + ' ' + switch_type

        Switch.__init__(self,
                        name=_name,
                        description=_description,
                        tags=_tags,
                        cutout=True if cutout is not None else False,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d if model3d is not None
                        else f'{_name}.wrl')

        self._init_switch()

        if cutout is not None:
            if cutout == 'simple':
                self._init_cutout_simple()
            elif cutout == 'relief':
                self._init_cutout_relief()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):

        # create fab outline
        self.append(RectLine(start=[-self.cherry_w/2, -self.cherry_h/2],
                             end=[self.cherry_w/2, self.cherry_h/2],
                             layer='F.Fab', width=0.1))

        # create silkscreen
        self.append(RectLine(start=[-self.cherry_w/2, -self.cherry_h/2],
                             end=[self.cherry_w/2, self.cherry_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create courtyard
        self.append(RectLine(start=[-self.cherry_w/2, -self.cherry_h/2],
                             end=[self.cherry_w/2, self.cherry_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))
        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[-3.81, -2.54], size=[2.5, 2.5], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[2.54, -5.08], size=[2.5, 2.5], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[4, 4], drill=4,
                        layers=['*.Cu', '*.Mask']))

        if self.switch_type == 'PCB':
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[-5.08, 0], size=[1.75, 1.75], drill=1.75,
                            layers=['*.Cu', '*.Mask']))
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[5.08, 0], size=[1.75, 1.75], drill=1.75,
                            layers=['*.Cu', '*.Mask']))

    def _init_cutout_simple(self):

        # create cutout
        self.append(RectLine(start=[-self.cherry_w/2, -self.cherry_h/2],
                             end=[self.cherry_w/2, self.cherry_h/2],
                             layer='Eco1.User', width=0.1))

    def _init_cutout_relief(self):

        # create cutout
        polyline = [[7, -7],
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
                    [7, -7]]

        self.append(PolygoneLine(polygone=polyline,
                                 layer='Eco1.User', width=0.1))


# https://www.cherrymx.de/en/dev.html
# https://github.com/keyboardio/keyswitch_documentation/blob/master/datasheets/ALPS/SKCL.pdf
class SwitchHybridCherryMxAlps(Switch):

    cherry_w = 14
    cherry_h = 14

    alps_w = 15.5
    alps_h = 12.8

    def __init__(self,
                 name: str = 'SW_Hybrid_Cherry_MX_Alps',
                 description: str = 'Cherry MX / Alps keyswitch hybrid',
                 tags: str = 'Cherry MX Alps Matias Hybrid Keyboard Keyswitch'
                             'Switch PCB',
                 keycap: Keycap = None,
                 path3d: str = None, model3d: str = None):

        Switch.__init__(self,
                        name=name,
                        description=description,
                        tags=tags,
                        keycap=keycap)

        self.path3d = path3d
        self.model3d = model3d

        self._init_switch()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):

        # Models
        if self.model3d is not None:
            filename = self.model3d
            if self.path3d is not None:
                filename = path.join(self.path3d, filename)

            self.append(Model(filename=filename,
                              at=[0, 0, 0], scale=[1, 1, 1],
                              rotate=[0, 0, 0]))
        else:
            filename1 = 'SW_Cherry_MX_PCB.wrl'
            filename2 = 'SW_Alps_Matias.wrl'

            if self.path3d is not None:
                filename1 = path.join(self.path3d, filename1)
                filename2 = path.join(self.path3d, filename2)

            self.append(Model(filename=filename1,
                              at=[0, 0, 0], scale=[1, 1, 1],
                              rotate=[0, 0, 0]))
            self.append(Model(filename=filename2,
                              at=[0, 0, 0], scale=[1, 1, 1],
                              rotate=[0, 0, 0]))

        base_polyline = [[-self.cherry_w/2, -self.cherry_h/2],
                         [self.cherry_w/2, -self.cherry_h/2],
                         [self.cherry_w/2, -self.alps_h/2],
                         [self.alps_w/2, -self.alps_h/2],
                         [self.alps_w/2, self.alps_h/2],
                         [self.cherry_w/2, self.alps_h/2],
                         [self.cherry_w/2, self.cherry_h/2],
                         [-self.cherry_w/2, self.cherry_h/2],
                         [-self.cherry_w/2, self.alps_h/2],
                         [-self.alps_w/2, self.alps_h/2],
                         [-self.alps_w/2, -self.alps_h/2],
                         [-self.cherry_w/2, -self.alps_h/2],
                         [-self.cherry_w/2, -self.cherry_h/2]]

        # create fab outline
        self.append(PolygoneLine(polygone=base_polyline,
                                 layer='F.Fab', width=0.1))

        # create silkscreen outline
        polyline = util.offset_polyline(base_polyline, 0.1)
        self.append(PolygoneLine(polygone=polyline,
                                 layer='F.SilkS', width=0.12))

        # create courtyard outline
        polyline = util.offset_polyline(base_polyline, 0.25)
        self.append(PolygoneLine(polygone=polyline,
                                 layer='F.CrtYd', width=0.05))

        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[-2.5, -4], size=[2.5, 2.5], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL,
                        at=[-3.81, -2.54], size=[4.46156, 2.5],
                        rotation=48, offset=[0.980778, 0], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL,
                    at=[2.52, -4.79], size=[3.081378, 2.5],
                    drill=[2.08137, 1.5], rotation=86,
                    layers=['*.Cu', 'B.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                    at=[0, 0], size=[4, 4], drill=4,
                    layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                    at=[-5.08, 0], size=[1.75, 1.75], drill=1.75,
                    layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                    at=[5.08, 0], size=[1.75, 1.75], drill=1.75,
                    layers=['*.Cu', '*.Mask']))


# http://www.kailh.com/en/Products/Ks/CS/
class SwitchKailhChocV1(Switch):

    choc_w = 15
    choc_h = 15

    choc_cut_w = 14.5
    choc_cut_h = 14.5

    def __init__(self,
                 name: str = 'SW_Kailh_Choc_V1',
                 description: str = 'Kailh Choc V1 (CPG1350) keyswitch',
                 tags: str = 'Kailh Choc V1 CPG1350 Keyswitch Switch',
                 cutout: bool = True, keycap: Keycap = None,
                 path3d: str = None, model3d: str = 'SW_Kailh_Choc_V1.wrl'):

        Switch.__init__(self,
                        name=name,
                        description=description,
                        tags=tags,
                        cutout=cutout,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d,
                        text_offset=9)

        self._init_switch()

        if cutout is True:
            self._init_cutout()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):

        # create fab outline
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.Fab', width=0.1))

        # create silkscreen
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create courtyard
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))

        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[0, -5.9], size=[2.2, 2.2], drill=1.2,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[5, -3.8], size=[2.2, 2.2], drill=1.2,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[3.2, 3.2], drill=3.2,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5.5, 0], size=[1.8, 1.8], drill=1.8,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[5.5, 0], size=[1.8, 1.8], drill=1.8,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5.22, 4.2], size=[1.2, 1.2], drill=1.2,
                        layers=['*.Cu', '*.Mask']))

    def _init_cutout(self):

        # create cutout
        self.append(RectLine(start=[-self.choc_cut_w/2, -self.choc_cut_h/2],
                             end=[self.choc_cut_w/2, self.choc_cut_h/2],
                             layer='Eco1.User', width=0.1))


# https://www.kailhswitch.com/mechanical-keyboard-switches/mini-keyboard-push-button-switches.html
class SwitchKailhChocMini(Switch):

    choc_mini_w = 14.5
    choc_mini_h = 13.5

    choc_mini_cut_w = 13.7
    choc_mini_cut_h = 12.7

    def __init__(self,
                 name: str = 'SW_Kailh_Choc_Mini',
                 description: str = 'Kailh Choc Mini CPG1232 low profile keyswitch',
                 tags: str = 'Kailh Choc Mini CPG1232 Keyboard Low Profile Keyswitch Switch',
                 cutout: bool = True, keycap: Keycap = None,
                 path3d: str = None, model3d: str = 'SW_Kailh_Choc_Mini.wrl'):

        Switch.__init__(self,
                        name=name,
                        description=description,
                        tags=tags,
                        cutout=cutout,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d,
                        text_offset=8.5)

        self._init_switch()

        if cutout is True:
            self._init_cutout()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):
        # create fab outline
        self.append(RectLine(start=[-self.choc_mini_w/2, -self.choc_mini_h/2],
                             end=[self.choc_mini_w/2, self.choc_mini_h/2],
                             layer='F.Fab', width=0.1))

        # create silkscreen
        self.append(RectLine(start=[-self.choc_mini_w/2, -self.choc_mini_h/2],
                             end=[self.choc_mini_w/2, self.choc_mini_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create courtyard
        self.append(RectLine(start=[-self.choc_mini_w/2, -self.choc_mini_h/2],
                             end=[self.choc_mini_w/2, self.choc_mini_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))

        # center hole
        polyline=[
            [5.95, -2.9],
            [-5.9, -2.9],
            [-5.9, 3],
            [-2.5, 3],
            [-2.5, 4.05],
            [2.05, 4.05],
            [2.05, 3],
            [5.95, 3],
            [5.95, -2.9]
        ]
        self.append(PolygoneLine(polygone=polyline,
                                 layer='Edge.Cuts', width=0.05))

        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[2, 5.4], size=[1.5, 1.5], drill=1.2,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[-4.58, 5.1], size=[1.5, 1.5], drill=1.2,
                        layers=['*.Cu', 'B.Mask']))

        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_OVAL,
                        at=[-5.29, -4.75], size=[1.2, 1.6], drill=[0.8, 1.2],
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_OVAL,
                        at=[5.29, -4.75], size=[1.2, 1.6], drill=[0.8, 1.2],
                        layers=['*.Cu', '*.Mask']))

    def _init_cutout(self):

        # create cutout
        self.append(RectLine(start=[-self.choc_mini_cut_w/2, -self.choc_mini_cut_h/2],
                             end=[self.choc_mini_cut_w/2, self.choc_mini_cut_h/2],
                             layer='Eco1.User', width=0.1))


# http://www.kailh.com/en/Products/Ks/KHS
class SwitchKailhKH(Switch):

    kailh_kh_w = 13
    kailh_kh_h = 13

    kailh_kh_cut_w = 12.2
    kailh_kh_cut_h = 12.2

    def __init__(self,
                 name: str = 'SW_Kailh_KH',
                 description: str = 'Kailh KH CPG1280 keyswitch',
                 tags: str = 'Kailh KH CPG1280 Keyboard Keyswitch Switch',
                 cutout: bool = True, keycap: Keycap = None,
                 path3d: str = None, model3d: str = 'SW_Kailh_KH.wrl'):

        Switch.__init__(self,
                        name=name,
                        description=description,
                        tags=tags,
                        cutout=cutout,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d)

        self._init_switch()

        if cutout is True:
            self._init_cutout()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):
        # create fab outline
        self.append(RectLine(start=[-self.kailh_kh_w/2, -self.kailh_kh_h/2],
                             end=[self.kailh_kh_w/2, self.kailh_kh_h/2],
                             layer='F.Fab', width=0.1))

        # create silkscreen
        self.append(RectLine(start=[-self.kailh_kh_w/2, -self.kailh_kh_h/2],
                             end=[self.kailh_kh_w/2, self.kailh_kh_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create courtyard
        self.append(RectLine(start=[-self.kailh_kh_w/2, -self.kailh_kh_h/2],
                             end=[self.kailh_kh_w/2, self.kailh_kh_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))

        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[-3.8, -2.55], size=[2.5, 2.5], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[3, -5.12], size=[2.5, 2.5], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))

        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[4, 4], drill=4,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-4.5, 0], size=[1.5, 1.5], drill=1.5,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[4.5, 0], size=[1.5, 1.5], drill=1.5,
                        layers=['*.Cu', '*.Mask']))

    def _init_cutout(self):

        # create cutout
        self.append(RectLine(start=[-self.kailh_kh_cut_w/2, -self.kailh_kh_cut_h/2],
                             end=[self.kailh_kh_cut_w/2, self.kailh_kh_cut_h/2],
                             layer='Eco1.User', width=0.1))


# http://www.kailh.com/en/Products/Ks/NotebookS/
class SwitchKailhNB(Switch):

    kailh_nb_w = 14
    kailh_nb_h = 14.8

    def __init__(self,
                 name: str = 'SW_Kailh_NB',
                 description: str = 'Kailh KH CPG1425 low profile notebook keyswitch',
                 tags: str = 'Kailh KH CPG1425 Keyboard Low Profile Notebook Keyswitch Switch',
                 cutout: bool = True, keycap: Keycap = None,
                 path3d: str = None, model3d: str = 'SW_Kailh_NB.wrl'):

        Switch.__init__(self,
                        name=name,
                        description=description,
                        tags=tags,
                        cutout=cutout,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d,
                        text_offset=8.5)

        self._init_switch()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):
        # create fab outline
        self.append(RectLine(start=[-self.kailh_nb_w/2, -self.kailh_nb_h/2],
                             end=[self.kailh_nb_w/2, self.kailh_nb_h/2],
                             layer='F.Fab', width=0.1))

        # create silkscreen
        self.append(RectLine(start=[-self.kailh_nb_w/2, -self.kailh_nb_h/2],
                             end=[self.kailh_nb_w/2, self.kailh_nb_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create courtyard
        self.append(RectLine(start=[-self.kailh_nb_w/2, -self.kailh_nb_h/2],
                             end=[self.kailh_nb_w/2, self.kailh_nb_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))

        # center hole
        self.append(RectLine(start=[1.1, -2.5], end=[-2.9, 2.5],
                             layer='Edge.Cuts', width=0.05))

        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[-2, -3.4], size=[1.4, 1.4], drill=1.1,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[2.9, -3.4], size=[1.4, 1.4], drill=1.1,
                        layers=['*.Cu', 'B.Mask']))

        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[5.5, -5.50], size=[1.3, 1.3], drill=1.3,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5.5, 5.5], size=[1.3, 1.3], drill=1.3,
                        layers=['*.Cu', '*.Mask']))


class SwitchHotswapKailh(Switch):

    kailh_hs_w = 14
    kailh_hs_h = 14

    def __init__(self,
                 plated_th: bool = False,
                 name: str = 'SW_Hotswap_Kailh_MX',
                 description: str = 'Kailh keyswitch Hotswap Socket',
                 tags: str = 'Kailh Keyboard Keyswitch Switch Hotswap Socket',
                 cutout: str = 'relief', keycap: Keycap = None,
                 path3d: str = None, model3d: str = 'SW_Hotswap_Kailh_MX.wrl'):

        if cutout not in ['simple', 'relief', None]:
            raise ValueError(f'Cutout type {cutout} not supported.')

        self.cutout = cutout
        self.plated_th = plated_th

        _name=name
        _tags=tags
        _description=description

        if self.plated_th is True:
            _name += '_plated'
            _tags += ' plated'
            _description += ' plated holes'

        Switch.__init__(self,
                        name=_name,
                        description=_description,
                        tags=_tags,
                        cutout=True if cutout is not None else False,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d)

        self._init_switch()

        if cutout is not None:
            if cutout == 'simple':
                self._init_cutout_simple()
            elif cutout == 'relief':
                self._init_cutout_relief()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):

        # set attributes
        self.setAttribute('smd')

        # create fab outline (keyswitch)
        self.append(RectLine(start=[-self.kailh_hs_w/2, -self.kailh_hs_h/2],
                             end=[self.kailh_hs_w/2, self.kailh_hs_h/2],
                             layer='F.Fab', width=0.1))

        # create fab outline (socket)
        self.append(Line(start=[-4, -6.8], end=[4.8, -6.8],
                    layer='B.Fab', width=0.12))
        self.append(Line(start=[4.8, -6.8], end=[4.8, -2.8],
                    layer='B.Fab', width=0.12))
        self.append(Line(start=[-0.3, -2.8], end=[4.8, -2.8],
                    layer='B.Fab', width=0.12))
        self.append(Line(start=[-6, -0.8], end=[-2.3, -0.8],
                    layer='B.Fab', width=0.12))
        self.append(Line(start=[-6, -0.8], end=[-6, -4.8],
                    layer='B.Fab', width=0.12))
        self.append(Arc(center=[-4, -4.8], start=[-4, -6.8],
                    angle=-90, layer='B.Fab', width=0.12))
        self.append(Arc(center=[-0.3, -0.8], start=[-0.3, -2.8],
                    angle=-90, layer='B.Fab', width=0.12))

        # create silkscreen (keyswitch)
        self.append(RectLine(start=[-self.kailh_hs_w/2, -self.kailh_hs_h/2],
                             end=[self.kailh_hs_w/2, self.kailh_hs_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create silkscreen (socket)
        self.append(Line(start=[-4.1, -6.9], end=[1, -6.9],
                         layer='B.SilkS', width=0.12))
        self.append(Line(start=[-0.2, -2.7], end=[4.9, -2.7],
                         layer='B.SilkS', width=0.12))
        self.append(Arc(center=[-4.1, -4.9], start=[-4.1, -6.9],
                        angle=-90, layer='B.SilkS', width=0.12))
        self.append(Arc(center=[-0.2, -0.7], start=[-0.2, -2.7],
                        angle=-90, layer='B.SilkS', width=0.12))

        # create courtyard (keyswitch)
        self.append(RectLine(start=[-self.kailh_hs_w/2, -self.kailh_hs_h/2],
                             end=[self.kailh_hs_w/2, self.kailh_hs_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))

        # create courtyard (socket)
        # !TODO: add KLC correct offset (0.25)
        self.append(Line(start=[-4, -6.8], end=[4.8, -6.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Line(start=[4.8, -6.8], end=[4.8, -2.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Line(start=[-0.3, -2.8], end=[4.8, -2.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Line(start=[-6, -0.8], end=[-2.3, -0.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Line(start=[-6, -0.8], end=[-6, -4.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Arc(center=[-4, -4.8], start=[-4, -6.8],
                    angle=-90, layer='B.CrtYd', width=0.05))
        self.append(Arc(center=[-0.3, -0.8], start=[-0.3, -2.8],
                    angle=-90, layer='B.CrtYd', width=0.05))

        # create pads
        if self.plated_th is True:
            self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[-3.81, -2.54], size=[3.6, 3.6], drill=3.05,
                            layers=['*.Cu', 'B.Mask']))
            self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[2.54, -5.08], size=[3.6, 3.6], drill=3.05,
                            layers=['*.Cu', 'B.Mask']))

            self.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[-6.585, -2.54], size=[3.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu']))
            self.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[5.32, -5.08], size=[3.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu']))

            self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[-7.085, -2.54], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Mask', 'B.Paste']))
            self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[5.842, -5.08], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Mask', 'B.Paste']))
        else:
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[-3.81, -2.54], size=[3.05, 3.05], drill=3.05,
                            layers=['*.Cu', '*.Mask']))
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[2.54, -5.08], size=[3.05, 3.05], drill=3.05,
                            layers=['*.Cu', '*.Mask']))

            self.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                        at=[-7.085, -2.54], size=[2.55, 2.5],
                        round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))
            self.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                        at=[5.842, -5.08], size=[2.55, 2.5],
                        round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))

        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[4, 4], drill=4,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5.08, 0], size=[1.75, 1.75], drill=1.75,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[5.08, 0], size=[1.75, 1.75], drill=1.75,
                        layers=['*.Cu', '*.Mask']))

    def _init_cutout_simple(self):
        # create cutout
        self.append(RectLine(start=[-self.kailh_hs_w/2, -self.kailh_hs_h/2],
                             end=[self.kailh_hs_w/2, self.kailh_hs_h/2],
                             layer='Eco1.User', width=0.1))

    def _init_cutout_relief(self):

        # create cutout
        polyline = [[7, -7],
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
                    [7, -7]]

        self.append(PolygoneLine(polygone=polyline,
                                 layer='Eco1.User', width=0.1))


class SwitchHotswapKailhChocV1(Switch):

    choc_w = 15
    choc_h = 15

    choc_cut_w = 14.5
    choc_cut_h = 14.5

    def __init__(self,
                 plated_th: bool = True,
                 name: str = 'SW_Hotswap_Kailh_Choc_V1',
                 description: str = 'Kailh keyswitch Hotswap Socket',
                 tags: str = 'Kailh Keyboard Choc V1 keyswitch Keyswitch Switch Hotswap Socket',
                 cutout: bool = True, keycap: Keycap = None,
                 path3d: str = None, model3d: str = 'SW_Hotswap_Kailh_Choc_v1.stp'):

        self.plated_th = plated_th

        _name=name
        _tags=tags
        _description=description

        if self.plated_th is True:
            _name += '_plated'
            _tags += ' plated'
            _description += ' plated holes'

        Switch.__init__(self,
                        name=_name,
                        description=_description,
                        tags=_tags,
                        cutout=cutout,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d,
                        text_offset=9)

        self._init_switch()

        if cutout is True:
            self._init_cutout()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):

        # set attributes
        self.setAttribute('smd')

        # socket outline
        # TODO: this outline is incorrect
        polyline_base = [
            [6.75, -2.25],
            [6.25, -1.75],
            [3.5, -1.75],
            [1.25, -4],
            [-1.25, -4],
            [-1.75, -4.5],
        ]

        polyline_base2 = [
            [-1.75, -7.5],
            [-1.25, -8],
            [1.25, -8],
            [3.5, -5.75],
            [6.25, -5.75],
            [6.75, -5.25],
        ]

        # create fab outline (keyswitch)
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.Fab', width=0.1))

        # create fab outline (socket)
        self.append(PolygoneLine(polygone=polyline_base,
                                 layer='B.Fab', width=0.1))
        self.append(PolygoneLine(polygone=polyline_base2,
                                 layer='B.Fab', width=0.1))

        # create silkscreen (keyswitch)
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create silkscreen (socket)
        # TODO: offset 0.1
        self.append(PolygoneLine(polygone=polyline_base,
                                 layer='B.SilkS', width=0.12))
        self.append(PolygoneLine(polygone=polyline_base2,
                                 layer='B.SilkS', width=0.12))

        # create courtyard (keyswitch)
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))

        # create courtyard (socket)
        # TODO: offset 0.25
        polyline = polyline_base + polyline_base2
        polyline.append(polyline_base[0])
        self.append(PolygoneLine(polygone=polyline,
                                 layer='B.CrtYd', width=0.05))

        # create pads
        if self.plated_th is True:
            self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[0, -5.9], size=[3.6, 3.6], drill=3.05,
                            layers=['*.Cu', 'B.Mask']))
            self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[5, -3.8], size=[3.6, 3.6], drill=3.05,
                            layers=['*.Cu', 'B.Mask']))

            self.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[-2.85, -6], size=[3.85, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu']))
            self.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[7.85, -3.8], size=[3.85, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu']))

            self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[-3.5, -6], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Mask', 'B.Paste']))
            self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[8.5, -3.8], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Mask', 'B.Paste']))
        else:
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[0, -5.9], size=[3.05, 3.05], drill=3.05,
                            layers=['*.Cu', '*.Mask']))
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[5, -3.8], size=[3.05, 3.05], drill=3.05,
                            layers=['*.Cu', '*.Mask']))

            self.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[-3.5, -6], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))
            self.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[8.5, -3.8], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))

        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[3.4, 3.4], drill=3.4,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5.5, 0], size=[1.9, 1.9], drill=1.9,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[5.5, 0], size=[1.9, 1.9], drill=1.9,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5.22, 4.2], size=[1.3, 1.3], drill=1.3,
                        layers=['*.Cu', '*.Mask']))

    def _init_cutout(self):

        # create cutout
        self.append(RectLine(start=[-self.choc_cut_w/2, -self.choc_cut_h/2],
                             end=[self.choc_cut_w/2, self.choc_cut_h/2],
                             layer='Eco1.User', width=0.1))