import NatronEngine
from natron_extent import getNode


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)


def animation(param, values, start_frame, duration, bound=[0, False, False], dimension=None):
    value_a = float(values[0])
    value_b = float(values[1])

    first_frame = start_frame
    last_frame = first_frame + duration

    if dimension == None:
        dimensions = range(param.getNumDimensions())
    else:
        dimensions = [dimension]

    for dimension in dimensions:
        param.setValueAtTime(value_a, first_frame, dimension)
        param.setValueAtTime(value_b, last_frame, dimension)

        # bound key frame
        bound_value = (abs(value_a - value_b) / 3) * bound[0]
        bound_duration = duration / 3
        if value_a < value_b:
            bound_value_a = value_a - bound_value
            bound_value_b = value_b + bound_value
        else:
            bound_value_a = value_a + bound_value
            bound_value_b = value_b - bound_value

        if bound[1]:
            param.setValueAtTime(bound_value_a, first_frame +
                                 bound_duration, dimension)
        if bound[2]:
            param.setValueAtTime(bound_value_b, last_frame -
                                 bound_duration, dimension)

        horizontal = NatronEngine.Natron.KeyframeTypeEnum.eKeyframeTypeHorizontal
        param.setInterpolationAtTime(first_frame,  horizontal, dimension)
        param.setInterpolationAtTime(last_frame,  horizontal, dimension)


def refresh(thisNode):
    transform = getNode(thisNode, 'transform')
    translate = transform.getParam('translate')
    scale = transform.getParam('scale')
    center = transform.getParam('center')

    rscale = thisNode.getParam('rscale').get()
    start_frame = thisNode.getParam('start_frame').get()
    speed = thisNode.getParam('speed').get()
    input_move = thisNode.getParam('input_move').get()
    output_move = thisNode.getParam('output_move').get()
    duration = thisNode.getParam('duration').get()
    bound = thisNode.getParam('bound').get()
    durations = thisNode.getParam('durations').get()
    transition_duration_percent = thisNode.getParam(
        'transition_duration').get()

    current_format = thisNode.getParam('current_format').get()
    width = current_format[0]
    height = current_format[1]

    # restaurar valores
    translate.restoreDefaultValue(0)
    translate.restoreDefaultValue(1)
    scale.restoreDefaultValue(0)
    scale.restoreDefaultValue(1)

    # calcula la duracion de la transicion
    transition_duration = (transition_duration_percent * duration) / 100

    # bounding box input
    bbox = thisNode.getInput(0).getRegionOfDefinition(1, 1)
    input_width = abs(bbox.x1 - bbox.x2)
    input_height = abs(bbox.y1 - bbox.y2)

    center_x = bbox.x1 + (input_width / 2)
    center_y = bbox.y1 + (input_height / 2)

    center.set(center_x, center_y)

    value_x1 = -bbox.x2
    value_x2 = (width - bbox.x2) + input_width
    value_y1 = -bbox.y2
    value_y2 = (height - bbox.y2) + input_height

    # transicion de entrada
    def translate_input_anim(value, dimension=0):
        animation(translate, [value, 0], start_frame,
                  transition_duration, [bound, False, True], dimension=dimension)

    def scale_input_anim(value_a, value_b):
        animation(scale, [value_a, value_b], start_frame,
                  transition_duration, [bound, False, True])

    if input_move == 0:
        translate_input_anim(value_x1)
    elif input_move == 1:
        translate_input_anim(value_x2)
    elif input_move == 2:
        translate_input_anim(value_y1, 1)
    elif input_move == 3:
        translate_input_anim(value_y2, 1)

    elif input_move == 4:
        scale_input_anim(1, 0)
    elif input_move == 5:
        scale_input_anim(0, 1)

    # transicion de salida
    start_frame_output = duration - transition_duration

    def translate_output_anim(value, dimension=0):
        animation(translate, [0, value], start_frame_output,
                  transition_duration, [bound, True, False], dimension=dimension)

    def scale_output_anim(value_a, value_b):
        animation(scale, [value_a, value_b], start_frame_output,
                  transition_duration, [bound, True, False])

    if output_move == 0:
        translate_output_anim(value_x1)
    elif output_move == 1:
        translate_output_anim(value_x2)
    elif output_move == 2:
        translate_output_anim(value_y1, 1)
    elif output_move == 3:
        translate_output_anim(value_y2, 1)
    elif output_move == 4:
        scale_output_anim(1, 0)
    elif output_move == 5:
        scale_output_anim(0, 1)
