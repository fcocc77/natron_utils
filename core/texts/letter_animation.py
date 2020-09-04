from base import link_to_parent, children_refresh
from nx import getNode, app, createNode, node_delete
from text_base import set_font, fit_text_to_box
from util import hash_generator
from animations import exaggerated_animation


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

    set_general_transform(thisNode)

    preview_text(thisNode)
    refresh_word(thisNode, 'title')
    refresh_word(thisNode, 'subtitle')

    set_text_transform(thisNode, 'title')
    set_text_transform(thisNode, 'subtitle')


def set_text_transform(thisNode, _type):

    general_transform = getNode(thisNode, 'General_Transform')

    transform_title = getNode(thisNode, 'letter_transform_' + _type)

    for dimension in range(2):
        position = getNode(thisNode, _type + '_position').getParam('translate').getValue(dimension)
        scale = general_transform.getParam('scale').getValue(dimension)

        center = general_transform.getParam('center').getValue(dimension)
        translate = general_transform.getParam('translate').getValue(dimension)

        position_added = position * scale
        new_position = position_added + translate + (center - (center * scale))
        new_center = (center * scale) - position_added

        new_position = position * scale + translate + (center - (center * scale))

        transform_title.getParam('translate').setValue(new_position, dimension)
        transform_title.getParam('center').setValue(new_center, dimension)

    rotate = general_transform.getParam('rotate').getValue()
    transform_title.getParam('rotate').setValue(rotate)


def set_general_transform(thisNode):
    input_transform = thisNode.getInput(0)
    if not input_transform:
        return

    rscale = thisNode.rscale.get()

    general_transform = getNode(thisNode, 'General_Transform')

    translate = input_transform.getParam('translate').get()
    translate_x = translate[0] * rscale
    translate_y = translate[1] * rscale

    center = input_transform.getParam('center').get()
    center_x = center[0] * rscale
    center_y = center[1] * rscale

    rotate = input_transform.getParam('rotate').get()
    scale = input_transform.getParam('scale').get()

    general_transform.getParam('translate').set(translate_x, translate_y)
    general_transform.getParam('center').set(center_x, center_y)
    general_transform.getParam('scale').set(scale[0], scale[1])
    general_transform.getParam('rotate').set(rotate)


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
    letters_amount = len(text)
    idxs = range(letters_amount)

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
            thisNode, letter.strip(), pos, gap, last_merge, _type, node_position, index, letters_amount
        )

        pos += letter_width
        node_position += 200
        last_letter_width = letter_width

    conection.connectInput(0, last_merge)


def create_letter(thisNode, letter, position, letter_gap, conection, _type, node_position, index, letters_amount):

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
                                  _type, letter_gap, position, letters_amount)

    return [merge, letter_width]


def refresh_word(thisNode, _type):

    titles = get_texts(thisNode, _type)
    letters_amount = len(titles)
    idxs = range(letters_amount)

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
            _type, letter_gap, position, letters_amount)

        position += letter_width


def calculate_duration_and_gap(thisNode, letters_amount, letter_gap_idx, _type):

    transition_duration = (thisNode.transition.get() * thisNode.duration.get()) / 100

    letter_gap_percent = thisNode.letter_gap.get()
    word_gap_percent = thisNode.word_gap.get()

    max_word_gap_duration = transition_duration / 2  # el numero 2 es que hay 2; title y subtitle
    word_gap_amount = (max_word_gap_duration * word_gap_percent) / 100

    # es el numero maximo de desfase que puede haber dentro de la duracion
    letters_amount -= 1
    max_letter_gap_duration = transition_duration / letters_amount

    divide_by_two = (2 * word_gap_percent) / 100
    if divide_by_two:
        max_letter_gap_duration /= divide_by_two
    letter_gap_amount = (max_letter_gap_duration * letter_gap_percent) / 100

    duration = transition_duration - (letters_amount * letter_gap_amount) - word_gap_amount

    # identifica si el titulo o subtitulo se desfasa
    _word_gap = 0
    if thisNode.word_gap_word.get() == 0:
        if _type == 'title':
            _word_gap = word_gap_amount
    else:
        if _type == 'subtitle':
            _word_gap = word_gap_amount

    letter_gap = letter_gap_idx * letter_gap_amount
    gap = thisNode.start_frame.get() + letter_gap + _word_gap

    return [duration, gap]


def refresh_letter(thisNode, text, local_transform, blur, transform, merge,
                   _type, letter_gap_idx, position, letters_amount):
    # Actualiza las animaciones de todos los parametros del texto

    duration, gap = calculate_duration_and_gap(thisNode, letters_amount, letter_gap_idx, _type)
    start_frame = gap

    exaggeration = [0.8, 0.7]
    key_frames = [False, True]

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
    exaggerated_animation(local_transform.getParam('rotate'), duration, start_frame, [rotate_from, rotate_to], exaggeration, key_frames=key_frames)

    scale_from = thisNode.getParam('scale').get()
    scale_to = 1
    exaggerated_animation(local_transform.getParam('scale'), duration, start_frame, [scale_from, scale_to], exaggeration, key_frames=key_frames)

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
    exaggerated_animation(blur.getParam('size'), duration, start_frame, [blur_x_from, 0], exaggeration, dimension=0, key_frames=key_frames)

    blur_y_from = thisNode.getParam('blur_y').get()
    exaggerated_animation(blur.getParam('size'), duration, start_frame, [blur_y_from, 0], exaggeration, dimension=1, key_frames=key_frames)

    #
    #
    #
    #

    # Transform
    displacement = thisNode.getParam('displacement').get()

    translate = transform.getParam('translate')
    translate.setValue(0, 1)
    exaggerated_animation(translate, duration, start_frame, [position + displacement, position], exaggeration, dimension=0, key_frames=key_frames)

    rotate = transform.getParam('rotate')
    rotate.set(angle)

    center = transform.getParam('center')

    center_x = letter_width / 2
    center_y = letter_height / 2

    center_from = center_x - displacement
    center_to = center_x

    center.setValue(center_y, 1)
    exaggerated_animation(center, duration, start_frame, [center_from, center_to], exaggeration, dimension=0, key_frames=key_frames)

    #
    #
    #
    #

    # Merge
    opacity_from = thisNode.opacity.get()
    opacity_to = 1

    exaggerated_animation(merge.getParam('mix'), duration, start_frame, [opacity_from, opacity_to], exaggeration, key_frames=key_frames)

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

    current_format = thisNode.getParam('current_format').get()

    fit_text_to_box(thisNode, current_format)
