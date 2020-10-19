from base import link_to_parent, get_rscale, get_duration, get_format, reformat_update
from nx import getNode, warning
from text_fit import separate_text, get_bbox_format, get_bbox
import random


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)

    input_node = thisNode.getInput(0)
    if input_node.getPluginID() == 'fr.inria.built-in.Input':
        warning('error', 'El nodo a conectar no puede ser un "Input"')
        return

    bbox_format = get_bbox_format(input_node)

    shadow_node = getNode(thisNode, 'shadow')
    shadow_switch = getNode(thisNode, 'shadow_switch').getParam('which')
    disable_shadow = shadow_node.getParam('disableNode')
    inside_shadow_node = getNode(thisNode, 'shadow_inside')
    inside_shadow_switch = getNode(thisNode, 'shadow_inside_switch').getParam('which')

    # se desabilita la sombra, por que modifica el bbox,
    # y se descuadre todo lo demas.
    shadow_switch.set(0)
    inside_shadow_switch.set(0)

    to_frame(thisNode, rscale, bbox_format)
    adjust_metadata(thisNode, rscale, bbox_format)

    shadow_switch.set(1)
    inside_shadow_switch.set(1)

    shadow_node.getParam('refresh').trigger()
    inside_shadow_node.getParam('refresh').trigger()


def get_frame_width(thisNode, bbox_format, rscale):

    frame_width = thisNode.frame_width.get() * rscale

    vertical = bbox_format[0] < bbox_format[1]
    if vertical:
        aspect = float(bbox_format[1]) / bbox_format[0]
        frame_width *= aspect

    return frame_width


def to_frame(thisNode, rscale, bbox_format):

    corner_radius = thisNode.corner_radius.get() * rscale
    bottom_margin = bbox_format[1] * thisNode.bottom_margin.get() / 100

    rectangle = getNode(thisNode, 'rectangle')
    rectangle_height = bbox_format[1] + bottom_margin
    rectangle.getParam('cornerRadius').set(corner_radius, corner_radius)

    rectangle.getParam('size').set(bbox_format[0], rectangle_height)
    rectangle.getParam('bottomLeft').set(0, -bottom_margin)

    #
    #

    frame_width = get_frame_width(thisNode, bbox_format, rscale)

    photo_mask = getNode(thisNode, 'photo_mask')
    photo_mask_width = bbox_format[0] - frame_width
    width_residue = bbox_format[0] - photo_mask_width
    photo_mask_height = bbox_format[1] - width_residue

    photo_mask_left = (bbox_format[0] - photo_mask_width) / 2
    photo_mask_bottom = (bbox_format[1] - photo_mask_height) / 2

    photo_mask.getParam('size').set(photo_mask_width, photo_mask_height)
    photo_mask.getParam('bottomLeft').set(photo_mask_left, photo_mask_bottom)
    photo_mask.getParam('cornerRadius').set(corner_radius, corner_radius)

    #
    #

    text_bbox = getNode(thisNode, 'text_bbox')
    text_width = photo_mask_width
    text_height = bottom_margin

    text_left = photo_mask_left
    text_bottom = -bottom_margin

    bottom_height = abs(text_bottom - photo_mask_bottom)

    text_bottom += (bottom_height - text_height) / 2

    text_bbox.getParam('size').set(text_width, text_height)
    text_bbox.getParam('bottomLeft').set(text_left, text_bottom)

    text_fit = getNode(thisNode, 'text_fit')
    text_fit.getParam('refresh').trigger()
    separate_text(text_fit, thisNode)

    set_text_color(thisNode)

    adjust_photo_transform(thisNode, [photo_mask_width, photo_mask_height], bbox_format)
    adjust_output_transform(thisNode)


def set_text_color(thisNode):
    getNode(thisNode, 'title_node').getParam('color').copy(thisNode.title_color)
    getNode(thisNode, 'subtitle_node').getParam('color').copy(thisNode.subtitle_color)


def adjust_photo_transform(thisNode, photo_mask_format, bbox_format):
    transform = getNode(thisNode, 'photo_transform')

    vertical = bbox_format[0] < bbox_format[1]
    dimension = 0
    if vertical:
        dimension = 1

    scale = float(photo_mask_format[dimension]) / bbox_format[dimension]
    transform.getParam('scale').set(scale, scale)

    transform.getParam('center').set(bbox_format[0] / 2, bbox_format[1] / 2)


def adjust_output_transform(thisNode):
    merge = getNode(thisNode, 'merge')
    transform = getNode(thisNode, 'transform')

    width, height = get_format(thisNode)

    bbox_width, bbox_height = get_bbox_format(merge)
    bbox = get_bbox(merge)

    scale = float(height) / float(bbox_height)
    transform.getParam('scale').set(scale, scale)

    center_y = bbox.y1
    center_x = bbox.x1

    transform.getParam('center').set(center_x, center_y)

    bbox_width *= scale

    translate_x = (width / 2) - (bbox_width / 2)
    transform.getParam('translate').set(translate_x, -center_y)

    reformat_update(thisNode, getNode(thisNode, 'reformat'))


def adjust_metadata(thisNode, rscale, bbox_format):

    adjust_metadata_text(thisNode, rscale, bbox_format, 'a')
    adjust_metadata_text(thisNode, rscale, bbox_format, 'b')


def adjust_metadata_text(thisNode, rscale, bbox_format, base_name):
    bbox_width, bbox_height = bbox_format

    frame_width = get_frame_width(thisNode, bbox_format, rscale) / 2
    size = thisNode.meta_size.get() * rscale

    prefix_node = getNode(thisNode, base_name + '_prefix')
    suffix_node = getNode(thisNode, base_name + '_suffix')
    symbol_node = getNode(thisNode, 'symbol')

    suffix_translate = getNode(thisNode, base_name + '_suffix_position').getParam('translate')
    symbol_translate = getNode(thisNode, base_name + '_symbol_position').getParam('translate')

    prefix = str(thisNode.getParam('meta_' + base_name + '_prefix').get())
    suffix = str(thisNode.getParam('meta_' + base_name + '_suffix').get())

    random.seed(thisNode.seed.get())
    number = random.randint(10, 99)
    text = prefix + str(number)
    prefix_node.getParam('text').set(text)

    suffix_node.getParam('text').set(suffix)
    suffix_disable = suffix_node.getParam('disableNode')
    if suffix:
        suffix_disable.set(False)
    else:
        suffix_disable.set(True)

    prefix_node.getParam('size').set(size)
    suffix_node.getParam('size').set(size)
    symbol_node.getParam('size').set(size)

    prefix_width, prefix_height = get_bbox_format(prefix_node)

    #

    # color
    prefix_node.getParam('color').copy(thisNode.prefix_color)
    suffix_node.getParam('color').copy(thisNode.suffix_color)
    symbol_node.getParam('color').copy(thisNode.symbol_color)

    # desabilita el simbolo para que actualice el color
    symbol_node_disable = symbol_node.getParam('disableNode')
    symbol_node_disable.set(True)
    symbol_node_disable.set(False)
    #

    symbol_size = size * 2

    symbol_translate.set(prefix_width, 0)
    suffix_translate.set(prefix_width + symbol_size, 0)

    #

    width, height = get_bbox_format(getNode(thisNode, base_name + '_merge'))

    translate = getNode(thisNode, base_name + '_position').getParam('translate')

    height_position = bbox_height - (frame_width / 2) - (height / 2)
    if base_name == 'a':
        width_position = frame_width
    else:
        width_position = bbox_width - frame_width - width

    translate.set(width_position, height_position)
