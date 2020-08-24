# funciones en comun que comparten todos los nodos de movimiento.


def center_from_input_bbox(node, center_param):
    bbox = node.getInput(0).getRegionOfDefinition(1, 1)

    input_width = abs(bbox.x1 - bbox.x2)
    input_height = abs(bbox.y1 - bbox.y2)

    center_x = bbox.x1 + (input_width / 2)
    center_y = bbox.y1 + (input_height / 2)

    center_param.set(center_x, center_y)
