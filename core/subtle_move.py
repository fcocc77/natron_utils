from natron_extent import getNode
from transition import lineal_transition


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    transform = getNode(thisNode, 'Transform')
    scale = transform.getParam('scale')
    translate = transform.getParam('translate')

    duration = thisNode.getParam('duration').get()
    start_frame = thisNode.getParam('start_frame').get()
    movement = thisNode.getParam('movement').get()
    level = thisNode.getParam('level').get()

    param = translate
    translate_level = level * 100
    scale_level = 1 + (level * 0.4)
    if movement == 0:
        values = [0, translate_level]
        dimension = 0
    if movement == 1:
        values = [translate_level, 0]
        dimension = 0
    if movement == 2:
        values = [translate_level, 0]
        dimension = 1
    if movement == 3:
        values = [0, translate_level]
        dimension = 1
    if movement == 4:
        values = [1, scale_level]
        param = scale
        dimension = None
    if movement == 5:
        values = [scale_level, 1]
        param = scale
        dimension = None

    scale.restoreDefaultValue(0)
    scale.restoreDefaultValue(1)

    translate.restoreDefaultValue(0)
    translate.restoreDefaultValue(1)

    lineal_transition(param, start_frame, duration, values, dimension)
