from natron_extent import warning


def link_to_parent(thisNode, thisParam, thisGroup):
    # vincula algunos parametros al nodo padre

    if not thisParam.getScriptName() == 'link':
        return

    if not hasattr(thisGroup, 'format'):
        warning('Link Error', 'El nodo padre no tiene los atributos para vincularlo')
        return

    _format = thisNode.getParam('format')
    _format.set(thisGroup.format.get())
    _format.setExpression('thisGroup.format.get()', False)

    speed = thisNode.getParam('speed')
    speed.set(thisGroup.speed.get())
    speed.setExpression('thisGroup.speed.get()', False)

    for dimension in range(3):
        durations = thisNode.getParam('durations')
        durations_value = thisGroup.durations.get()[dimension]
        durations.setValue(durations_value, dimension)
        durations_exp = 'thisGroup.durations.get()[dimension]'
        durations.setExpression(durations_exp, False, dimension)


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
