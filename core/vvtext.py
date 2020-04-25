from util import *
from PySide.QtCore import QTimer

running = False


def main(thisParam, thisNode, thisGroup, app, userEdited):

    # defina la app y el nodo como variables globales,
    # para poder acceder de otras funcciones
    global _app
    global _thisNode
    global _thisParam
    global running

    _app = app
    _thisNode = thisNode
    _thisParam = thisParam
    # ----------------------

    if not running:
        running = True

        _thisNode.getParam('text_generator').setEnabled(False)
        _thisNode.getParam('refresh_param').setEnabled(False)

        QTimer.singleShot(0, main_timer)


def main_timer():
    button_name = _thisParam.getScriptName()
    if button_name == 'text_generator':
        delete_text_Nodes()
        preview_text()
        create_word()
    elif button_name == 'refresh_param':
        refresh_expression(_thisNode)
    elif button_name == 'fit_to_box':
        fit_text_to_box()

    debug_show()

    _thisNode.getParam('text_generator').setEnabled(True)
    _thisNode.getParam('refresh_param').setEnabled(True)

    global running
    running = False


def fit_text_to_box():

    title = _thisNode.getNode("title")
    subtitle = _thisNode.getNode("subtitle")

    x = 1920
    y = 1080
    max_height = y / 2

    def font_resize(text):
        # reescala la fuente hasta que quede
        # del ancho del cuadro
        size_param = text.getParam('size')
        size_param.setValue(0)

        size = 0
        width = 0
        height = 0
        while(width < x and height < max_height):
            size += 1
            size_param.setValue(size)
            width = text.getRegionOfDefinition(1, 1).x2
            height = text.getRegionOfDefinition(1, 1).y2

        return [width, height]

    title_x, title_y = font_resize(title)
    subtitle_x, subtitle_y = font_resize(subtitle)

    # calcula el alto total, para poder centrar los 2 textos al cuadro
    height = title_y + subtitle_y
    move_up = (y - height) / 2

    title_translate = _thisNode.getNode("title_position").getParam('translate')
    subtitle_translate = _thisNode.getNode(
        "subtitle_position").getParam('translate')

    # ajusta los textos verticalmente
    title_translate.setValue(subtitle_y + move_up, 1)
    subtitle_translate.setValue(move_up, 1)

    # centra los textos horizontalmente
    title_translate.setValue(
        (x / 2) - (title_x / 2), 0
    )
    subtitle_translate.setValue(
        (x / 2) - (subtitle_x / 2), 0
    )


def get_size_font():
    # calcula el tamanio de la fuente, despues que pasa por la escala de un 'Transform'

    src_size = _thisNode.title.size.get()
    scale = _thisNode.General_Transform.scale.getValue()

    font_size = src_size * scale

    return font_size


def refresh_expression(group):
    # cuando se modifica el parametro de origen de una expresion,
    # la expresion no actualiza, asi que esta funcion
    # recorre cada nodo del grupo y lo habilita y desabilita,
    # y con eso se actualiza todo el nodo.

    for node in group.getChildren():
        disableNode = node.getParam('disableNode')
        if disableNode:
            disable = disableNode.get()

            disableNode.set(not disable)
            disableNode.set(disable)


def createNode(name):
    nodes = {
        'blur': 'net.sf.cimg.CImgBlur',
        'text': 'net.fxarena.openfx.Text',
        'transform': 'net.sf.openfx.TransformPlugin',
        'merge': 'net.sf.openfx.MergePlugin',
        'output': 'fr.inria.built-in.Output',
        'position': 'net.sf.openfx.Position'
    }

    node_name = _app.createNode(nodes[name], -1, _thisNode).getScriptName()
    node = getattr(_thisNode, node_name)

    node.setScriptName('text_' + name + '_' + hash_generator(7))

    return node


def delete_text_Nodes():
    text_nodes = []
    for node in _thisNode.getChildren():
        _node = node.getScriptName().split('_')[0]

        if _node == 'text':
            text_nodes.append(node)
            node.destroy()

    # natron necesita que se borren 2 veces los nodos, por un error de natron
    for node in text_nodes:
        node.destroy()


