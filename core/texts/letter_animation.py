from base import link_to_parent, children_refresh
from nx import getNode, app
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
        create_titles(thisNode)


def refresh(thisNode):
    preview_text(thisNode)


def create_titles(thisNode):
    word_gap = thisNode.word_gap_first.get()

    title = thisNode.title.get()
    title_conection = getNode(thisNode, 'letter_transform_title')
    title_gap = False
    if word_gap == 0:
        title_gap = True
    create_word(thisNode, title, title_conection, title_gap, 'title')

    subtitle = thisNode.subtitle.get()
    subtitle_conection = getNode(thisNode, 'letter_transform_subtitle')
    subtitle_gap = False
    if word_gap == 1:
        subtitle_gap = True
    create_word(thisNode, subtitle, subtitle_conection, subtitle_gap, 'subtitle')


def create_word(thisNode, text, conection, word_gap, _type):
    idxs = range(len(text))

    # el desfase en el tiempo de las letras
    reverse = thisNode.letter_gap_direction.get()
    if (reverse):
        gaps = reversed(idxs)
    else:
        gaps = idxs

    pos = 0
    node_position = -1000
    last_letter_width = 0
    last_merge = None
    for index, gap, letter in zip(idxs, gaps, text):
        # si la letra es un espacio agrega la posicion de la letra anterior
        # para que quede el espacio
        if letter == ' ':
            pos += last_letter_width
            continue

        last_merge, letter_width = create_letter(
            thisNode, letter.strip(), pos, gap, word_gap, last_merge, _type, node_position
        )

        # la entrada numero 2 pertenece a la maskara, asi que la omite
        if index >= 2:
            index += 1

        pos += letter_width
        node_position += 200
        last_letter_width = letter_width

    conection.connectInput(0, last_merge)


def create_letter(thisNode, letter, position, letter_gap, word_gap, conection, _type, node_position):

    gap = letter_gap * thisNode.letter_gap.get()
    # ! falta desfase para las 3 duraciones

    start_frame = gap
    duration = 50

    # desfase en el tiempo para las expresiones
    word_gap_exp = '0'
    if word_gap:
        word_gap_exp = 'thisGroup.word_gap.get()'

    curve_time = '.curve( frame - (' + str(letter_gap) + \
        ' * thisGroup.letter_gap.get() ) - ' + word_gap_exp + ' )'
    # ------------------------

    # create text
    text = createNode(thisNode, 'text')
    text.setPosition(node_position, 0)
    text.text.set(letter)
    text.size.set(get_size_font(thisNode, _type))
    font = thisNode.getParam('font').get()
    set_font(text, font)

    # las letras dependiendo de la fuente, se salen del bbox,
    # asi que se hace un calculo con el autoSize y luego se suma
    # el doble del ancho a la letra y asi no se sale
    text.autoSize.set(True)

    letter_width = text.getRegionOfDefinition(1, 1).x2
    letter_height = text.getRegionOfDefinition(1, 1).y2

    text.autoSize.set(False)

    new_letter_width = letter_width * 2
    text.canvas.set(new_letter_width, letter_height)

    move_to_rigth = letter_width / 2
    text.center.set(move_to_rigth, letter_height)

    # Text color
    color_exp = 'thisGroup.color.getValue(dimension)'
    for i in range(3):
        text.color.setExpression(color_exp, False, i)

    # Transform solo para rotacion y escala local
    local_transform = createNode(thisNode, 'transform')
    local_transform.setPosition(node_position, 100)

    angle = thisNode.getParam('displacement_angle').get()

    rotate_from = -angle + thisNode.getParam('rotate').get()
    rotate_to = -angle
    lineal_animation(local_transform.rotate, start_frame, duration, [rotate_from, rotate_to])

    scale_from = thisNode.getParam('scale').get()
    scale_to = 1
    lineal_animation(local_transform.scale, start_frame, duration, [scale_from, scale_to])

    # Position para corregir el tranform del texto
    local_transform_exp = '-' + str(move_to_rigth)

    local_transform.translate.setExpression(local_transform_exp, False, 0)
    local_transform.translate.setExpression('0', False, 1)

    local_transform.connectInput(0, text)

    # Blur
    blur = createNode(thisNode, 'blur')
    blur.setPosition(node_position, 200)
    blur.cropToFormat.set(False)
    blur.connectInput(0, local_transform)

    blur_x_from = thisNode.getParam('blur_x').get()
    lineal_animation(blur.size, start_frame, duration, [blur_x_from, 0], dimension=0)

    blur_y_from = thisNode.getParam('blur_y').get()
    lineal_animation(blur.size, start_frame, duration, [blur_y_from, 0], dimension=1)

    # ------------------

    # Transform
    transform = createNode(thisNode, 'transform')
    transform.setPosition(node_position, 300)

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

    transform.connectInput(0, blur)
    # -----------------------------------

    # Opacity expression
    merge = createNode(thisNode, 'merge')
    merge.setPosition(node_position, 400)

    opacity_from = thisNode.opacity.get()
    opacity_to = 1

    lineal_animation(merge.mix, start_frame, duration, [opacity_from, opacity_to])

    merge.connectInput(1, transform)
    if conection:
        merge.connectInput(0, conection)
    else:
        crop = createNode(thisNode, 'crop')
        crop.setPosition(node_position - 100, 500)
        crop.getParam('size').set(0, 0)
        merge.connectInput(0, crop)
    # ------------------------

    return [merge, letter_width]


def createNode(thisNode, name):
    nodes = {
        'blur': 'net.sf.cimg.CImgBlur',
        'text': 'net.fxarena.openfx.Text',
        'transform': 'net.sf.openfx.TransformPlugin',
        'merge': 'net.sf.openfx.MergePlugin',
        'output': 'fr.inria.built-in.Output',
        'position': 'net.sf.openfx.Position',
        'crop': 'net.sf.openfx.CropPlugin'
    }

    _app = app()
    node_name = _app.createNode(nodes[name], -1, thisNode).getScriptName()
    node = getattr(thisNode, node_name)

    node.setScriptName('text_' + name + '_' + hash_generator(7))

    return node


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
