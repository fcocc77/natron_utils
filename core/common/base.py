from nx import alert, warning


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)


def link_to_parent(thisNode, thisParam, thisGroup):
    # vincula algunos parametros al nodo padre

    if not thisParam.getScriptName() == 'link':
        return

    if not hasattr(thisGroup, 'getParam'):
        return

    params_count = 0

    def link(attribute):
        attribute_parent = thisGroup.getParam(attribute)
        attribute_child = thisNode.getParam(attribute)
        if attribute_child and attribute_parent:
            dimensions = attribute_parent.getNumDimensions()
            if dimensions == 1:
                attribute_child.set(attribute_parent.get())
                attribute_child.setExpression('thisGroup.' + attribute + '.get()', False)
            else:
                for dimension in range(dimensions):
                    attribute_child.setValue(attribute_parent.get()[dimension], dimension)
                    attribute_child.setExpression('thisGroup.' + attribute + '.getValue(dimension)', False, dimension)

            return 1
        return 0

    params_count += link('format')
    params_count += link('speed')
    params_count += link('motion_blur')
    params_count += link('durations')

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
