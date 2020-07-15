from nx import getNode
from text_base import generate_texts


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    generate_texts(thisNode)
