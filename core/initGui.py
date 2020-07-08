import shutil
import os
import filecmp
import NatronGui


# modulos
import collect_files
import export_pyplugs
import backup
import update_node


def reload_nodes():
    repo = '/home/pancho/Documents/GitHub/natron_utils'
    natron_plugins = '/usr/share/Natron/Plugins'

    os.system('sh ' + repo + '/install.sh')

    def reload_module(module):
        module_name = module.split('.')[0]
        try:
            reload(eval(module_name))
        except:
            None

    # recarga los modulos de core
    for root, dirs, files in os.walk(repo + '/core'):
        for module in files:
            reload_module(module)

    # recarga los modulos de plugins
    for root, dirs, files in os.walk(repo + '/plugins'):
        for module in files:
            reload_module(module)

    print 'Reloaded Plugins.'


NatronGui.natron.addMenuCommand('Videovina/Reload Nodes', 'reload_nodes',
                                QtCore.Qt.Key.Key_R, QtCore.Qt.KeyboardModifier.ShiftModifier)
