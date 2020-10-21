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

    # Texte overlay
    pre_transform = getNode(thisNode, 'pre_transform')
    text_transform = getNode(thisNode, 'text_transform')
    text_transform.getParam('resetCenter').trigger()

    scale = 1.0 / pre_transform.getParam('scale').get()[0]
    text_transform.getParam('scale').set(scale * 2, scale * 2)

    tx = pre_transform.getParam('translate').getValue(0) * rscale
    ty = pre_transform.getParam('translate').getValue(1) * rscale

    text_transform.getParam('translate').set(-tx, -ty)
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
