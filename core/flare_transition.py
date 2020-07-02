from transition import directional_transition, back_and_forth_transition


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        set_transition(thisNode)


def set_transition(thisNode):
    duration = thisNode.duration.get()
    exaggeration_time = thisNode.exaggeration.get()
    exaggeration_value = thisNode.exaggeration_value.get()
    start_frame = thisNode.start_frame.get()
    rscale = thisNode.rscale.get()
    blur_size = thisNode.blur.get() * rscale
    values = [0.0, 1.0]

    dissolve = thisNode.Dissolve1.which
    flare_merge = thisNode.flare_merge.mix
    blur = thisNode.Blur.size

    directional_transition(dissolve, duration, exaggeration_time,
                           exaggeration_value, start_frame, values)
    back_and_forth_transition(flare_merge, duration, start_frame, [0, 1])
    back_and_forth_transition(blur, duration, start_frame, [0, blur_size])
