from base import link_to_parent
from nx import getNode, app, createNode, node_delete, autocrop, bbox_bake, question
from text_base import set_font, transfer_transform
from text_fit import calcule_text_transform
from util import hash_generator
from animations import exaggerated_animation


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)
        refresh_word(thisNode, 'title')
        refresh_word(thisNode, 'subtitle')

    elif knob_name == 'text_generator':
        text_generator(thisNode)

    elif knob_name == 'texts_refresh':
        refresh_word(thisNode, 'title')
        refresh_word(thisNode, 'subtitle')

    elif knob_name == 'clear_text':
        if question('Seguro que desea borrar todas las letras?', 'Letters Delete'):
            delete_text_nodes(thisNode)

    elif knob_name == 'separated_by_letter':
        separated_by_letter(thisParam, thisNode)


def text_generator(thisNode):

    refresh(thisNode)
    delete_text_nodes(thisNode)
    create_titles(thisNode)


def refresh(thisNode):
    set_general_transform(thisNode)

    text_fit = getNode(thisNode, 'TextFit')
    text_fit.getParam('refresh').trigger()

    set_text_transform(thisNode, 'title')
    set_text_transform(thisNode, 'subtitle')

    refresh_output(thisNode)


def refresh_output(thisNode):

    input_transition = thisNode.getParam('input_transition').get()
    output_transition = thisNode.getParam('output_transition').get()

    # in_out_switch
    in_out_switch = getNode(thisNode, 'in_out_switch').getParam('which')

    if input_transition and output_transition:
        in_out_switch.set(1)
    elif input_transition:
        in_out_switch.set(0)
    elif output_transition:
        in_out_switch.set(2)

    # time
    frame_range = getNode(thisNode, 'FrameRange').getParam('frameRange')

    duration = thisNode.getParam('duration').get()
    start_frame = thisNode.getParam('start_frame').get()
    last_frame = start_frame + duration

    frame_range.set(start_frame, last_frame)

    switch = getNode(thisNode, 'switch_time_reverse').getParam('which')
    switch.restoreDefaultValue()
    mid_frame = last_frame - (duration / 2)
    switch.setValueAtTime(0, mid_frame)
    switch.setValueAtTime(1, mid_frame + 1)

    # se crea un crop 'bake' por que el nodo de retime en reversa, se queda pegado con bounding box
    if output_transition:
        crop_time_reverse = getNode(thisNode, 'crop_time_reverse')
        bbox_bake(crop_time_reverse, mid_frame, last_frame)


def separated_by_letter(thisParam, thisNode):
    letter_gap_param = thisNode.getParam('letter_gap')
    letter_gap_direction = thisNode.getParam('letter_gap_direction')

    separated = thisParam.get()

    letter_gap_param.setEnabled(separated)
    letter_gap_direction.setEnabled(separated)


def set_text_transform(thisNode, _type):
    general_transform = getNode(thisNode, 'general_transform')
    transform_title = getNode(thisNode, 'letter_transform_' + _type)

    text_fit = getNode(thisNode, 'TextFit')
    position = text_fit.getParam(_type + '_position').get()

    calcule_text_transform(transform_title, general_transform, position)


def set_general_transform(thisNode):
    input_transform = thisNode.getInput(0)

    general_transform = getNode(thisNode, 'general_transform')
    origina_input_transform = getNode(thisNode, 'origina_input_transform')

    transfer_transform(input_transform, general_transform, thisNode.rscale.get())
    transfer_transform(input_transform, origina_input_transform)


def get_text(thisNode, _type, index):
    _index = str(index)

    text = getNode(thisNode, 'text_' + _type + '_text_' + _index)
    crop = getNode(thisNode, 'text_' + _type + '_crop_' + _index)
    local_transform = getNode(thisNode, 'text_' + _type + '_local_transform_' + _index)
    blur = getNode(thisNode, 'text_' + _type + '_blur_' + _index)
    transform = getNode(thisNode, 'text_' + _type + '_transform_' + _index)
    merge = getNode(thisNode, 'text_' + _type + '_merge_' + _index)

    if not text:
        return None

    return {
        'text': text,
        'crop': crop,
        'local_transform': local_transform,
        'blur': blur,
        'transform': transform,
        'merge': merge,
        'index': index
    }


