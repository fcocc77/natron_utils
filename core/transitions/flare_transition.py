from animations import directional_animation, back_and_forth_animation


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

    directional_animation(dissolve, duration, start_frame, values, [exaggeration_time, exaggeration_value])
    back_and_forth_animation(flare_merge, duration, start_frame, [0, 1])
    back_and_forth_animation(blur, duration, start_frame, [0, blur_size])
