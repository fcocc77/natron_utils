from slide_common import setup
from base import get_rscale, get_format
from nx import getNode


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
    #
    #