def get_texts(thisNode, _type):
    titles = []

    max_letter = 30

    has_letter = False
    for i in reversed(range(max_letter)):
        title = get_text(thisNode, _type,  i)

        if title:
            has_letter = True
        else:
            if has_letter:
                titles.append('space')
                continue
            else:
                continue

        titles.append(title)

    return list(reversed(titles))


def create_titles(thisNode, only_refresh=False):

    separated_by_letter = thisNode.separated_by_letter.get()

    title = thisNode.title.get()
    title_conection = getNode(thisNode, 'letter_transform_title')

    subtitle = thisNode.subtitle.get()
    subtitle_conection = getNode(thisNode, 'letter_transform_subtitle')

    if separated_by_letter:
        create_word(thisNode, title, title_conection, 'title')
        create_word(thisNode, subtitle, subtitle_conection, 'subtitle')
    else:
        create_one_word(thisNode, title, title_conection, 'title')
        create_one_word(thisNode, subtitle, subtitle_conection, 'subtitle')


def create_one_word(thisNode, text, conection, _type):
    # crea el texto sin separar por letras

    node_position = 1000
    last_merge, letter_width = create_letter(
        thisNode, text, 0, 0, None, _type, node_position, 0, 1
    )

    conection.connectInput(0, last_merge)


