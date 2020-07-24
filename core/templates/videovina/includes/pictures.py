import os
import random
from slides import get_slides, get_slide, get_slide_position
from nx import getNode, delete, app, alert
from vv_misc import get_resolution
from vina import get_videovina


def generate_random_pictures(thisNode, app, workarea):
    reformat = thisNode.getParam('reformat').get()
    random_pictures = thisNode.getParam('random_pictures').get()
    first_picture, last_picture = get_max_pictures()

    references_dir = thisNode.reference_pictures.get()
    references_pictures = os.listdir(references_dir)
    references_count = len(references_pictures)

    indexs_without_repeat = random.sample(range(references_count), references_count)
    pictures = []

    index = 0
    for i in range(last_picture + 1):
        if random_pictures:
            picture_index = indexs_without_repeat[index]
        else:
            picture_index = index

        picture = references_dir + '/' + references_pictures[picture_index]
        pictures.append(picture)

        index += 1
        if index >= references_count:
            index = 0

    generate_pictures(pictures, reformat_node=reformat)


def generate_pictures(pictures, pictures_amount=False, reformat_node=True):
    _app = app()
    workarea = _app
    vina_node = get_videovina()

    slides = get_slides(workarea)
    first_picture, last_picture = get_max_pictures()

    if pictures_amount:
        count = len(pictures)
        if last_picture >= count:
            last_picture = count - 1

    _range = range(first_picture, last_picture + 1)

    for index in _range:
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
            width, hight = get_resolution(vina_node)
            if not reformat:
                reformat = _app.createNode('vv.ResolutionExpand', 2, workarea)
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
            reader = _app.createReader(picture, workarea)
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


def get_index_last_picture():
    pictures = get_pictures()
    if len(pictures):
        return pictures[-1]['index']
    else:
        return 0


def get_max_pictures():
    # obtiene el rango maximo de imagenes que necesita para la cantidad de entradas de las slides.

    first_picture = 100000
    last_picture = -1

    for obj in get_slides():
        slide = obj['slide']
        index = obj['index']

        inputs = slide.getMaxInputCount()

        first = index - int(round(inputs / 2.0))
        if inputs > 0:
            first += 1

        if first < first_picture:
            first_picture = first

        last = index + inputs / 2
        if last > last_picture:
            last_picture = last

    if first_picture < 0:
        first_picture = 0

    return [first_picture, last_picture]
