#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

import wx


def get_confirmation_dialog(parent=None, message: str = '', title: str = 'Confirm') -> bool:
    confirmation_dialog = wx.MessageDialog(
        parent, message, title,
        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
    choice = confirmation_dialog.ShowModal()
    confirmation_dialog.Destroy()

    if choice == wx.ID_NO:
        return False
    return True


def error_dialog(parent=None, message: str = '', title: str = 'Error') -> None:
    error_dialog = wx.MessageDialog(
        parent, message, title,
        wx.OK | wx.ICON_ERROR)
    error_dialog.ShowModal()
    error_dialog.Destroy()
