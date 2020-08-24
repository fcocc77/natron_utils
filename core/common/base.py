from nx import alert, warning


def link_to_parent(thisNode, thisParam, thisGroup):
    # vincula algunos parametros al nodo padre

    if not thisParam.getScriptName() == 'link':
        return

    if not hasattr(thisGroup, 'getParam'):
        return

    params_count = 0

    format_parent = thisGroup.getParam('format')
    format_child = thisNode.getParam('format')
    if format_child and format_parent:
        params_count += 1
        format_child.set(format_parent.get())
        format_child.setExpression('thisGroup.format.get()', False)

    speed_parent = thisGroup.getParam('speed')
    speed_child = thisNode.getParam('speed')
    if speed_child and speed_parent:
        params_count += 1
        speed_child.set(speed_parent.get())
        speed_child.setExpression('thisGroup.speed.get()', False)

    durations_parent = thisGroup.getParam('durations')
    durations_child = thisNode.getParam('durations')
    if durations_child and durations_parent:
        params_count += 1
        for dimension in range(3):
            durations_value = durations_parent.get()[dimension]
            durations_child.setValue(durations_value, dimension)

            durations_exp = 'thisGroup.durations.get()[dimension]'
            durations_child.setExpression(durations_exp, False, dimension)

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
