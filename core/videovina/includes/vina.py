# Datos solo del nodo de videovina,
# no incluir otras funcionalidades que no corresponda
# al nodo de videovina.
from nx import app
from argparse import Namespace


def get_videovina():
    # obtiene el nodo principal de videovina
    for node in app().getChildren():
        if node.getPluginID() == 'vv.VideoVina':
            return node

    return None


def get_videovina_render():
    for node in app().getChildren():
        if node.getPluginID() == 'vv.vinarender':
            input_node = node.getInput(0)
            if input_node:
                if input_node.getPluginID() == 'vv.VideoVina':
                    return node

    return None


def videovina_data():
    videovina_node = get_videovina()

    return Namespace(
        durations=videovina_node.getParam('durations').get(),
        total_slides=videovina_node.getParam('total_slides').get(),
        transition_duration=videovina_node.getParam('transition_duration').get(),
        speed=videovina_node.getParam('speed').get(),
        format=videovina_node.getParam('format').get(),
        color=videovina_node.getParam('color').get(),
        user=videovina_node.getParam('user').get(),
        project_name=videovina_node.getParam('project_name').get(),
        user_id=videovina_node.getParam('user_id').get(),
        song=videovina_node.getParam('song').get()
    )


def get_transition_duration():
    vina = videovina_data()

    normal_speed = vina.durations[1]
    slide_duration = vina.durations[vina.speed]

    # esta velocidad de frames corresponde a la velocidad normal,
    # y calcula la velocidad final dependiendo de la velocidad de la slide
    transition_frames = (slide_duration * vina.transition_duration) / normal_speed
    # -------------------------

    return transition_frames


def get_last_frame():
    vina = videovina_data()
    amount = vina.total_slides

    ranges = get_ranges(amount)
    if ranges:
        last_frame = ranges[-1][-1]
    else:
        last_frame = 0

    last_padding = 5  # Frames

    return last_frame + last_padding


def get_ranges_without_transition(slide_count):
    # obtiene todos los rangos a partir del 'get_reange()',
    # pero los rangos no se superponen, por causa de las transiciones.
    ranges = get_ranges_with_transition(slide_count)

    mid_transition_frames = get_transition_duration() / 2
    new_ranges = []

    last_last_frame = 0
    for i, _range in enumerate(ranges):
        first_frame = _range[0] + mid_transition_frames
        last_frame = _range[1] - mid_transition_frames

        # si es el primer y ultimo frames, los deja como estaban
        if i == 0:
            first_frame = _range[0]
        if i == len(ranges) - 1:
            last_frame = _range[1]

        # 'get_transition_duration()' calcula en int, por eso a veces,
        # el ultimo y primer frame pueden ser iguales, si son iguales le suma 1 al siguiente
        if last_last_frame == first_frame:
            first_frame += 1

        new_ranges.append((first_frame, last_frame))
        last_last_frame = last_frame

        i += 1

    return new_ranges


def get_ranges_with_transition(slide_count, speed=None):
    vina = videovina_data()

    if not speed:
        speed = vina.speed

    transition_frames = get_transition_duration()

    # le suma la duracion de la transicion de entrada y salida, a la duracion de la slide
    slide_duration = vina.durations[speed] + (transition_frames * 2)

    first_frame = 1
    last_frame = slide_duration

    transition_subtraction = 0

    # genera una lista con cada rango, dependiendo de la duracion
    frame_range_list = []
    for index in range(slide_count):

        # le resta la transicion, para que las 'slides' se superpongan
        frame_range_list.append((
            first_frame - transition_subtraction,
            last_frame - transition_subtraction
        ))

        transition_subtraction += transition_frames

        first_frame += slide_duration
        last_frame += slide_duration

    return frame_range_list


def get_ranges(slide_count, speed=None, transition=True):
    if transition:
        return get_ranges_with_transition(slide_count, speed)
    else:
        return get_ranges_without_transition(slide_count)
