#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

import os
import shutil
import wx

from KiSwitchPlugin.deps_path import deps_path
from KiSwitchPlugin.plugin.dialog_util import get_confirmation_dialog, error_dialog

with deps_path():
    from KiSwitch.fplibtable import FpLib, FpLibTable
    from KiSwitch.switch import SwitchCherryMX
    from KiSwitch.renderer import GenericRenderer
    from KiSwitch.generator import SWITCHES

LIBNAME = 'KiSwitchLib'


def prepare_lib_table(parent_frame=None, project_path: str = '', lib_name: str = LIBNAME) -> None:
    fp_lib_table = FpLibTable.read(project_path)

    if lib_name in fp_lib_table.libs:
        if not get_confirmation_dialog(parent_frame, f'Library {lib_name} already exists in fp-lib-table, overwrite?'):
            raise Exception(
                f'Library {lib_name} already exists in fp-lib-table, cannot overwrite.')
        fp_lib_table.removeLib(lib_name)

    fp_lib_table.addLib(FpLib(lib_name, '${KIPRJMOD}' + f'/{lib_name}.pretty'))
    fp_lib_table.write(project_path)


def prepare_lib_dir(parent_frame=None, project_path: str = '', lib_name: str = LIBNAME) -> str:
    library_dir = os.path.join(project_path, f'{lib_name}.pretty')

    if os.path.exists(library_dir):
        if not get_confirmation_dialog(parent_frame, f'Local library {lib_name} already exists, overwrite?'):
            raise Exception(
                f'Local library {lib_name} already exists, cannot overwrite.')
        shutil.rmtree(library_dir)

    os.mkdir(library_dir)

    return library_dir


class wxRenderer(GenericRenderer):
    def __init__(self, paint_dc: 'wx.PaintDC', scale: int, center: tuple[int, int]):
        super().__init__(scale, center)
        self.paint_dc = paint_dc

    def draw_circle(self, center: tuple[int, int], radius: int, color: str, width: int | None=None) -> None:
        if width is None:
            self.paint_dc.SetPen(wx.Pen(color, width=0))
            self.paint_dc.SetBrush(wx.Brush(color, style=wx.BRUSHSTYLE_SOLID))
        else:
            self.paint_dc.SetPen(wx.Pen(color, width=width))
        self.paint_dc.DrawCircle(wx.Point(center[0], center[1]), radius)

    def draw_arc(self, center: tuple[int, int], start: tuple[int, int], end: tuple[int, int], color: str, width: int):
        self.paint_dc.SetPen(wx.Pen(color, width=width))
        self.paint_dc.DrawArc(wx.Point(start[0], start[1]), wx.Point(end[0], end[1]), wx.Point(center[0], center[1]))

    def draw_line(self, start: tuple[int, int], end: tuple[int, int], color: str, width: int):
        self.paint_dc.SetPen(wx.Pen(color, width=width))
        self.paint_dc.DrawLine(wx.Point(start[0], start[1]), wx.Point(end[0], end[1]))


class FootprintPreview(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        w, h = self.GetClientSize()
        pxmm = w / 25
        print(f'panel size: {w}x{h} mm/px: {pxmm}')

        dc = wx.PaintDC(self)
        dc.Clear()

        renderer = wxRenderer(dc, pxmm, (w // 2, h // 2))

        switch = SwitchCherryMX()

        renderer.draw(switch)


class GeneratorDialog(wx.Dialog):
    NAME = 'KiSwitch Generator'
    DESCRIPTION = 'Generate Keyboard Switch Footprints'

    def __init__(self, pcbnew_window, project_path):
        super().__init__(
            pcbnew_window, title=self.NAME,
            style=wx.DEFAULT_DIALOG_STYLE)

        self.project_path = project_path
        self.pcbnew_window = pcbnew_window

        top_sizer = wx.BoxSizer(wx.VERTICAL)

        middle_sizer = wx.BoxSizer(wx.HORIZONTAL)

        max_display_area = wx.Display().GetClientArea()
        self.maxDialogSize = wx.Size(
            min(500, max_display_area.Width),
            min(800, max_display_area.Height - 200))

        self.scroll_window = wx.ScrolledWindow(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.VSCROLL)
        self.scroll_window.SetSizeHints(
            self.maxDialogSize, wx.Size(self.maxDialogSize.width, -1))
        self.scroll_window.SetScrollRate(5, 5)

        middle_sizer.Add(self.scroll_window, 0, wx.EXPAND | wx.ALL, 5)

        self.setup_preview(middle_sizer)


        sampleList = [sw.__name__ for sw in SWITCHES]

        self.cb = wx.ComboBox(self,
                              size=wx.DefaultSize,
                              choices=sampleList)

        top_sizer.Add(self.cb, 0, wx.ALL, 8 )


        top_sizer.Add(middle_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.setup_buttons(top_sizer)

        self.SetSizer(top_sizer)

        self.on_resize()

    def on_resize(self):
        # self.scroll_window.GetSizer().Layout()
        # self.scroll_window.Fit()
        # self.scroll_window.FitInside()
        # self.GetSizer().Layout()
        self.Fit()

    def on_close(self, event):
        self.EndModal(0)  # return 0 to showModal()

    def on_generate(self, event):
        print('on_generate')
        try:
            library_dir = prepare_lib_dir(
                self, self.project_path, LIBNAME)
            prepare_lib_table(self, self.project_path, LIBNAME)
            # generate_switch_cherry_mx(library_dir)
        except Exception as e:
            error_dialog(self, str(e))

    def setup_preview(self, sizer):
        internal_sizer = wx.BoxSizer(wx.VERTICAL)

        preview_label = wx.StaticText(
            self, label="Preview:", size=wx.DefaultSize, style=wx.ALIGN_LEFT)
        internal_sizer.Add(preview_label, 0, wx.EXPAND | wx.ALL, 2)

        preview = FootprintPreview(self)
        preview.SetSizeHints(wx.Size(self.maxDialogSize.width,
                             self.maxDialogSize.height // 2), wx.Size(self.maxDialogSize.width, -1))

        internal_sizer.Add(preview, 0, wx.EXPAND | wx.ALL, 2)

        sizer.Add(internal_sizer, 0, wx.EXPAND | wx.ALL, 2)

    def setup_buttons(self, parent_sizer):
        button_box = wx.BoxSizer(wx.HORIZONTAL)

        close_button = wx.Button(self, label='Close')
        self.Bind(wx.EVT_BUTTON, self.on_close, id=close_button.GetId())
        button_box.Add(close_button, 1, wx.RIGHT, 10)

        generate_button = wx.Button(self, label='Generate')
        self.Bind(wx.EVT_BUTTON, self.on_generate, id=generate_button.GetId())
        button_box.Add(generate_button, 1, wx.RIGHT, 10)

        parent_sizer.Add(button_box, 0, wx.ALIGN_RIGHT |
                         wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)


class ImporterDialog(wx.Dialog):
    def __init__(self, parent, title, project_path=None):
        super().__init__(
            parent, title=title,
            style=wx.DEFAULT_DIALOG_STYLE)

    def OnResize(self):
        self.scrollWindow.GetSizer().Layout()
        self.scrollWindow.Fit()
        self.scrollWindow.FitInside()
        self.GetSizer().Layout()
        self.Fit()
