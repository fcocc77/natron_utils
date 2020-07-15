import os
from nx import getNode, createNode


def generate_texts(thisNode):
    title = thisNode.getParam('title').get()
    subtitle = thisNode.getParam('subtitle').get()
    font = thisNode.getParam('font').get()
    titles = [title, subtitle]

    text_merge = getNode(thisNode, 'text_merge')
    if not text_merge:
        text_merge = createNode(
            'merge', 'text_merge', thisNode, position=[0, 200])

    posx = 0
    for i, text in enumerate(['title', 'subtitle']):
        text_node = getNode(thisNode, text)
        if not text_node:
            text_node = createNode(
                'text', text, thisNode, position=[posx, 0])
        text_node.getParam('text').set(titles[i])
        text_node.getParam('interactive').set(False)
        text_node.getParam('autoSize').set(True)
        text_node.getParam('centerInteract').set(True)
        text_node.getParam('custom').set(font)
        set_font(text_node, font)

        position_node = getNode(thisNode, text + '_position')
        if not position_node:
            position_node = createNode(
                'position', text + '_position', thisNode, position=[posx, 100])
        position_node.connectInput(0, text_node)

        text_merge.connectInput(i, position_node)

        posx += 200

    current_format = thisNode.getParam('current_format').get()
    fit_text_to_box(thisNode, current_format)


def set_font(text, font):
    basename = os.path.basename(font).split('.')[0].split(' ')[0]

    text.getParam('custom').setValue(font)
    text.getParam('custom').reloadFile()

    option = None
    for o in text.getParam('name').getOptions():
        if basename in o:
            option = o
            break

    text.getParam('name').set(option)


def fit_text_to_box(thisNode, format=[1920, 1080]):

    title = getNode(thisNode, "title")
    subtitle = getNode(thisNode, "subtitle")

    x = format[0]
    y = format[1]
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

    title_translate = getNode(thisNode, "title_position").getParam('translate')
    subtitle_translate = getNode(
        thisNode, "subtitle_position").getParam('translate')

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
