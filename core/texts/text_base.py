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


def transfer_transform(input_transform, output_transform, rscale=1):
    if not input_transform:
        return

    translate = input_transform.getParam('translate').get()
    translate_x = translate[0] * rscale
    translate_y = translate[1] * rscale

    center = input_transform.getParam('center').get()
    center_x = center[0] * rscale
    center_y = center[1] * rscale

    rotate = input_transform.getParam('rotate').get()
    scale = input_transform.getParam('scale').get()

    output_transform.getParam('translate').set(translate_x, translate_y)
    output_transform.getParam('center').set(center_x, center_y)
    output_transform.getParam('scale').set(scale[0], scale[1])
    output_transform.getParam('rotate').set(rotate)
