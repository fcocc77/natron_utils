import NatronEngine

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    param = thisNode.Dissolve1.which
    param = thisNode.Transform2.translate

    duration = thisNode.duration.get()
    exaggeration_time = thisNode.exaggeration.get()
    exaggeration_value = thisNode.exaggeration_value.get()    
    start_frame = thisNode.start_frame.get()
    values = [ thisNode.value_range.getValue(0), thisNode.value_range.getValue(1) ]

    transition(param, duration, exaggeration_time, exaggeration_value, start_frame, values)

def transition(param, duration, exaggeration_time, exaggeration_value, start_frame, values):
    
    exaggeration_value = 1 - exaggeration_value  
    
    first_frame = start_frame
    last_frame = first_frame + duration

    value_a = values[0]
    value_b = values[1]

    if value_a > value_b:
        value_range = value_a - value_b
    else:
        value_range = value_b - value_a

    # obtiene el valor de la exageracion dependiendo de la cantidad de frames de la transicion
    _exaggeration_time = ( duration / 2 ) * exaggeration_time
    # -------------------

    # obtiene el valor de la exageracion de valor dependiendo de la cantidad del valor
    _exaggeration_value = ( value_range / 2 ) * exaggeration_value
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

    param.restoreDefaultValue()

    param.setValueAtTime(value_a, first_frame)
    param.setValueAtTime(exaggeration_first_value, exaggeration_first)

    param.setValueAtTime(value_b, last_frame)
    param.setValueAtTime(exaggeration_last_value, exaggeration_last)

    param.setInterpolationAtTime(first_frame,  horizontal)
    param.setInterpolationAtTime(last_frame,  horizontal)
