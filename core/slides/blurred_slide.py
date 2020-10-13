from slide_common import setup
from nx import getNode
from base import get_rscale, get_format


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    setup(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    width, height = get_format(thisNode)

    hard_shape = thisNode.hard_shape.get()

    # Rectangle Mask
    rectangle_mask = getNode(thisNode, 'mask_rectangle')

    width_percent = 80
    rectangle_mask.getParam('width').set(width_percent)

    softness_param = rectangle_mask.getParam('softness')
    if hard_shape:
        softness_param.set(0)
    else:
        softness_param.set(500)

    rectangle_mask.getParam('refresh').trigger()
    #
    #

    # Transform de Imagen
    direction = thisNode.direction.get()

    image_transform = getNode(thisNode, 'image_transform')
    image_translate = image_transform.getParam('translate')
    image_transform.getParam('center').set(width / 2, height / 2)
    image_scale = image_transform.getParam('scale')

    if hard_shape:
        image_scale.set(.8, .8)
    else:
        image_scale.set(1, 1)

    mask_left = width - (width * width_percent / 100)
    mask_left /= 2
    if direction == 0:
        image_translate.set(-mask_left, 0)
    else:
        image_translate.set(mask_left, 0)
    #
    #

    # Background
    background_transform = getNode(thisNode, 'background_transform')
    back_scale = background_transform.getParam('scale')
    back_center = background_transform.getParam('center')
    back_translate = background_transform.getParam('translate')

    back_center.set(width / 2, height / 2)
    scale_size = 2
    back_scale.set(scale_size, scale_size)
    back_position_x = width / 3
    if direction == 0:
        back_translate.set(back_position_x, 0)
    else:
        back_translate.set(-back_position_x, 0)
    #
    #

    # omni_reflect switch
    omni_reflect = getNode(thisNode, 'omni_reflect_switch').getParam('which')
    if hard_shape:
        omni_reflect.set(0)
    else:
        omni_reflect.set(1)
    #
    #
