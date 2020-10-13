import NatronEngine
from nx import getNode
from animations import simple_animation, back_and_forth_animation
from base import get_rscale, get_duration, reformat_update, limit_transition, children_refresh


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    children_refresh(thisParam, thisNode)
    name = thisParam.getScriptName()

    if name == 'refresh':
        refresh(thisNode)
    if name == 'reload_flares':
        getNode(thisNode, 'FlareTransition').getParam('reload_flares').trigger()


def refresh(thisNode):

    reformat_update(thisNode, 'reformat')

    start_frame = thisNode.getParam('start_frame').get()
    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)

    # Dissolve
    dissolve = getNode(thisNode, 'dissolve').getParam('which')
    simple_animation(dissolve, duration, start_frame, [0, 1])
    #
    #

    # Blur
    blur = getNode(thisNode, 'blur').getParam('size')
    blur_size = thisNode.blur.get() * rscale
    back_and_forth_animation(blur, duration, start_frame, [0, blur_size])
    #
    #

    limit_transition(thisNode, start_frame)
