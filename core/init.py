import os
import shutil
import sys
import NatronEngine

# vvPlugins modules
import vvtext
import ink
import vinarender
import merge_matte
import util
# --------------


def reload_nodes():
    repo = '/home/pancho/Documents/GitHub/natron_pyplugs'
    natron_plugins = '/usr/share/Natron/Plugins'

    plugins = repo + '/plugins'
    core = repo + '/core'

    # recarga los modulos de core
    for module in os.listdir(core):

        develop_module = core + '/' + module
        natron_plugin = natron_plugins + '/' + module

        shutil.copy(develop_module, natron_plugin)

        _module = module.split('.')[0]

        # si el modulo esta cargado lo recarga
        if _module in sys.modules:
            reload(eval(_module))
            print(_module + ': has updated.')

    # recarga los modulos de plugins
    for plugin in os.listdir(plugins):
        ext = plugin.split('.')[-1]
        plugin_name = plugin.split('.')[0]
        if ext == 'py':
            try:
                reload(eval(plugin_name))
                print(plugin_name + ': has updated.')
            except:
                None


NatronGui.natron.addMenuCommand('videovina/Reload Nodes', 'reload_nodes',
                                QtCore.Qt.Key.Key_U, QtCore.Qt.KeyboardModifier.ControlModifier)
