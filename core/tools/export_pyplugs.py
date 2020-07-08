import os
import shutil
import NatronGui
from PySide import QtCore
from natron_extent import getNode, alert, get_select_node


def export_pyplugs():

    selected = get_select_node('fr.inria.built-in.Group')

    if not selected:
        alert('Debe seleccionar un grupo')
        return

    group = selected
    if not group.getPluginID() == 'fr.inria.built-in.Group':
        alert('Debe ser un nodo de grupo')
        return

    group.getParam('exportAsPyPlug').trigger()


NatronGui.natron.addMenuCommand('Videovina/Export Plugin', 'export_pyplugs.export_pyplugs',
                                QtCore.Qt.Key.Key_E, QtCore.Qt.KeyboardModifier.ShiftModifier)
