import NatronEngine


def back_and_forth_animation(param, duration, start_frame, values, transition=100, input=True, output=True, dimension=None):
    # transicion ida y vuelta

    last_frame = start_frame + duration
    central_frame = (start_frame + last_frame) / 2

    if transition < 100:
        transition_duration = ((duration / 2) * transition) / 100

        a_first_frame = start_frame
        a_last_frame = transition_duration

        b_first_frame = last_frame - transition_duration
        b_last_frame = last_frame

    value_a = values[0]
    value_b = values[1]

    if dimension == None:
        dimensions = range(param.getNumDimensions())
    else:
        dimensions = [dimension]

    for dimension in dimensions:
        param.restoreDefaultValue(dimension)
        horizontal = NatronEngine.Natron.KeyframeTypeEnum.eKeyframeTypeHorizontal

        if transition < 100:
            if input:
                param.setValueAtTime(value_a, a_first_frame, dimension)
                param.setValueAtTime(value_b, a_last_frame, dimension)
                param.setInterpolationAtTime(a_first_frame,  horizontal, dimension)
                param.setInterpolationAtTime(a_last_frame,  horizontal, dimension)
            if output:
                param.setValueAtTime(value_b, b_first_frame, dimension)
                param.setValueAtTime(value_a, b_last_frame, dimension)
                param.setInterpolationAtTime(b_first_frame,  horizontal, dimension)
                param.setInterpolationAtTime(b_last_frame,  horizontal, dimension)

        else:
            if input:
                param.setValueAtTime(value_a, start_frame, dimension)
                param.setInterpolationAtTime(start_frame,  horizontal, dimension)

            param.setValueAtTime(value_b, central_frame, dimension)
            param.setInterpolationAtTime(central_frame,  horizontal, dimension)

            if output:
                param.setValueAtTime(value_a, last_frame, dimension)
                param.setInterpolationAtTime(last_frame,  horizontal, dimension)


def simple_animation(param, duration, start_frame, values, interpolation=[True, True], restore=True, dimension=None):

    if dimension == None:
        dimensions = range(param.getNumDimensions())
    else:
        dimensions = [dimension]

    for dimension in dimensions:
        first_frame = start_frame
        last_frame = first_frame + duration

        value_a = float(values[0])
        value_b = float(values[1])

        if restore:
            param.restoreDefaultValue(dimension)

        param.setValueAtTime(value_a, first_frame, dimension)
        param.setValueAtTime(value_b, last_frame, dimension)

        horizontal = NatronEngine.Natron.KeyframeTypeEnum.eKeyframeTypeHorizontal
        if interpolation[0]:
            param.setInterpolationAtTime(first_frame, horizontal, dimension)
        if interpolation[1]:
            param.setInterpolationAtTime(last_frame, horizontal, dimension)


def linear_animation(param, duration, start_frame, values, restore=True, dimension=None):
    simple_animation(param, duration, start_frame, values, interpolation=[False, False], restore=True, dimension=None)


def exaggerated_animation(
        param,
        duration,
        start_frame,
        values,
        exaggeration=[0.7, 0.7],
        dimension=None,
        key_frames=[True, True]):

    if not dimension == None:
        directional_animation(param, duration, start_frame, values, exaggeration, dimension, key_frames)
    else:
        for dimension in range(param.getNumDimensions()):
            directional_animation(param, duration, start_frame, values, exaggeration, dimension, key_frames)


def directional_animation(
        param,
        duration,
        start_frame,
        values,
        exaggeration=[0.7, 0.7],
        dimension=0,
        key_frames=[True, True]):

    exaggeration_time, exaggeration_value = exaggeration

    exaggeration_value = 1 - exaggeration_value

    first_frame = start_frame
    last_frame = first_frame + duration

    value_a = float(values[0])
    value_b = float(values[1])

    if value_a > value_b:
        value_range = value_a - value_b
    else:
        value_range = value_b - value_a

    param.restoreDefaultValue(dimension)

    param.setValueAtTime(value_a, first_frame, dimension)
    param.setValueAtTime(value_b, last_frame, dimension)

    if exaggeration_time > 0:
        # obtiene el valor de la exageracion dependiendo de la cantidad de frames de la transicion
        _exaggeration_time = (duration / 2) * exaggeration_time

        # obtiene el valor de la exageracion de valor dependiendo de la cantidad del valor
        _exaggeration_value = (value_range / 2) * exaggeration_value

        exaggeration_first = first_frame + _exaggeration_time
        exaggeration_last = last_frame - _exaggeration_time

        if value_a > value_b:
            exaggeration_first_value = value_a - _exaggeration_value
            exaggeration_last_value = value_b + _exaggeration_value
        else:
            exaggeration_first_value = value_a + _exaggeration_value
            exaggeration_last_value = value_b - _exaggeration_value

        horizontal = NatronEngine.Natron.KeyframeTypeEnum.eKeyframeTypeHorizontal

        if key_frames[0]:
            param.setValueAtTime(exaggeration_first_value, exaggeration_first, dimension)
            param.setInterpolationAtTime(first_frame, horizontal, dimension)

        if key_frames[1]:
            param.setValueAtTime(exaggeration_last_value, exaggeration_last, dimension)
            param.setInterpolationAtTime(last_frame, horizontal, dimension)