def create_letter(letter, position, gap):

    # desfase en el tiempo para las expresiones
    curve_time = '.curve( frame - ' + str(gap) + \
        ' * thisGroup.delay_param.get() )'
    # ------------------------

    # create text
    text = createNode('text')
    text.text.set(letter)
    text.size.set(get_size_font())
    set_font(text)

    # las letras dependiendo de la fuente, se salen del bbox,
    # asi que se hace un calculo con el autoSize y luego se suma
    # el doble del ancho a la letra y asi no se sale
    text.autoSize.set(True)

    letter_width = text.getRegionOfDefinition(1, 1).x2
    letter_height = text.getRegionOfDefinition(1, 1).y2

    text.autoSize.set(False)

    new_letter_width = letter_width * 2
    text.canvas.set(new_letter_width, letter_height)
    # ---------------------------

    move_to_rigth = letter_width / 2
    text.center.set(move_to_rigth, letter_height)

    # Opacity expression
    opacity_exp = 'thisGroup.opacity_param' + curve_time
    for i in range(4):
        text.color.setExpression(opacity_exp, False, i)
    # ------------------------

    # Position para corregir el tranform del texto
    position_node = createNode('position')
    position_node.translate.set(- move_to_rigth, 0)
    position_node.connectInput(0, text)
    # ------------------------

    # Blur
    blur = createNode('blur')
    blur.cropToFormat.set(False)
    blur.connectInput(0, position_node)

    blur_exp = (
        'blur_x = thisGroup.blur_x_param' + curve_time + '\n'
        'blur_y = thisGroup.blur_y_param' + curve_time + '\n'
        'scale = thisGroup.resolution_scale.get() \n'
        'if dimension == 0: \n'
        '   ret = blur_x * scale \n'
        'else: \n'
        '   ret = blur_y * scale \n'
    )
    blur.size.setExpression(blur_exp, True, 0)
    blur.size.setExpression(blur_exp, True, 1)
    # ------------------

    # Transform solo para rotacion y escala local
    local_transform = createNode('transform')
    rotate_exp = (
        'rotate = thisGroup.rotate_param' + curve_time + '\n'
        'angle = thisGroup.angle_param' + curve_time + '\n'
        'ret = rotate - angle'
    )
    local_transform.rotate.setExpression(rotate_exp, True, 0)

    scale_exp = 'thisGroup.scale_param' + curve_time + ''
    local_transform.scale.setExpression(scale_exp, False, 0)
    local_transform.scale.setExpression(scale_exp, False, 1)

    local_transform.translate.setExpression('0', False, 0)
    local_transform.translate.setExpression('0', False, 1)

    local_transform.connectInput(0, blur)
    # --------------------

    # Transform
    transform = createNode('transform')
    translate_exp = (
        'translate = thisGroup.translate_param' + curve_time + ' \n'
        'translate = translate * thisGroup.resolution_scale.get() \n'
        'if dimension == 0: \n'
        '   ret = translate + ' + str(position) + '\n'
        'else: \n'
        '   ret = 0'
    )
    transform.translate.setExpression(translate_exp, True, 0)
    transform.translate.setExpression(translate_exp, True, 1)

    center_x = str(letter_width / 2)
    center_y = str(letter_height / 2)
    center_exp = (
        'translate = thisGroup.translate_param' + curve_time + ' \n'
        'translate = translate * thisGroup.resolution_scale.get() \n'
        'if dimension == 0: \n'
        '   ret = ' + center_x + ' - translate \n'
        'else: \n'
        '   ret = ' + center_y
    )
    transform.center.setExpression(center_exp, True, 0)
    transform.center.setExpression(center_exp, True, 1)

    angle_exp = 'thisGroup.angle_param' + curve_time
    transform.rotate.setExpression(angle_exp, False, 0)

    transform.connectInput(0, local_transform)
    # -----------------------------------

    return [transform, letter_width]


def set_font(text):
    font = _thisNode.custom_font.get()

    basename = os.path.basename(font).split('.')[0]

    option = basename[0] + '/' + basename

    text.getParam('custom').setValue(font)
    text.getParam('custom').reloadFile()
    text.getParam('name').set(option)


def preview_text():
    # nodos de titulos para la visualizacion de la caja

    title = _thisNode.text_param.get()
    subtitle = _thisNode.subtitle_param.get()

    title_node = _thisNode.getNode('title')
    subtitle_node = _thisNode.getNode('subtitle')

    title_node.getParam('text').setValue(title)
    subtitle_node.getParam('text').setValue(subtitle)

    set_font(title_node)
    set_font(subtitle_node)

    fit_text_to_box()


def create_word():

    merge = _thisNode.getNode("TextMerge")
    # -------------------

    title = _thisNode.text_param.get()
    subtitle = _thisNode.subtitle_param.get()

    idxs = range(len(title))

    # el desfase en el tiempo de las letras
    reverse = _thisNode.direction_param.get()
    if (reverse):
        gaps = reversed(idxs)
    else:
        gaps = idxs
    # ---------------

    pos = 0
    last_letter_width = 0
    for index, gap, letter in zip(idxs, gaps, title):
        # si la letra es un espacio agrega la posicion de la letra anterior
        # para que quede el espacio
        if letter == ' ':
            pos += last_letter_width
            continue
        # ------------------

        transform, letter_width = create_letter(letter.strip(), pos, gap)

        # la entrada numero 2 pertenece a la maskara, asi que la omite
        if index >= 2:
            index += 1

        merge.connectInput(index, transform)
        pos += letter_width
        last_letter_width = letter_width
