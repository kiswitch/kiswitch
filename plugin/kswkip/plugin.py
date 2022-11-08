import os
import shutil
import pcbnew
import wx

from .dialog import GeneratorDialog, ImporterDialog, get_confirmation_dialog
from .fplibtable import FpLibTable, FpLibTableLib

from keyswitch_generator import generate_switch_cherry_mx


def get_project_path() -> str:
    board_file = pcbnew.GetBoard().GetFileName()
    if board_file == '':
        raise Exception('No board file, please save your board first.')
    return os.path.dirname(board_file) # individual board file also considered a project


def prepare_lib_table(project_path: str, lib_name: str) -> None:
    fp_lib_table = FpLibTable.read(project_path)

    if lib_name in fp_lib_table.libs:
        if not get_confirmation_dialog(message=f'Library {lib_name} already exists in fp-lib-table, overwrite?'):
            raise Exception(f'Library {lib_name} already exists in fp-lib-table, cannot overwrite.')
        fp_lib_table.removeLib(lib_name)

    fp_lib_table.addLib(FpLibTableLib(lib_name, '${KIPRJMOD}' + f'/{lib_name}.pretty'))
    fp_lib_table.write(project_path)


def prepare_lib_dir(project_path: str, lib_name: str) -> str:
    library_dir = os.path.join(project_path, f'{lib_name}.pretty')

    if os.path.exists(library_dir):
        if not get_confirmation_dialog(message=f'Local library {lib_name} already exists, overwrite?'):
            raise Exception(f'Local library {lib_name} already exists, cannot overwrite.')
        shutil.rmtree(library_dir)

    os.mkdir(library_dir)

    return library_dir


class KswKiPGenerator(pcbnew.ActionPlugin):
    def __init__(self):
        super().__init__()
        self.lib_name = 'ksw'

    def defaults(self):
        self.name = 'Keyswitch KiCad Plugin (Generator)'
        self.category = 'Keyboards'
        self.description = 'Keyboard Keyswitch Generator'
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        try:
            project_path = get_project_path()

            dialog = GeneratorDialog()
            dialog.ShowModal()

            library_dir = prepare_lib_dir(project_path, self.lib_name)
            prepare_lib_table(project_path, self.lib_name)

            generate_switch_cherry_mx(library_dir)

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