def create_word(thisNode, text, conection, _type):
    letters_amount = len(text)
    idxs = range(letters_amount)

    # el desfase en el tiempo de las letras
    reverse = thisNode.letter_gap_direction.get()
    if (reverse):
        gaps = reversed(idxs)
    else:
        gaps = idxs

    position = 0
    node_position = 1000
    last_merge = None
    letter_index = 0
    for index, gap, letter in zip(idxs, gaps, text):
        # si la letra es un espacio le suma una parte del tamanio de la fuente
        if letter == ' ':
            position += get_size_font(thisNode, _type) / 3
            continue

        last_merge, letter_width = create_letter(
            thisNode, letter.strip(), position, gap, last_merge, _type, node_position, index, letters_amount
        )

        position += letter_width
        node_position += 200

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

    # create crop
    crop = createNode(
        node='crop',
        label='text_' + _type + '_crop_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y + 100]
    )
    crop.connectInput(0, text)

    # Transform solo para rotacion y escala local
    local_transform = createNode(
        node='transform',
        label='text_' + _type + '_local_transform_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y + 200]
    )
    local_transform.connectInput(0, crop)

    # Blur
    blur = createNode(
        node='blur',
        label='text_' + _type + '_blur_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y + 300]
    )
    blur.connectInput(0, local_transform)

    # Transform
    transform = createNode(
        node='transform',
        label='text_' + _type + '_transform_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y + 400]
    )
    transform.connectInput(0, blur)

    # Opacity Merge
    merge = createNode(
        node='merge',
        label='text_' + _type + '_merge_' + str(index),
        group=thisNode,
        position=[node_position, node_position_y + 500]
    )

    merge.connectInput(1, transform)
    if conection:
        merge.connectInput(0, conection)
    else:
        first_crop = createNode(
            node='crop',
            label='text_' + _type + '_crop',
            group=thisNode,
            position=[node_position - 100, node_position_y + 600]
        )

        merge.connectInput(0, first_crop)
        first_crop.getParam('size').set(0, 0)

    letter_width = refresh_letter(thisNode, text, crop, local_transform, blur, transform, merge,
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

        if letter == 'space':
            position += get_size_font(thisNode, _type) / 3
            continue

        letter_width = refresh_letter(
            thisNode,
            letter['text'],
            letter['crop'],
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

    max_letter_gap_duration = transition_duration

    if letters_amount:
        max_letter_gap_duration /= letters_amount

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


def refresh_letter(thisNode, text, crop, local_transform, blur, transform, merge,
                   _type, letter_gap_idx, position, letters_amount):
    # Actualiza las animaciones de todos los parametros del texto

    def animation(param, values, dimension=None):
        duration, gap = calculate_duration_and_gap(thisNode, letters_amount, letter_gap_idx, _type)
        start_frame = gap

        exaggeration = [0.8, 0.7]
        key_frames = [False, True]

        exaggerated_animation(param, duration, start_frame, values, exaggeration, dimension=dimension, key_frames=key_frames)

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

    # Text color

    for i in range(3):
        if _type == 'title':
            text.getParam('color').setValue(thisNode.color.get()[i], i)
        else:
            text.getParam('color').setValue(thisNode.color_subtitle.get()[i], i)

    #
    #

    autocrop(thisNode, text, crop)
    crop.getParam('disableNode').set(True)

    #
    #

    # Local Transform
    angle = thisNode.getParam('displacement_angle').get()

    rotate_from = -angle + thisNode.getParam('rotate').get()
    rotate_to = -angle
    animation(local_transform.getParam('rotate'), [rotate_from, rotate_to])

    scale_from = thisNode.getParam('scale').get()
    scale_to = 1
    animation(local_transform.getParam('scale'), [scale_from, scale_to])

    local_transform.getParam('resetCenter').trigger()

    # Position para corregir el tranform del texto
    local_transform.getParam('translate').set(-move_to_rigth, 0)

    #
    #
    #
    #

    # Blur
    blur.getParam('cropToFormat').set(False)

    blur_x_from = thisNode.getParam('blur_x').get() * thisNode.rscale.get()
    animation(blur.getParam('size'), [blur_x_from, 0], dimension=0)

    blur_y_from = thisNode.getParam('blur_y').get() * thisNode.rscale.get()
    animation(blur.getParam('size'), [blur_y_from, 0], dimension=1)

    #
    #
    #
    #

    # Transform
    displacement = thisNode.getParam('displacement').get() * thisNode.rscale.get()

    translate = transform.getParam('translate')
    translate.setValue(0, 1)
    animation(translate, [position + displacement, position], dimension=0)

    rotate = transform.getParam('rotate')
    rotate.set(angle)

    center = transform.getParam('center')

    center_x = letter_width / 2
    center_y = letter_height / 2

    center_from = center_x - displacement
    center_to = center_x

    center.setValue(center_y, 1)
    animation(center, [center_from, center_to], dimension=0)

    #
    #
    #
    #

    # Merge
    opacity_from = thisNode.opacity.get()
    opacity_to = 1

    animation(merge.getParam('mix'), [opacity_from, opacity_to])

    #
    #
    #
    #

    crop.getParam('disableNode').set(False)

    #
    #
    #
    #

    return letter_width


def delete_text_nodes(thisNode):
    delete_nodes = []
    for node in thisNode.getChildren():
        _node = node.getLabel().split('_')[0]

        if _node == 'text':
            delete_nodes.append(node)

    autocrop_node = getNode(thisNode, 'autocrop')
    if autocrop_node:
        delete_nodes.append(autocrop_node)

    node_delete(delete_nodes)


def get_size_font(thisNode, _type):
    # calcula el tamanio de la fuente, despues que pasa por la escala de un 'Transform'

    text_fit = getNode(thisNode, 'TextFit')

    if _type == 'title':
        src_size = text_fit.getParam('font_size_title').get()
    elif _type == 'subtitle':
        src_size = text_fit.getParam('font_size_subtitle').get()
    else:
        return 0

    scale = thisNode.general_transform.scale.getValue()

    font_size = src_size * scale

    return font_size
