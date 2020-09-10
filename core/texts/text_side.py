from base import link_to_parent
from text_fit import refresh_text_fit


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    title_node, subtitle_node = refresh_text_fit(thisNode)

    title_color = thisNode.title_color
    subtitle_color = thisNode.subtitle_color

    title_node.getParam('color').copy(title_color)
    subtitle_node.getParam('color').copy(subtitle_color)
