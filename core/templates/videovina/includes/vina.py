# datos del nodo de videovina
from natron_extent import app
from argparse import Namespace


def get_videovina():
    # obtiene el nodo principal de videovina
    for node in app().getChildren():
        if node.getPluginID() == 'vv.VideoVina':
            return node

    return None


def videovina_data():
    videovina_node = get_videovina()

    return Namespace(
        durations=videovina_node.getParam('durations').get(),
        transition_duration=videovina_node.getParam('transition_duration').get(),
        speed=videovina_node.getParam('speed').get(),
        pictures_amount=videovina_node.getParam('pictures_amount').get(),
        format=videovina_node.getParam('format').get(),
        color=videovina_node.getParam('color').get()
    )


def get_transition_duration():
    vina = videovina_data()

    normal_speed = vina.durations[1]
    slide_duration = vina.durations[vina.speed]

    # esta velocidad de frames corresponde a la velocidad normal,
    # y calculta la velocidad final dependiendo de la velocidad de la slide
    transition_frames = (slide_duration * vina.transition_duration) / normal_speed
    # -------------------------

    return transition_frames


def get_ranges(slide_count=None, speed=None):
    vina = videovina_data()

    if not speed:
        speed = vina.speed
    if not slide_count:
        slide_count = vina.pictures_amount

    slide_duration = vina.durations[speed]

    mid_transition_frames = get_transition_duration() / 2

    first_frame = 1
    last_frame = slide_duration + mid_transition_frames

    # genera una lista con cada rango, dependiendo de la duracion
    frame_range_list = []
    for index in range(slide_count + 1):
        frame_range_list.append((first_frame, last_frame))

        # si es el primer slide, le sumamos la mitad de la duracion de la transicion,
        # ya que la primera transicion va a negro.
        if index == 0:
            first_frame += slide_duration + mid_transition_frames
        else:
            first_frame += slide_duration
        last_frame += slide_duration
    # -------------------------------

    return frame_range_list
