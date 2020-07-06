import NatronEngine

def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    transform = getNode(thisNode, 'transform')
    translate = transform.getParam('translate')