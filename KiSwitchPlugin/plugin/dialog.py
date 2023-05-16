
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


class GeneratorDialog(wx.Dialog):
    def __init__(self, parent=None, project_path=None):
        wx.Dialog.__init__(
            self, parent, title=f'KiSwitch Generator',
            style=wx.DEFAULT_DIALOG_STYLE)

    def OnResize(self):
        self.scrollWindow.GetSizer().Layout()
        self.scrollWindow.Fit()
        self.scrollWindow.FitInside()
        self.GetSizer().Layout()
        self.Fit()


class ImporterDialog(wx.Dialog):
    def __init__(self, parent=None, project_path=None):
        wx.Dialog.__init__(
            self, parent, title=f'KiSwitch Importer',
            style=wx.DEFAULT_DIALOG_STYLE)

    def OnResize(self):
        self.scrollWindow.GetSizer().Layout()
        self.scrollWindow.Fit()
        self.scrollWindow.FitInside()
        self.GetSizer().Layout()
        self.Fit()
