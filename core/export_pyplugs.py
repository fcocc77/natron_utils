import os
import shutil
import NatronGui
from PySide import QtCore
from natron_utils import getNode, alert

def export_pyplugs():
    app = NatronGui.natron.getGuiInstance(0)

    selected = app.getSelectedNodes(app)

    if len(selected) == 0:
        alert('Debe seleccionar un grupo')
        return
    elif len(selected) > 1:
        alert('Debe seleccionar solo un grupo')
        return
    
    group = selected[0]
    if not group.getPluginID() == 'fr.inria.built-in.Group':
        alert('Debe ser un nodo de grupo')
        return

    group.getParam('exportAsPyPlug').trigger()

NatronGui.natron.addMenuCommand('Videovina/Export Plugin', 'export_pyplugs.export_pyplugs',
                                QtCore.Qt.Key.Key_E, QtCore.Qt.KeyboardModifier.ShiftModifier)
