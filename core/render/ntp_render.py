import NatronEngine
from natron_extent import *
from base import *


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    name = thisParam.getScriptName()

    if name == 'send':
        render(thisNode)


def render(thisNode):
    print 'render'
    None
