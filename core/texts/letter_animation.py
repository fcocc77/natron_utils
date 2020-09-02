from base import link_to_parent, children_refresh
from nx import getNode, app, createNode, node_delete
from text_base import set_font, fit_text_to_box
from util import hash_generator
from animations import lineal_animation


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)
    elif knob_name == 'text_generator':
        delete_text_nodes(thisNode)
        create_titles(thisNode)
    elif knob_name == 'texts_refresh':
        refresh_word(thisNode, 'title')
        refresh_word(thisNode, 'subtitle')


def refresh(thisNode):
    preview_text(thisNode)
    refresh_word(thisNode, 'title')
    refresh_word(thisNode, 'subtitle')


def get_text(thisNode, _type, index):
    _index = str(index)

    text = getNode(thisNode, 'text_' + _type + '_text_' + _index)
    local_transform = getNode(thisNode, 'text_' + _type + '_local_transform_' + _index)
    blur = getNode(thisNode, 'text_' + _type + '_blur_' + _index)
    transform = getNode(thisNode, 'text_' + _type + '_transform_' + _index)
    merge = getNode(thisNode, 'text_' + _type + '_merge_' + _index)

    if not text:
        return None

    return {
        'text': text,
        'local_transform': local_transform,
        'blur': blur,
        'transform': transform,
        'merge': merge,
        'index': index
    }


def get_texts(thisNode, _type):
    titles = []
    for i in range(100):
        title = get_text(thisNode, _type,  i)
        if not title:
            break

        titles.append(title)

    return titles


def create_titles(thisNode, only_refresh=False):

    title = thisNode.title.get()
    title_conection = getNode(thisNode, 'letter_transform_title')
    create_word(thisNode, title, title_conection, 'title')

    subtitle = thisNode.subtitle.get()
    subtitle_conection = getNode(thisNode, 'letter_transform_subtitle')
    create_word(thisNode, subtitle, subtitle_conection, 'subtitle')


def create_word(thisNode, text, conection, _type):
    idxs = range(len(text))

    # el desfase en el tiempo de las letras
    reverse = thisNode.letter_gap_direction.get()
    if (reverse):
        gaps = reversed(idxs)
    else:
        gaps = idxs

    pos = 0
    node_position = 1000
    last_letter_width = 0
    last_merge = None
    letter_index = 0
    for index, gap, letter in zip(idxs, gaps, text):
        # si la letra es un espacio agrega la posicion de la letra anterior
        # para que quede el espacio
        if letter == ' ':
            pos += last_letter_width
            continue

        last_merge, letter_width = create_letter(
            thisNode, letter.strip(), pos, gap, last_merge, _type, node_position, index
        )

        pos += letter_width
        node_position += 200
        last_letter_width = letter_width

    conection.connectInput(0, last_merge)


def create_letter(thisNode, letter, position, letter_gap, conection, _type, node_position, index):

    if _type == 'title':
        node_position_y = -1300
    else:
        node_position_y = -500

    # create text
    text = createNode(
        node='text',
        label='text_' + _type + '_text_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y]
    )
    text.getParam('text').set(letter)

    # Transform solo para rotacion y escala local
    local_transform = createNode(
        node='transform',
        label='text_' + _type + '_local_transform_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y + 100]
    )
    local_transform.connectInput(0, text)

    # Blur
    blur = createNode(
        node='blur',
        label='text_' + _type + '_blur_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y + 200]
    )
    blur.connectInput(0, local_transform)

    # Transform
    transform = createNode(
        node='transform',
        label='text_' + _type + '_transform_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y + 300]
    )
    transform.connectInput(0, blur)

    # Opacity Merge
    merge = createNode(
        node='merge',
        label='text_' + _type + '_merge_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y + 400]
    )

    merge.connectInput(1, transform)
    if conection:
        merge.connectInput(0, conection)
    else:
        crop = createNode(
            node='crop',
            label='text_' + _type + '_crop',
            group=thisNode,
            position=[node_position - 100, node_position_y + 500]
        )

        merge.connectInput(0, crop)
        crop.getParam('size').set(0, 0)

    letter_width = refresh_letter(thisNode, text, local_transform, blur, transform, merge,
                                  _type, letter_gap, position)

    return [merge, letter_width]


def refresh_word(thisNode, _type):

    titles = get_texts(thisNode, _type)
    idxs = range(len(titles))

    # el desfase en el tiempo de las letras
    reverse = thisNode.letter_gap_direction.get()
    if (reverse):
        gaps = reversed(idxs)
    else:
        gaps = idxs

    position = 0
    for letter, letter_gap in zip(titles, gaps):

        letter_width = refresh_letter(
            thisNode,
            letter['text'],
            letter['local_transform'],
            letter['blur'],
            letter['transform'],
            letter['merge'],
            _type, letter_gap, position)

        position += letter_width


def calculate_duration_and_gap(letters_amount, gap, duration):

    gap_amount = (gap * 100) / duration

    duration = duration - ((letters_amount * gap_amount) - gap_amount)

    return [duration, gap_amount]


