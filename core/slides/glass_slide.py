from nx import getNode, createNode, warning
from base import *
from slide_common import setup


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    setup(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):

    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)

    # Texte overlay
    pre_transform = getNode(thisNode, 'pre_transform')
    text_transform = getNode(thisNode, 'text_transform')
    translate = text_transform.getParam('translate')
    text_transform.getParam('resetCenter').trigger()

    scale = 1.0 / pre_transform.getParam('scale').get()[0]
    text_transform.getParam('scale').set(scale * 2, scale * 2)

    tx = pre_transform.getParam('translate').getValue(0) * rscale
    ty = pre_transform.getParam('translate').getValue(1) * rscale

    # movimietos de background texto
    move = 500 * rscale

    if thisNode.align.get() == 1:
        tx_from = -tx - move
        tx_to = -tx + move
    else:
        tx_from = -tx + move
        tx_to = -tx - move

    translate.setValue(-ty, 1)

    translate.restoreDefaultValue(0)
    translate.setValueAtTime(tx_from, 1, 0)
    translate.setValueAtTime(tx_to, duration, 0)

    #
    #

    # include text
    text_merge = getNode(thisNode, 'text_merge').getParam('mix')
    text_overlap = getNode(thisNode, 'text_overlap').getParam('mix')

    if thisNode.include_text.get():
        text_merge.set(1)
        text_overlap.set(1)
    else:
        text_merge.set(0)
        text_overlap.set(0)
    #
    #
