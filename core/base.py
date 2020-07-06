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