def refresh_letter(thisNode, text, local_transform, blur, transform, merge,
                   _type, letter_gap_idx, position):
    # Actualiza las animaciones de todos los parametros del texto

    #

    # identifica si el titulo o subtitulo se desfasa primero
    word_gap = 0
    if thisNode.word_gap_word.get() == 0:
        if _type == 'title':
            word_gap = thisNode.word_gap.get()
    else:
        if _type == 'subtitle':
            word_gap = thisNode.word_gap.get()

    transition_duration = (thisNode.transition.get() * thisNode.duration.get()) / 100

    letter_gap_diff = thisNode.letter_gap.get()

    duration, letter_gap_diff = calculate_duration_and_gap(4, letter_gap_diff, transition_duration)

    letter_gap = letter_gap_idx * letter_gap_diff
    gap = thisNode.start_frame.get() + letter_gap + word_gap
    # ! falta desfase para las 3 duraciones

    start_frame = gap

    print duration

    #

    # Text
    text.getParam('size').set(get_size_font(thisNode, _type))
    font = thisNode.getParam('font').get()
    set_font(text, font)

    # las letras dependiendo de la fuente, se salen del bbox,
    # asi que se hace un calculo con el autoSize y luego se suma
    # el doble del ancho a la letra y asi no se sale
    text.getParam('autoSize').set(True)

    letter_width = text.getRegionOfDefinition(1, 1).x2
    letter_height = text.getRegionOfDefinition(1, 1).y2

    text.getParam('autoSize').set(False)

    new_letter_width = letter_width * 2
    text.getParam('canvas').set(new_letter_width, letter_height)

    move_to_rigth = letter_width / 2
    text.getParam('center').set(move_to_rigth, letter_height)

    #
    #
    #
    #

    # Text color
    text_color = thisNode.color.get()
    for i in range(3):
        text.getParam('color').setValue(text_color[i], i)

    # Local Transform
    angle = thisNode.getParam('displacement_angle').get()

    rotate_from = -angle + thisNode.getParam('rotate').get()
    rotate_to = -angle
    lineal_animation(local_transform.getParam('rotate'), start_frame, duration, [rotate_from, rotate_to])

    scale_from = thisNode.getParam('scale').get()
    scale_to = 1
    lineal_animation(local_transform.getParam('scale'), start_frame, duration, [scale_from, scale_to])

    local_transform.getParam('resetCenter').trigger()

    # Position para corregir el tranform del texto
    local_transform.getParam('translate').set(-move_to_rigth, 0)

    #
    #
    #
    #

    # Blur
    blur.getParam('cropToFormat').set(False)

    blur_x_from = thisNode.getParam('blur_x').get()
    lineal_animation(blur.getParam('size'), start_frame, duration, [blur_x_from, 0], dimension=0)

    blur_y_from = thisNode.getParam('blur_y').get()
    lineal_animation(blur.getParam('size'), start_frame, duration, [blur_y_from, 0], dimension=1)

    #
    #
    #
    #

    # Transform
    displacement = thisNode.getParam('displacement').get()

    translate = transform.getParam('translate')
    translate.setValue(0, 1)
    lineal_animation(translate, start_frame, duration, [position + displacement, position], dimension=0)

    rotate = transform.getParam('rotate')
    rotate.set(angle)

    center = transform.getParam('center')

    center_x = letter_width / 2
    center_y = letter_height / 2

    center_from = center_x - displacement
    center_to = center_x

    center.setValue(center_y, 1)
    lineal_animation(center, start_frame, duration, [center_from, center_to], dimension=0)

    #
    #
    #
    #

    # Merge
    opacity_from = thisNode.opacity.get()
    opacity_to = 1

    lineal_animation(merge.getParam('mix'), start_frame, duration, [opacity_from, opacity_to])

    return letter_width


def delete_text_nodes(thisNode):
    text_nodes = []
    for node in thisNode.getChildren():
        _node = node.getLabel().split('_')[0]

        if _node == 'text':
            text_nodes.append(node)

    node_delete(text_nodes)


def get_size_font(thisNode, _type):
    # calcula el tamanio de la fuente, despues que pasa por la escala de un 'Transform'

    if _type == 'title':
        src_size = thisNode.title_node.size.get()
    elif _type == 'subtitle':
        src_size = thisNode.subtitle_node.size.get()
    else:
        return 0

    scale = thisNode.General_Transform.scale.getValue()

    font_size = src_size * scale

    return font_size


def preview_text(thisNode):

    title = thisNode.title.get()
    subtitle = thisNode.subtitle.get()

    title_node = getNode(thisNode, 'title_node')
    subtitle_node = getNode(thisNode, 'subtitle_node')

    title_node.getParam('text').setValue(title)
    subtitle_node.getParam('text').setValue(subtitle)

    font = thisNode.getParam('font').get()

    set_font(title_node, font)
    set_font(subtitle_node, font)

    fit_text_to_box(thisNode)
