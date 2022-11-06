import pcbnew
import os
import shutil
import wx

def get_project_path():
    board_file = pcbnew.GetBoard().GetFileName()
    if board_file == '':
        raise Exception('No board file, please save your board first.')
    return os.path.dirname(board_file) # individual board file also considered a project


def create_library_dir(path, name):
    library_dir = os.path.join(path, f'{name}.pretty')

    if os.path.exists(library_dir):
        overwrite_dialog = wx.MessageDialog(
            None,
            'Local keyswitch library exists Would you like to overwrite?',
            'Confirm',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        choice = overwrite_dialog.ShowModal()
        overwrite_dialog.Destroy()

        if choice == wx.ID_NO:
            raise Exception('Local keyswitch library exists, cannot overwrite.')

        shutil.rmtree(library_dir, ignore_errors=True)

    os.mkdir(library_dir)

    return library_dir
