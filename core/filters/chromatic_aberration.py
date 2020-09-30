from base import link_to_parent, children_refresh, get_rscale, get_duration, get_format, get_start_frame, get_transition_duration
from nx import getNode
from animations import back_and_forth_animation


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
    start_frame = get_start_frame(thisNode)
    last_frame = start_frame + duration

    separation = thisNode.separation.get() * rscale
    orientation = thisNode.orientation.get()

    red_translate = getNode(thisNode, 'red_position').getParam('translate')
    blue_translate = getNode(thisNode, 'blue_position').getParam('translate')

    red_translate.restoreDefaultValue(0)
    red_translate.restoreDefaultValue(1)
    blue_translate.restoreDefaultValue(0)
    blue_translate.restoreDefaultValue(1)

    reverse_separation = thisNode.reverse_separation.get()

    # Animacion
    transition_duration = thisNode.transition_duration.get()
    if thisNode.with_animation.get():
        if not reverse_separation:
            red_values = [-separation, 0]
            blue_value = [separation, 0]
        else:
            red_values = [0, -separation]
            blue_value = [0, separation]

        back_and_forth_animation(red_translate, duration, start_frame, red_values, transition_duration, dimension=orientation)
        back_and_forth_animation(blue_translate, duration, start_frame, blue_value, transition_duration, dimension=orientation)
    else:
        red_translate.setValue(-separation, orientation)
        blue_translate.setValue(separation, orientation)
    #

    # Switch
    switch = getNode(thisNode, 'switch').getParam('which')
    switch.restoreDefaultValue()
    switch.set(1)
    if thisNode.with_animation.get():
        if not reverse_separation:
            if transition_duration < 100:
                transition_duration = get_transition_duration(thisNode)
                switch_frame_a = start_frame + transition_duration
                switch.setValueAtTime(1, switch_frame_a)
                switch.setValueAtTime(0, switch_frame_a + 1)

                switch_frame_b = last_frame - transition_duration

                switch.setValueAtTime(0, switch_frame_b)
                switch.setValueAtTime(1, switch_frame_b + 1)
