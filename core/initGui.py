import shutil
import os
import sys
import filecmp
import NatronGui


# modulos
import collect_files
import export_pyplugs
import backup
import update_node
import sort


def reload_nodes():
    repo = '/home/pancho/Documents/GitHub/natron_utils'
    natron_plugins = '/usr/share/Natron/Plugins'

    os.system('sh ' + repo + '/install.sh')

    ignore = ['init', 'initGui']

    def reload_modules():
        # recarga todos los modulos
        for root, dirs, files in os.walk(natron_plugins):
            for f in files:
                name = f.split('.')[0]
                ext = f.split('.')[-1]

                if not name in ignore:
                    if ext == 'py':
                        try:
                            reload(eval(name))
                        except:
                            print 'Modulo ' + name + ': No Cargado.'

    reload_modules()
    reload_modules()

    print 'Reloaded Plugins.'


NatronGui.natron.addMenuCommand('Videovina/Reload Nodes', 'reload_nodes',
                                QtCore.Qt.Key.Key_R, QtCore.Qt.KeyboardModifier.ShiftModifier)
