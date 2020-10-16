from base import link_to_parent, children_refresh, get_rscale, get_format
from nx import getNode


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

    reformat_low = getNode(thisNode, 'reformat_low')
    reformat_low.getParam('boxSize').set(1920 / 7, 1080 / 7)

    thisNode.Reformat3.boxSize.set(width, height)
    thisNode.Reformat4.boxSize.set(width, height)
    thisNode.Reformat5.boxSize.set(width, height)

    # si la imagen es vertical cambia el switch a los reformat correspondientes
    dot_input = thisNode.dot_input

    _width = dot_input.getOutputFormat().width()
    _height = dot_input.getOutputFormat().height()

    switch = thisNode.Switch1.which
    vertical = _width < _height

    aspect = 1920.0 / 1080.0  # aspecto de referencia
    aspect_input = float(_width) / float(_height)

    if vertical:
        switch.set(1)
    else:
        if aspect >= aspect_input:
            switch.set(0)
        else:
            switch.set(2)
