# Ordena solo la estructura de videovina
import os
import shutil
import NatronGui
from PySide import QtCore
from natron_extent import getNode, app
from slides import get_slides, get_slide_position
from develop import update_post_fx
from pictures import get_pictures


def sort():
    for obj in get_slides():
        slide = obj['slide']
        transition = obj['transition']
        dot = obj['dot']
        index = obj['index']

        posx = get_slide_position(index)[0]

        slide.setPosition(posx, 0)
        dot.setPosition(posx - 50, 100)
        transition.setPosition(posx, 200)

    for obj in get_pictures():
        image = obj['image']
        reformat = obj['reformat']
        index = obj['index']

        posx = get_slide_position(index)[0]

        image.setPosition(posx - 12, - 400)
        reformat.setPosition(posx, - 200)

    first_black = getNode(label='FirstBlack')
    first_black.setPosition(-200, 200)
    filter_dot = getNode(label='filter_dot')
    filter_dot.setPosition(-200, 100)

    update_post_fx()


NatronGui.natron.addMenuCommand('Videovina/Sort Template', 'sort.sort',
                                QtCore.Qt.Key.Key_X, QtCore.Qt.KeyboardModifier.ShiftModifier)
