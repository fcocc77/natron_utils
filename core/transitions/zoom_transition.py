import NatronEngine
from nx import getNode
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
    rscale = thisNode.getParam('rscale').get()

    duration = thisNode.getParam('duration').get()

    # animacion para el 'dissolve' solo con la mitad de la duracion
    mid_duration = duration / 2
    start_frame_dissolve = start_frame + (mid_duration / 2)
    exaggerated_animation(dissolve, mid_duration, start_frame_dissolve, [0.0, 2.0])

    src_blur = getNode(thisNode, 'src_blur')
    src_blur_param = src_blur.getParam('size')
    blur_size = thisNode.getParam('blur').get() * 2 * rscale
    exaggerated_animation(src_blur_param, duration, start_frame, [0, blur_size])

    src_transform = getNode(thisNode, 'src_transform')

    src_rotate_param = src_transform.getParam('rotate')
    src_rotate = thisNode.getParam('src_rotate').get()
    exaggerated_animation(src_rotate_param, duration, start_frame, [0.0, src_rotate])

    src_scale_param = src_transform.getParam('scale')
    src_scale = thisNode.getParam('src_scale').get()
    exaggerated_animation(src_scale_param, duration, start_frame, [1.0, src_scale])

    dst_transform = getNode(thisNode, 'dst_transform')

    dst_rotate_param = dst_transform.getParam('rotate')
    dst_rotate = thisNode.getParam('dst_rotate').get()
    exaggerated_animation(dst_rotate_param, duration, start_frame, [dst_rotate, 0])

    dst_scale_param = dst_transform.getParam('scale')
    dst_scale = thisNode.getParam('dst_scale').get()
    exaggerated_animation(dst_scale_param, duration, start_frame, [dst_scale, 1.0])
