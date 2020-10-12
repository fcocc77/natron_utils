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

    # Rectangle Mask

    rectangle_mask = getNode(thisNode, 'rectangle_mask')
    rectangle_mask_size = rectangle_mask.getParam('size')
    rectangle_mask_bottom_left = rectangle_mask.getParam('bottomLeft')

    mask_width = width / 1.25

    rectangle_mask_size.set(mask_width, height)
    mask_left = (width - mask_width) / 2
    rectangle_mask_bottom_left.set(mask_left, 0)
    #
    #

    # Transform de Imagen
    direction = thisNode.direction.get()

    image_transform = getNode(thisNode, 'image_transform')
    image_translate = image_transform.getParam('translate')
    image_transform.getParam('center').set(width / 2, height / 2)
    image_transform.getParam('scale').set(0.8, 0.8)
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
    back_scale.set(3, 3)
    back_position_x = width / 3
    if direction == 0:
        back_translate.set(back_position_x, 0)
    else:
        back_translate.set(-back_position_x, 0)
    #
    #
