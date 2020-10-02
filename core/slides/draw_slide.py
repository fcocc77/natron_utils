from slide_common import setup
from base import get_rscale
from nx import getNode, reload_all_read


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    setup(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)

    # Desenfoque de Imagen
    photo_blur = getNode(thisNode, 'photo_blur')
    blur_size = 10 * rscale
    photo_blur.getParam('size').set(blur_size, blur_size)
    #

    # Desenfoque de 'ink'
    ink_blur = getNode(thisNode, 'ink_blur')
    blur_size = 200 * rscale
    ink_blur.getParam('size').set(blur_size, blur_size)
    #

    # Desenfoque de 'Noisier'
    noisier_blur = getNode(thisNode, 'noisier_blur')
    blur_size = 50 * rscale
    noisier_blur.getParam('size').set(blur_size, blur_size)
    #

    # Photo IDistort
    photo_idistort = getNode(thisNode, 'photo_idistort')
    distort_scale = 50 * rscale
    photo_idistort.getParam('uvScale').set(distort_scale, distort_scale)
    #

    # Noisier IDistort
    noisier_idistort = getNode(thisNode, 'noisier_idistort')
    distort_scale = 100 * rscale
    noisier_idistort.getParam('uvScale').set(distort_scale, distort_scale)
    #

    # Correccion mask channels
    getNode(thisNode, 'paint_merge').getParam('maskChannel_Mask').set(3)  # blue
    getNode(thisNode, 'edge_merge').getParam('maskChannel_Mask').set(2)  # green
    #

    reload_all_read(thisNode)
