# Si un nodo plugin de videovina ya fue creado, esta opcion
# actualiza el nodo con los parametros nuevos pero dejando
# todos los valores que estan en el nodo antiguio, solo si ese parametro
# no fue borrado.
import NatronGui
from PySide import QtCore
from natron_extent import get_parent, get_select_node, copy


def update_node():
    app = NatronGui.natron.getGuiInstance(0)

    node = get_select_node()

    _id = node.getPluginID()
    label = node.getLabel()
    parent = get_parent(node)
    position = node.getPosition()

    new_node = copy(node, parent)
    new_node.setPosition(position[0] + 200, position[1])
    new_node.setLabel(label)


NatronGui.natron.addMenuCommand('Videovina/Update Plugin', 'update_node.update_node',
                                QtCore.Qt.Key.Key_U, QtCore.Qt.KeyboardModifier.ShiftModifier)
