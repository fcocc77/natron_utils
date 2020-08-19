import NatronEngine
from nx import getNode
# from base import *
from animations import exaggerated_animation


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    name = thisParam.getScriptName()

    if name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):

    dissolve = thisNode.Dissolve1.which
    start_frame = thisNode.getParam('start_frame').get()
    duration = thisNode.getParam('duration').get()

    exaggerated_animation(dissolve, duration, start_frame, [0.0, 1.0])

    src_transform = getNode(thisNode, 'src_transform')
    src_scale = src_transform.getParam('scale')
    exaggerated_animation(src_scale, duration, start_frame, [1.0, 0.5], key_frames=[True, True])

    dst_transform = getNode(thisNode, 'dst_transform')
    dst_scale = dst_transform.getParam('scale')
    exaggerated_animation(dst_scale, duration, start_frame, [2.0, 1.0], key_frames=[True, True])
