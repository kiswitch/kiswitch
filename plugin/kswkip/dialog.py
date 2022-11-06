
import wx

class GeneratorDialog(wx.Dialog):
    def __init__(self, parent=None, project_path=None):
        wx.Dialog.__init__(
            self, parent, title=f'KswKiP Generator',
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
            self, parent, title=f'KswKiP Importer',
            style=wx.DEFAULT_DIALOG_STYLE)

    def OnResize(self):
        self.scrollWindow.GetSizer().Layout()
        self.scrollWindow.Fit()
        self.scrollWindow.FitInside()
        self.GetSizer().Layout()
        self.Fit()
