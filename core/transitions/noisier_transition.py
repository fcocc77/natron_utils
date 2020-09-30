from base import link_to_parent, children_refresh, get_rscale, get_duration, get_format, get_start_frame, get_durations, limit_transition
from nx import getNode
from animations import exaggerated_animation, simple_animation
from vina import value_by_durations


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)
    durations = get_durations(thisNode)
    width, height = get_format(thisNode)
    start_frame = get_start_frame(thisNode)
    last_frame = start_frame + duration

    direction = thisNode.direction.get()

    # Imagenes Duplicadas
    duplicate_a = getNode(thisNode, 'duplicate_a')
    duplicate_b = getNode(thisNode, 'duplicate_b')

    duplicate_a_scale = duplicate_a.getParam('scale')
    duplicate_b_scale = duplicate_b.getParam('scale')

    duplicate_a_translate = duplicate_a.getParam('translate')
    duplicate_b_translate = duplicate_b.getParam('translate')
    #

    #

    # Transforms
    translate_a = getNode(thisNode, 'transform_a').getParam('translate')
    translate_b = getNode(thisNode, 'transform_b').getParam('translate')

    #

    translate_a.restoreDefaultValue(0)
    translate_a.restoreDefaultValue(1)

    translate_b.restoreDefaultValue(0)
    translate_b.restoreDefaultValue(1)
    #

    #
    exaggeration = [0.7, 0.7]
    if direction == 0:  # Left
        values_a = [0, -width]
        values_b = [width, 0]
        dimension = 0

        duplicate_a_translate.set(width, 0)
        duplicate_b_translate.set(-width, 0)

    elif direction == 1:  # Right
        values_a = [0, width]
        values_b = [-width, 0]
        dimension = 0

        duplicate_a_translate.set(-width, 0)
        duplicate_b_translate.set(width, 0)

    elif direction == 2:  # Up
        values_a = [0, -height]
        values_b = [height, 0]
        dimension = 1

        duplicate_a_translate.set(0, height)
        duplicate_b_translate.set(0, -height)

    elif direction == 3:  # Down
        values_a = [0, height]
        values_b = [-height, 0]
        dimension = 1

        duplicate_a_translate.set(0, -height)
        duplicate_b_translate.set(0, height)
    #

    if dimension == 0:
        duplicate_a_scale.set(-1, 1)
        duplicate_b_scale.set(-1, 1)
    else:
        duplicate_a_scale.set(1, -1)
        duplicate_b_scale.set(1, -1)

    exaggerated_animation(translate_a, duration, start_frame, values_a, exaggeration=exaggeration, dimension=dimension)
    exaggerated_animation(translate_b, duration, start_frame, values_b, exaggeration=exaggeration, dimension=dimension)
    #

    #

    # Noise
    noise_keyer = getNode(thisNode, 'noise_keyer')
    tolerance = noise_keyer.getParam('toleranceLower')

    noise_node = getNode(thisNode, 'noise')
    noise_translate = noise_node.getParam('transformTranslate')
    noise_scale = noise_node.getParam('transformScale')
    noise_size_param = noise_node.getParam('noiseSize')
    noise_z_slope = noise_node.getParam('noiseZSlope')

    evolution = thisNode.evolution.get() / 10
    evolution = value_by_durations(evolution, durations, reverse=True)[thisNode.speed.get()]
    noise_z_slope.set(evolution)

    noise_size = thisNode.noise_size.get() * rscale
    noise_size_param.set(noise_size, noise_size)

    noise_blur = getNode(thisNode, 'noise_blur').getParam('size')

    noise_translate.restoreDefaultValue(0)
    noise_translate.restoreDefaultValue(1)

    crushed = 1 - thisNode.crushed.get()
    blur_size = thisNode.dir_blur.get() * rscale
    if dimension == 0:
        noise_scale.set(1, crushed)
        noise_blur.set(blur_size, 0)
        noise_values = [values_a[0] * 1.5, values_a[1] * 1.5]

    else:
        noise_scale.set(crushed, 1)
        noise_blur.set(0, blur_size)
        noise_values = [values_b[0] * 1.5, values_b[1] * 1.5]

    exaggerated_animation(tolerance, duration, start_frame, [-0.8, -0.2], exaggeration=exaggeration)
    exaggerated_animation(noise_translate, duration, start_frame, noise_values, exaggeration=exaggeration, dimension=dimension)

    limit_transition(thisNode)
