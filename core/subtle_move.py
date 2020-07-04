from natron_extent import getNode


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)


def animation(param, start_frame, duration, values, break_frame, break_duration, dimension=None):

    if dimension == None:
        dimensions = range(param.getNumDimensions())
    else:
        dimensions = [dimension]

    for dimension in dimensions:
        first_frame = start_frame
        last_frame = first_frame + duration

        value_a = float(values[0])
        value_b = float(values[1])

        param.restoreDefaultValue(dimension)

        param.setValueAtTime(value_a, first_frame, dimension)
        param.setValueAtTime(value_b, last_frame, dimension)

        first_frame_break = break_frame
        last_frame_break = break_frame + break_duration

        param.setValueAtTime(value_a/2, first_frame_break, dimension)
        param.setValueAtTime(value_b/2, last_frame_break, dimension)


def refresh(thisNode):
    transform = getNode(thisNode, 'Transform')
    scale = transform.getParam('scale')
    translate = transform.getParam('translate')
    center = transform.getParam('center')

    duration = thisNode.getParam('duration').get()
    start_frame = thisNode.getParam('start_frame').get()
    movement = thisNode.getParam('movement').get()
    level = thisNode.getParam('level').get()
    current_format = thisNode.getParam('current_format').get()
    rscale = thisNode.getParam('rscale').get()
    break_frame = thisNode.getParam('break_frame').get()
    break_duration = thisNode.getParam('break_frame_duration').get()

    width = current_format[0]
    height = current_format[1]

    param = translate
    translate_level = level * 50 * rscale

    # calcula la escala para que la translacion siempre quede dentro de cuadro
    scale_for_translate_x = ((translate_level * 2) / width) + 1
    scale_for_translate_y = ((translate_level * 2) / height) + 1
    # --------------------

    scale_level = 1 + (level * 0.2)
    if movement == 0:
        values = [-translate_level, translate_level, 0, scale_for_translate_x]
    if movement == 1:
        values = [translate_level, -translate_level, 0, scale_for_translate_x]
    if movement == 2:
        values = [translate_level, -translate_level, 1, scale_for_translate_y]
    if movement == 3:
        values = [-translate_level, translate_level, 1, scale_for_translate_y]
    if movement == 4:
        values = [1, scale_level, None, 0]
        param = scale
    if movement == 5:
        values = [scale_level, 1, None, 0]
        param = scale

    scale.restoreDefaultValue(0)
    scale.restoreDefaultValue(1)

    # translate
    translate.restoreDefaultValue(0)
    translate.restoreDefaultValue(1)
    center.set(width / 2, height / 2)
    scale.set(values[3], values[3])
    # ---------------------

    animation(param, start_frame, duration, [
        values[0], values[1]], break_frame, break_duration, dimension=values[2])
