#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

import os
import shutil
import pcbnew
import wx

from KiSwitchPlugin.plugin.dialog_generator import GeneratorDialog
from KiSwitchPlugin.plugin.dialog_importer import ImporterDialog
from KiSwitchPlugin.plugin.dialog_util import error_dialog
from KiSwitchPlugin.util import logException, PLUGINPATH


def get_project_path() -> str:
    board_file = pcbnew.GetBoard().GetFileName()
    if board_file == '':
        raise Exception('No board file, please save your board first.')
    # individual board file also considered a project
    return os.path.dirname(board_file)


def get_pcbnew_frame() -> wx.Frame:
    pcbnew_frame = None
    try:
        for win in wx.GetTopLevelWindows():
            title = win.GetTitle().lower()
            if ('pcbnew' in title and not 'python' in title) or 'pcb editor' in title:
                pcbnew_frame = win
                break

        if len(pcbnew_frame) == 1:
            pcbnew_frame = pcbnew_frame[0]
        else:
            pcbnew_frame = None
    except:
        pass

    return pcbnew_frame


class KiSwitchPlugin(pcbnew.ActionPlugin):
    def __init__(self):
        try:
            getattr(self, 'dialog_class')
        except AttributeError:
            raise Exception('required dialog_class not defined')

        self.pcbnew_frame = None
        self.project_path = None

        super().__init__()


    def defaults(self):
        self.name = self.dialog_class.NAME
        self.category = 'Keyboard switch keyswitch'
        self.description = self.dialog_class.DESCRIPTION
        self.show_toolbar_button = True

        icon_path = os.path.join(PLUGINPATH, 'assets', 'icon24.png')
        self.icon_file_name = icon_path

    def Run(self):
        try:
            if self.pcbnew_frame is None:
                self.pcbnew_frame = get_pcbnew_frame()

            if self.project_path is None:
                self.project_path = get_project_path()

            dialog = self.dialog_class(self.pcbnew_frame, self.project_path)
            dialog.ShowModal()

        except Exception as e:
            if dialog in locals():
                parent = dialog
            else:
                parent = self.pcbnew_frame
            error_dialog(parent, str(e))
            logException(e, self.name)

        finally:
            if 'dialog' in locals():
                dialog.Destroy()



class KiSwitchPluginGenerator(KiSwitchPlugin):
    def __init__(self):
        self.dialog_class = GeneratorDialog
        super().__init__()


class KiSwitchPluginImporter(KiSwitchPlugin):
    def __init__(self):
        self.dialog_class = ImporterDialog
        super().__init__()
