import NatronEngine
from natron_extent import *
from base import *


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    None
