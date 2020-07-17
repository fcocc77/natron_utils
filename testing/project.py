
import sys
from sys import argv
import NatronEngine

from slides import get_slides, get_slide
from log import slide_testing_log, testing_log


def testing(
        app=None,
        project=None,
        slide_range=None,
        format=None,
        speed=None):

    app.loadProject(project)

    # variables globales
    global slides
    slides = get_slides()
    # -----------------

    errors = 0

    errors += test_format(format)
    errors += test_speed(speed)
    errors += test_slide_range(slide_range)

    print 'Testing Error: ' + str(errors)


def test_slides(slide_node, param, value):
    errors = ''
    for i, slide in enumerate(slides):
        transition = slide[slide_node]
        if transition:
            if not transition.getParam(param).get() == value:
                errors += transition.getLabel() + ', '
        else:
            errors += 'No existe la Transicion ' + str(i) + ', '

    return errors


def test_speed(speed):
    speed_error = test_slides('transition', 'speed', speed)
    slide_testing_log('Speed', speed_error)

    if speed_error:
        return 1
    return 0


def test_format(format):
    format_error = test_slides('transition', 'format', format)
    slide_testing_log('Formato', format_error)

    if format_error:
        return 1
    return 0


def test_slide_range(slide_range):
    _range = range(slide_range[0], slide_range[1] + 1)

    error = 0

    # verifica si existe cada slide del rango entrante
    for i in _range:
        if not get_slide(index=i):
            error += 1
    # --------------------

    # si no esta el index de cada slide en el rango entrante, da error
    for slide in slides:
        index = slide['index']
        if not index in _range:
            error += 1
    # ----------------

    testing_log('Rango de slides', error, 0)

    error += testing_log('Cantidad de slides', len(slides), len(_range))

    return error
