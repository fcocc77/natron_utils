# Si un nodo plugin de videovina ya fue creado, esta opcion
# actualiza el nodo con los parametros nuevos pero dejando
# todos los valores que estan en el nodo antiguio, solo si ese parametro
# no fue borrado.
import NatronGui
from PySide import QtCore
from natron_extent import get_parent, get_select_node, copy, get_output_nodes, warning


def update_node():
    app = NatronGui.natron.getGuiInstance(0)

    node = get_select_node()

    if not node:
        warning('Update Node', 'Debe seleccionar un nodo.')
        return

    _id = node.getPluginID()
    label = node.getLabel()
    parent = get_parent(node)
    position = node.getPosition()

    node.setPosition(position[0] + 150, position[1])
    node.setColor(1, 0, 0)
    node.setLabel('delete_' + label)

    new_node = copy(node, parent)

    # conecta las entradas del antiguo nodo al nuevo nodo
    for i in range(node.getMaxInputCount()):
        input_node = node.getInput(i)
        if input_node:
            new_node.connectInput(i, input_node)
            node.disconnectInput(i)

    # conecta las nodos de salida
    for output_node, i in get_output_nodes(node):
        output_node.disconnectInput(i)
        output_node.connectInput(i, new_node)

    new_node.setPosition(position[0], position[1])
    new_node.setLabel(label)


NatronGui.natron.addMenuCommand('Videovina/Update Plugin', 'update_node.update_node',
                                QtCore.Qt.Key.Key_U, QtCore.Qt.KeyboardModifier.ShiftModifier)
