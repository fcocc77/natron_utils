# funciones en comun que comparten todas las slides
from nx import getNode, createNode, warning
from base import children_refresh


def setup(thisParam, thisNode):
    children_refresh(thisParam, thisNode)
    knob_name = thisParam.getScriptName()

    if knob_name == 'generate_inputs':
        generate_inputs(thisNode)

    if knob_name == 'render':
        twelve_render(thisNode)


def twelve_render(thisNode):
    render = getNode(thisNode, 'TwelveRender')
    render.getParam('render').trigger()


def generate_inputs(thisNode):
    amount = thisNode.input_amount.getValue()
    count = thisNode.getMaxInputCount()

    if amount + 1 <= count:
        warning('Slide inputs', 'Ya existen ' + str(amount) + ' inputs extra.')
        return

    pos = getNode(thisNode, 'Image').getPosition()
    posx = pos[0] + 200
    pasy = pos[1]
    for i in range(amount):
        name = 'E-' + str(i + 1)
        _input = getNode(thisNode, name)
        if not _input:
            _input = createNode('input', name, thisNode, position=[posx, pasy])

        posx += 200