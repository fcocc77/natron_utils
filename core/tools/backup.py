import os
import shutil
import NatronGui
from PySide import QtCore
from natron_extent import saveProject, alert

def backup():
    # guarda el proyecto antes de copiarlo
    project_path = saveProject()

    project_dir = os.path.dirname(project_path)
    backup_dir = project_dir + '/backup' 

    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)

    for i in range(100):
        # encuentra version disponible
        dirname = os.path.dirname(project_path)
        basename = os.path.basename(project_path) 
        backup_name = '__' + basename[:-4] + '_backup_' + str(i + 1) + '.ntp'
        new_backup = backup_dir + '/' + backup_name
        if not os.path.isfile( new_backup ):
            break

    shutil.copy(project_path, new_backup) 
    alert('Se genero un back-up de este proyecto llamado: ' + backup_name)

NatronGui.natron.addMenuCommand('Videovina/Project Back-UP', 'backup.backup',
                                QtCore.Qt.Key.Key_B, QtCore.Qt.KeyboardModifier.ShiftModifier)
