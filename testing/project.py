
import sys
from sys import argv
import NatronEngine

from slides import get_slides
from log import slide_testing_log, testing_log


def testing(
        app=None,
        project=None,
        slide_amount=None,
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
    errors += test_slide_amount(slide_amount)

    print errors


def test_speed(speed):
    speed_error = ''
    for i, slide in enumerate(slides):
        transition = slide['transition']
        if not transition.getParam('speed').get() == speed:
            speed_error += transition.getLabel() + ', '

    slide_testing_log('Speed', speed_error)

    if speed_error:
        return 1
    return 0


def test_format(format):
    format_error = ''
    for i, slide in enumerate(slides):
        transition = slide['transition']
        if not transition.getParam('format').get() == format:
            format_error += transition.getLabel() + ', '

    slide_testing_log('Formato', format_error)

    if format_error:
        return 1
    return 0


def test_slide_amount(slide_amount):
    return testing_log('Cantidad de slides', len(slides), slide_amount)
