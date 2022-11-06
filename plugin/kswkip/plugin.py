import pcbnew
import os
import wx

from .dialog import GeneratorDialog, ImporterDialog

class KswKiPGenerator(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = 'Keyswitch KiCad Plugin (Generator)'
        self.category = 'Keyboards'
        self.description = 'Keyboard Keyswitch Generator'
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):

        try:
            dialog = GeneratorDialog()
            dialog.ShowModal()

        except Exception as e:
            except_dialog = wx.MessageDialog(
                None, str(e), 'Error', wx.OK)
            except_dialog.ShowModal()
            except_dialog.Destroy()

            log_file = os.path.join(os.path.dirname(__file__), 'KswKiPGenerator.log')
            with open(log_file, 'w') as f:
                f.write(repr(e))

        finally:
            if 'dialog' in locals():
                dialog.Destroy()


class KswKiPImporter(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = 'Keyswitch KiCad Plugin (Importer)'
        self.category = 'Keyboards'
        self.description = 'Keyboard Keyswitch Importer'
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        try:
            dialog = ImporterDialog()
            dialog.ShowModal()

        except Exception as e:
            except_dialog = wx.MessageDialog(
                None, f'Exception: {e}', 'Error', wx.OK)
            except_dialog.ShowModal()
            except_dialog.Destroy()

            log_file = os.path.join(os.path.dirname(__file__), 'KswKiPImporter.log')
            with open(log_file, 'w') as f:
                f.write(repr(e))

        finally:
            dialog.Destroy()
