from base import link_to_parent, children_refresh, get_rscale, get_format
from nx import getNode, createNode, get_output, node_delete


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    width, height = get_format(thisNode)

    image_input = getNode(thisNode, 'Image')
    mask_input = getNode(thisNode, 'Mask')
    output_node = get_output(thisNode)

    node_pos_x, node_pos_y = image_input.getPosition()
    samples = thisNode.samples.get()

    sample = 1.0 / (samples - 1)

    # crea una lista de tolerancias para el keyer
    tolerances = []
    tolerance = sample
    for i in range(samples):
        tolerance -= sample
        tolerance = round(tolerance, 3)
        # cuando es '-1.0' en keyer desaparece, por eso se pone '0.90'
        if tolerance < -0.90:
            tolerance = -0.90

        tolerances.append(tolerance)
    tolerances = list(reversed(tolerances))
    #
    #

    # crea una lista de desenfoques
    blurs = []
    blur_added = (thisNode.blur_size.get() * rscale) / samples
    blur_size = 0
    for i in range(samples):
        blur_size += blur_added
        blurs.append(blur_size)
    #
    #

    # Elimina los nodos sobrantes
    delete_nodes = []
    for i in range(samples, 10):
        delete_nodes.append(getNode(thisNode, 'blur_' + str(i)))
        delete_nodes.append(getNode(thisNode, 'keyer_' + str(i)))
    node_delete(delete_nodes)
    #
    #

    softness = 0 - (thisNode.softness.get() / 10)

    last_blur_connect = image_input
    for index in range(samples):
        node_pos_y += 100

        blur = createNode('blur', 'blur_' + str(index), thisNode, force=False)
        blur.connectInput(0, last_blur_connect)
        blur.setPosition(node_pos_x, node_pos_y)
        blur.getParam('maskInvert').set(True)
        blur.getParam('boundary').set(True)
        blur_size = blurs[index]
        blur.getParam('size').set(blur_size, blur_size)

        keyer = createNode('keyer', 'keyer_' + str(index), thisNode, force=False)
        keyer.connectInput(0, mask_input)
        keyer.setPosition(node_pos_x + 300, node_pos_y)

        keyer.getParam('softnessLower').set(softness)
        keyer.getParam('toleranceLower').set(tolerances[index])

        blur.connectInput(1, keyer)

        last_blur_connect = blur

        blur_size *= 2

    output_node.disconnectInput(0)
    output_node.connectInput(0, blur)
