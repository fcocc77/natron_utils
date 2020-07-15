from nx import getNode, createNode, warning
from base import *
from slide_base import generate_inputs


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    children_refresh(thisParam, thisNode)
    knob_name = thisParam.getScriptName()

    if knob_name == 'generate_inputs':
        generate_inputs(thisNode)
    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    None
