import NatronEngine


def back_and_forth_transition(param, duration, start_frame, values):
    # transicion ida y vuelta

    first_frame = start_frame
    last_frame = first_frame + duration
    central_frame = (first_frame + last_frame) / 2

    value_a = values[0]
    value_b = values[1]

    for dimension in range(param.getNumDimensions()):
        param.restoreDefaultValue(dimension)

        param.setValueAtTime(value_a, first_frame, dimension)
        param.setValueAtTime(value_b, central_frame, dimension)
        param.setValueAtTime(value_a, last_frame, dimension)

        horizontal = NatronEngine.Natron.KeyframeTypeEnum.eKeyframeTypeHorizontal
        param.setInterpolationAtTime(first_frame,  horizontal, dimension)
        param.setInterpolationAtTime(central_frame,  horizontal, dimension)
        param.setInterpolationAtTime(last_frame,  horizontal, dimension)


def lineal_transition(param, start_frame, duration, values, dimension=None):
    if not dimension == None:
        directional_transition(param, duration, start_frame, values, 0, 0, dimension)
    else:
        for dimension in range(param.getNumDimensions()):
            directional_transition(param, duration, start_frame, values, 0, 0, dimension)


def directional_transition(param, duration, start_frame, values, exaggeration_time=0.7, exaggeration_value=0.7, dimension=0):

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
        # -------------------

        # obtiene el valor de la exageracion de valor dependiendo de la cantidad del valor
        _exaggeration_value = (value_range / 2) * exaggeration_value
        # -------------------

        exaggeration_first = first_frame + _exaggeration_time
        exaggeration_last = last_frame - _exaggeration_time

        if value_a > value_b:
            exaggeration_first_value = value_a - _exaggeration_value
            exaggeration_last_value = value_b + _exaggeration_value
        else:
            exaggeration_first_value = value_a + _exaggeration_value
            exaggeration_last_value = value_b - _exaggeration_value

        horizontal = NatronEngine.Natron.KeyframeTypeEnum.eKeyframeTypeHorizontal

        param.setValueAtTime(exaggeration_first_value,
                             exaggeration_first, dimension)
        param.setValueAtTime(exaggeration_last_value,
                             exaggeration_last, dimension)

        param.setInterpolationAtTime(first_frame,  horizontal, dimension)
        param.setInterpolationAtTime(last_frame,  horizontal, dimension)
