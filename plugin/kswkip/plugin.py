import pcbnew
import os
import wx


class KswKiPGenerator(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = 'Keyswitch KiCad Plugin (Generator)'
        self.category = 'Keyboards'
        self.description = 'Keyboard Keyswitch Generator'
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')


class KswKiPImporter(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = 'Keyswitch KiCad Plugin (Importer)'
        self.category = 'Keyboards'
        self.description = 'Keyboard Keyswitch Importer'
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')
