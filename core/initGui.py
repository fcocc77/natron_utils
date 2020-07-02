import shutil
import os
import filecmp
import NatronGui


# modulos
import collect_files
import export_pyplugs
import backup


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
        if ext == 'png':
            shutil.copy(develop_module, natron_plugin)

    # recarga los modulos de core
    for module in os.listdir(core):
        update(module, 'core')

    # recarga los modulos de plugins
    for module in os.listdir(plugins):
        update(module, 'plugins')


NatronGui.natron.addMenuCommand('Videovina/Reload Nodes', 'reload_nodes',
                                QtCore.Qt.Key.Key_R, QtCore.Qt.KeyboardModifier.ShiftModifier)
