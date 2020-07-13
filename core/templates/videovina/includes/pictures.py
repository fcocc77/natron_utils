import os
import random
from slides import get_slides, get_slide, get_slide_position
from natron_extent import getNode, delete, app
from vv_misc import get_resolution


def generate_random_pictures(thisNode, app, workarea):
    amount = thisNode.getParam('pictures_amount').get()
    reformat = thisNode.getParam('reformat').get()

    references_dir = thisNode.reference_pictures.get()
    references_pictures = os.listdir(references_dir)
    references_count = len(references_pictures)

    indexs_without_repeat = random.sample(range(references_count), references_count)
    random_pictures = []

    index = 0
    for i in range(amount):
        picture_index = indexs_without_repeat[index]
        picture = references_dir + '/' + references_pictures[picture_index]
        random_pictures.append(picture)

        index += 1
        if index >= references_count:
            index = 0

    generate_pictures(thisNode, workarea, app, random_pictures, amount, reformat)


def generate_pictures(thisNode, workarea, app, pictures, amount, reformat_node=True):
    slides = get_slides(workarea)

    for index in range(amount):
        node_to_connect = None

        obj = get_slide(workarea, index)
        if obj:
            node_to_connect = obj['slide']
            node_to_connect.disconnectInput(0)

        posx = get_slide_position(index)[0]
        posy = get_slide_position(index)[1] - 400

        picture = pictures[index]

        reformat_name = 'slide_' + str(index) + '_reformat'
        reformat = getNode(workarea, reformat_name)
        if reformat_node:
            width, hight = get_resolution(thisNode)
            if not reformat:
                reformat = app.createNode('vv.ResolutionExpand', 2, workarea)
                reformat.setLabel(reformat_name)
                reformat.getParam('boxSize').set(width, hight)
                reformat.setColor(.5, .4, .4)

            reformat.setPosition(posx, - 200)
            if node_to_connect:
                node_to_connect.connectInput(0, reformat)
        else:
            if reformat:
                delete(reformat)

        # si la imagen ya fue generada, solo cambia el la imagen 'filename'
        reader_name = 'slide_' + str(index) + '_image'
        reader = getNode(workarea, reader_name)

        if reader:
            reader.getParam('filename').set(picture)
        else:
            reader = app.createReader(picture, workarea)
            reader.setLabel(reader_name)
            # deja la imagen con rgba para que no de conflicto, porque
            # a veces da conflicto al mezclar imagenes usando el shufle.
            reader.getParam('outputComponents').set(0)
            # ---------------------

        if reformat_node:
            reformat.connectInput(0, reader)
            reformat.getParam('refresh').trigger()
        else:
            if node_to_connect:
                node_to_connect.connectInput(0, reader)

        reader.setPosition(posx - 12, posy)


def get_picture(workarea, index):
    _index = str(index)

    image = getNode(workarea, 'slide_' + _index + '_image')
    reformat = getNode(workarea, 'slide_' + _index + '_reformat')

    if not image:
        return None

    return {
        'image': image,
        'reformat': reformat,
        'index': index
    }


def get_pictures(workarea=None):
    if not workarea:
        workarea = app()

    pictures = []
    for i in range(100):
        obj = get_picture(workarea, i)
        if obj:
            pictures.append(obj)

    return pictures
