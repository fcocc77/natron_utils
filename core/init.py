# vvPlugins modules
import natron_utils
import vvtext
import collect_files
import transition
import shape_transition
import ink
import vinarender
import merge_matte
import videovina
import resolution_expand
import multi_photos
import glass_transition
import util
# --------------

import shutil
import os
import sys
import filecmp
import NatronEngine
import NatronGui
from PySide import QtCore

def reload_nodes():

    repo = '/home/pancho/Documents/GitHub/natron_utils'
    natron_plugins = '/usr/share/Natron/Plugins'

    plugins = repo + '/plugins'
    core = repo + '/core'

    def update(module, _type):
        if _type == 'core':
            develop_module = core + '/' + module
        else:
            develop_module = plugins + '/' + module
        natron_plugin = natron_plugins + '/' + module

        ext = module.split('.')[-1]
        if ext == 'py':
            if not os.path.isfile(natron_plugin):
                shutil.copy(develop_module, natron_plugin)

            elif not filecmp.cmp(develop_module, natron_plugin):
                shutil.copy(develop_module, natron_plugin)
                module_name = module.split('.')[0]

                try:
                    reload(eval(module_name))
                    print(module_name + ': has updated.')
                except:
                    None

    # recarga los modulos de core
    for module in os.listdir(core):
        update(module, 'core')

    # recarga los modulos de plugins
    for module in os.listdir(plugins):
        update(module, 'plugins')


NatronGui.natron.addMenuCommand('Videovina/Reload Nodes', 'reload_nodes',
                                QtCore.Qt.Key.Key_R, QtCore.Qt.KeyboardModifier.ShiftModifier)

