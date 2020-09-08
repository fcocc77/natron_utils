from base import link_to_parent, children_refresh
from text_base import set_font, transfer_transform
from nx import getNode, get_parent, createNode


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)

    elif knob_name == 'font_size_title':
        getNode(thisNode, 'title_node').getParam('size').set(thisParam.get())

    elif knob_name == 'font_size_subtitle':
        getNode(thisNode, 'subtitle_node').getParam('size').set(thisParam.get())

    elif knob_name == 'separate_text':
        separate_text(thisNode)


def refresh(thisNode):
    title_size, subtitle_size = fit_text_to_box(thisNode)

    thisNode.getParam('font_size_title').set(title_size)
    thisNode.getParam('font_size_subtitle').set(subtitle_size)

    input_transform = thisNode.getInput(0)
    general_transform = getNode(thisNode, 'General_Transform')

    transfer_transform(thisNode, input_transform, general_transform)


def fit_text_to_box(thisNode):

    title = thisNode.title.get()
    subtitle = thisNode.subtitle.get()

    title_node = getNode(thisNode, "title_node")
    subtitle_node = getNode(thisNode, "subtitle_node")

    title_node.getParam('text').setValue(title)
    subtitle_node.getParam('text').setValue(subtitle)

    font = thisNode.getParam('font').get()
    set_font(title_node, font)
    set_font(subtitle_node, font)

    current_format = thisNode.getParam('current_format').get()

    x = current_format[0]
    y = current_format[1]
    max_height = y / 2

    def font_resize(text):
        # reescala la fuente hasta que quede
        # del ancho del cuadro
        size_param = text.getParam('size')
        size_param.setValue(0)

        size = 10  # tamanio inicial
        width = 0
        height = 0
        while(width < x and height < max_height):
            size += 1
            size_param.setValue(size)
            width = text.getRegionOfDefinition(1, 1).x2
            height = text.getRegionOfDefinition(1, 1).y2

        return [size, width, height]

    title_size, title_x, title_y = font_resize(title_node)
    subtitle_size, subtitle_x, subtitle_y = font_resize(subtitle_node)

    # calcula el alto total, para poder centrar los 2 textos al cuadro
    height = title_y + subtitle_y
    move_up = (y - height) / 2

    title_translate = getNode(thisNode, "title_position_node").getParam('translate')
    subtitle_translate = getNode(thisNode, "subtitle_position_node").getParam('translate')

    title_position_param = thisNode.getParam('title_position')
    subtitle_position_param = thisNode.getParam('subtitle_position')

    # ajusta los titulos
    title_x_pos = (x / 2) - (title_x / 2)
    title_y_pos = subtitle_y + move_up

    title_translate.setValue(title_x_pos, 0)
    title_translate.setValue(title_y_pos, 1)

    title_position_param.setValue(title_x_pos, 0)
    title_position_param.setValue(title_y_pos, 1)

    # ajusta los subtitulos
    subtitle_x_pos = (x / 2) - (subtitle_x / 2)
    subtitle_y_pos = move_up

    subtitle_translate.setValue(subtitle_x_pos, 0)
    subtitle_translate.setValue(subtitle_y_pos, 1)

    subtitle_position_param.setValue(subtitle_x_pos, 0)
    subtitle_position_param.setValue(subtitle_y_pos, 1)

    return[title_size, subtitle_size]


def calcule_text_transform(transform_title, transform, position):
    # calcula los parametros de un Transform, a partir de un 'Transform' y un 'Position'

    for dimension in range(2):
        _position = position[dimension]
        scale = transform.getParam('scale').getValue(dimension)

        center = transform.getParam('center').getValue(dimension)
        translate = transform.getParam('translate').getValue(dimension)

        position_added = _position * scale
        new_position = position_added + translate + (center - (center * scale))
        new_center = (center * scale) - position_added

        new_position = _position * scale + translate + (center - (center * scale))

        transform_title.getParam('translate').setValue(new_position, dimension)
        transform_title.getParam('center').setValue(new_center, dimension)

    rotate = transform.getParam('rotate').getValue()
    transform_title.getParam('rotate').setValue(rotate)


def separate_text(thisNode):

    parent = get_parent(thisNode)
    pos_x, pos_y = thisNode.getPosition()
    general_transform = getNode(thisNode, 'General_Transform')
    scale = general_transform.getParam('scale').getValue()

    title = thisNode.title.get()
    subtitle = thisNode.subtitle.get()

    title_size = thisNode.font_size_title.get() * scale
    subtitle_size = thisNode.font_size_subtitle.get() * scale

    title_position = thisNode.getParam('title_position').get()
    subtitle_position = thisNode.getParam('subtitle_position').get()

    font = thisNode.getParam('font').get()

    title_node = getNode(parent, 'title_node')
    if not title_node:
        title_node = createNode(
            node='text',
            label='title_node',
            group=parent,
            position=[pos_x + 200, pos_y]
        )

    title_node.getParam('text').setValue(title)
    title_node.getParam('size').setValue(title_size)
    title_node.getParam('autoSize').set(True)
    set_font(title_node, font)

    subtitle_node = getNode(parent, 'subtitle_node')
    if not subtitle_node:
        subtitle_node = createNode(
            node='text',
            label='subtitle_node',
            group=parent,
            position=[pos_x + 400, pos_y]
        )

    subtitle_node.getParam('text').setValue(subtitle)
    subtitle_node.getParam('size').setValue(subtitle_size)
    subtitle_node.getParam('autoSize').set(True)
    set_font(subtitle_node, font)

    title_transform = getNode(parent, 'title_transform')
    if not title_transform:
        title_transform = createNode(
            node='transform',
            label='title_transform',
            group=parent,
            position=[pos_x + 200, pos_y + 50]
        )
    title_transform.connectInput(0, title_node)
    calcule_text_transform(title_transform, general_transform, title_position)

    subtitle_transform = getNode(parent, 'subtitle_transform')
    if not subtitle_transform:
        subtitle_transform = createNode(
            node='transform',
            label='subtitle_transform',
            group=parent,
            position=[pos_x + 400, pos_y + 50]
        )
    subtitle_transform.connectInput(0, subtitle_node)
    calcule_text_transform(subtitle_transform, general_transform, subtitle_position)

    merge = getNode(parent, 'titles_merge')
    if not merge:
        merge = createNode(
            node='merge',
            label='titles_merge',
            group=parent,
            position=[pos_x + 400, pos_y + 150]
        )

    merge.connectInput(0, title_transform)
    merge.connectInput(1, subtitle_transform)
