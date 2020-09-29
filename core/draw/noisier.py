from base import link_to_parent, children_refresh, get_rscale, get_duration, get_format, get_start_frame, get_durations
from nx import getNode
from animations import simple_animation
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
    width, height = get_format(thisNode)
    start_frame = get_start_frame(thisNode)
    last_frame = start_frame + duration
    durations = get_durations(thisNode)

    # Background
    background = getNode(thisNode, 'background')
    background.getParam('size').set(width, height)
    #

    # Noise
    noise = getNode(thisNode, 'noise')
    size_param = noise.getParam('noiseSize')
    z_slope = noise.getParam('noiseZSlope')

    size = thisNode.noise_size.get() * rscale
    size_param.set(size, size)

    evolution = thisNode.evolution.get() / 10
    evolution = value_by_durations(evolution, durations, reverse=True)[thisNode.speed.get()]

    z_slope.set(evolution)
    #

    # Repetir Transicion
    if thisNode.repeat_transition.get():
        duration = thisNode.repeat_duration.get() * (duration / 2) / 100

        start_frame_a = start_frame
        last_frame_a = start_frame_a + duration

        start_frame_b = last_frame - duration
        last_frame_b = start_frame_b + duration
    else:
        start_frame_a = start_frame
        last_frame_a = last_frame
    #

    # Keyer
    keyer = getNode(thisNode, 'keyer')
    tolerance_lower = keyer.getParam('toleranceLower')
    softness_lower = keyer.getParam('softnessLower')

    transition_duration = thisNode.transition_duration.get() * (duration / 2) / 100
    tolerance = 1 - thisNode.tolerance.get()

    tolerance_lower.restoreDefaultValue()
    tolerance_lower.set(-tolerance)

    if thisNode.input_transition.get():
        simple_animation(tolerance_lower, transition_duration, start_frame_a, [-1, -tolerance])
    if thisNode.output_transition.get():
        simple_animation(tolerance_lower, transition_duration, last_frame_a - transition_duration, [-tolerance, -1], restore=False)

    if thisNode.repeat_transition.get():
        if thisNode.output_transition.get():
            simple_animation(tolerance_lower, transition_duration, start_frame_b, [-1, -tolerance], restore=False)
        if thisNode.input_transition.get():
            simple_animation(tolerance_lower, transition_duration, last_frame_b - transition_duration, [-tolerance, -1], restore=False)

    smoothness = -thisNode.smoothness.get() / 2
    softness_lower.set(smoothness)
    #

    # Self Stencil
    stencil_offset = getNode(thisNode, 'offset_stencil').getParam('timeOffset')
    offset = thisNode.stencil_offset.get()

    offset = value_by_durations(offset, durations)[thisNode.speed.get()]
    stencil_offset.set(offset)

    stencil_switch = getNode(thisNode, 'stencil_switch').getParam('which')
    stencil_switch.set(thisNode.self_stencil.get())
    #
