from slide_common import setup
from base import get_rscale, get_format
from nx import getNode
import random


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)

    setup(thisParam, thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    width, height = get_format(thisNode)

    # Ajuste en escala para que no queden bordes negros en el background
    background_transform = getNode(thisNode, 'background_transform')
    scale = 1.2
    background_transform.getParam('scale').set(scale, scale)
    background_transform.getParam('center').set(width / 2, height / 2)
    #
    #

    # gradiente para el blur
    ramp = getNode(thisNode, 'ramp')
    ramp.getParam('point1').set(0, height)
    #
    #

    # Ajusto de cuatro de fotos
    photo_frame = getNode(thisNode, 'PhotoFrame')

    meta_a_suffix = photo_frame.getParam('meta_a_suffix')
    meta_b_suffix = photo_frame.getParam('meta_b_suffix')

    if width == 960:
        meta_a_suffix.set('Half HD')
        meta_b_suffix.set('960 x 540')
    elif width == 1920:
        meta_a_suffix.set('HD')
        meta_b_suffix.set('1920 x 1080')
    else:
        meta_a_suffix.set('4K')
        meta_b_suffix.set('3840 x 2160')

    colorize = getNode(thisNode, 'colorize').getParam('white')
    for dimension in range(3):
        color = thisNode.color.getValue(dimension)

        colorize.setValue(color, dimension)
        photo_frame.getParam('title_color').setValue(color, dimension)
        photo_frame.getParam('symbol_color').setValue(color, dimension)
    #
    #

    # Fotos Extras
    extra_colorize = getNode(thisNode, 'extra_colorize')
    if not extra_colorize:
        return
    colorize_white = extra_colorize.getParam('white')
    for dimension in range(3):
        color = thisNode.color.getValue(dimension)
        colorize_white.setValue(color, dimension)

    extra_blur = getNode(thisNode, 'extra_blur')
    blur_size = 2 * rscale
    extra_blur.getParam('size').set(blur_size, blur_size)

    i = 0
    for name_transform in ['transform_1', 'transform_2']:

        transform = getNode(thisNode, name_transform)
        if not transform:
            continue
        translate = transform.getParam('translate')
        rotate = transform.getParam('rotate')
        scale = transform.getParam('scale')
        center = transform.getParam('center')

        center.set(width / 2, height / 2)
        translate.set(0, 0)
        scale.set(.4, .4)

        random.seed(thisNode.seed.get() + i)
        max_rotate = 20
        rotate_value = random.randint(-max_rotate, max_rotate)
        rotate.set(rotate_value)

        # Separacion
        separation = 700 * rscale
        if i == 0:
            translate.set(-separation, 0)
        else:
            translate.set(separation, 0)

        i += 1
