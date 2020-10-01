from nx import getNode, reload_all_read

from slide_common import setup


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    setup(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):

    # Correccion mask channels
    getNode(thisNode, 'edge_noise_merge').getParam('maskChannel_Mask').set(3)  # blue
    getNode(thisNode, 'pixels_grade').getParam('maskChannel_Mask').set(4)  # alpha
    getNode(thisNode, 'letter_merge').getParam('maskChannel_Mask').set(2)  # green
    getNode(thisNode, 'shapes_merge').getParam('maskChannel_Mask').set(1)  # red
    #

    reload_all_read(thisNode)
