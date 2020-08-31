from nx import alert, warning
from vina import get_videovina
import NatronGui


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)


def link_to_parent(thisNode, thisParam, thisGroup):
    # vincula algunos parametros al nodo padre
    if not thisParam.getScriptName() == 'link':
        return

    # si el grupo es el root 'app', hace la vinculacion al nodo de videovina
    node_for_expression = 'thisGroup'
    if type(thisGroup) == NatronGui.GuiApp:
        videovina_node = get_videovina()

        if not videovina_node:
            return
        node_for_expression = videovina_node.getScriptName()
        thisGroup = videovina_node

    params_count = 0

    def link(attribute):
        attribute_parent = thisGroup.getParam(attribute)
        attribute_child = thisNode.getParam(attribute)
        if attribute_child and attribute_parent:
            if hasattr(attribute_child, 'set'):
                dimensions = attribute_parent.getNumDimensions()
                if dimensions == 1:
                    attribute_child.set(attribute_parent.get())
                    attribute_child.setExpression(node_for_expression + '.' + attribute + '.get()', False)
                else:
                    for dimension in range(dimensions):
                        attribute_child.setValue(attribute_parent.get()[dimension], dimension)
                        attribute_child.setExpression(node_for_expression + '.' + attribute + '.getValue(dimension)', False, dimension)

                return 1
        return 0

    for param in thisNode.getParams():
        page = param.getParent()
        if page:
            if page.getScriptName() == 'control':
                params_count += link(param.getScriptName())

    if params_count > 0:
        alert('Se vincularon ' + str(params_count) + ' parametros.')
    else:
        warning('Link Error', 'El nodo padre no tiene los atributos para vincularlo')


def children_refresh(thisParam, thisNode):
    # actualiza todos los nodos hijos, si presionamos el boton refresh,
    # y si es que el nodo hijo tiene el parametro de 'refresh'
    if not thisParam:
        return

    if thisParam.getScriptName() == 'refresh':
        for node in thisNode.getChildren():
            refresh = node.getParam('refresh')
            if refresh:
                refresh_expressions(thisNode)
                refresh.trigger()


def refresh_expressions(node):
    # A veces queda las expression con error, cuando cambiamos nombre u otra razon,
    # con esta funcion actualiazamos las expressiones

    for param in node.getParams():
        if hasattr(param, "getExpression"):
            for dimension in range(param.getNumDimensions()):
                exp, hasRetVariable = param.getExpression(dimension)
                if exp:
                    param.setExpression(exp, hasRetVariable)

    for child in node.getChildren():
        refresh_expressions(child)
