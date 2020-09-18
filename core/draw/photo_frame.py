from base import link_to_parent, get_rscale, get_duration, get_format, get_start_frame, reformat_update
from nx import getNode
from text_fit import separate_text, get_bbox_format, get_bbox


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)
    start_frame = get_start_frame(thisNode)

    bbox_format = get_bbox_format(thisNode.getInput(0))

    corner_radius = thisNode.corner_radius.get() * rscale
    bottom_margin = bbox_format[1] * thisNode.bottom_margin.get() / 100

    rectangle = getNode(thisNode, 'rectangle')
    rectangle_height = bbox_format[1] + bottom_margin
    rectangle.getParam('cornerRadius').set(corner_radius, corner_radius)

    rectangle.getParam('size').set(bbox_format[0], rectangle_height)
    rectangle.getParam('bottomLeft').set(0, -bottom_margin)

    #
    #

    frame_width = thisNode.frame_width.get() * rscale

    vertical = bbox_format[0] < bbox_format[1]
    if vertical:
        aspect = float(bbox_format[1]) / bbox_format[0]
        frame_width *= aspect

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
