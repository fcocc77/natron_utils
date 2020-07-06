from natron_extent import getNode, createNode, warning
from slide_base import generate_inputs


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'generate_inputs':
        generate_inputs(thisNode)
    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    subtle_move = getNode(thisNode, 'SubtleMove')
    subtle_move.getParam('refresh').trigger()
