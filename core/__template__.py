import NatronEngine
from natron_extent import *


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    name = thisParam.getScriptName()
    children_refresh(thisParam, thisNode)

    if name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    None
