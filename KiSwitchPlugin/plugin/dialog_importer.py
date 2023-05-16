#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

import wx

class ImporterDialog(wx.Dialog):
    NAME = 'KiSwitch Importer'
    DESCRIPTION = 'Import Keyboard layout'

    def __init__(self, pcbnew_window, project_path=None):
        wx.Dialog.__init__(
            self, pcbnew_window, title=self.NAME,
            style=wx.DEFAULT_DIALOG_STYLE)

    def OnResize(self):
        return
