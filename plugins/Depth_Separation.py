# -*- coding: utf-8 -*-
# DO NOT EDIT THIS FILE
# Natron PyPlug
# This file was automatically generated by Natron PyPlug exporter version 10.

# Hand-written code should be added in a separate file named Depth_SeparationExt.py
# See http://natron.readthedocs.org/en/master/devel/groups.html#adding-hand-written-code-callbacks-etc
# Note that Viewers are never exported

import NatronEngine
import sys

# Try to import the extensions file where callbacks and hand-written code should be located.
try:
    from Depth_SeparationExt import *
except ImportError:
    pass

def getPluginID():
    return "vv.depth_separation"

def getIconPath():
    return "Depth_Separation.png"

def getLabel():
    return "Depth_Separation"

def getVersion():
    return 1

def getGrouping():
    return "videovina"

def createInstance(app,group):
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    lastNode.setColor(0.7, 0.7, 0.7)

    # Create the user parameters
    lastNode.control = lastNode.createPageParam("control", "Control")
    param = lastNode.createDoubleParam("inside_expand", "Inside Expand")
    param.setMinimum(0, 0)
    param.setMaximum(1, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(1, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(0.465, 0)
    lastNode.inside_expand = param
    del param

    param = lastNode.createDoubleParam("rotate", "Rotate")
    param.setMinimum(-180, 0)
    param.setMaximum(180, 0)
    param.setDisplayMinimum(-180, 0)
    param.setDisplayMaximum(180, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValueAtTime(0, 0, 0)
    param.setValueAtTime(-10, 100, 0)
    lastNode.rotate = param
    del param

    param = lastNode.createDoubleParam("translate_x", "Translate X")
    param.setMinimum(-1000, 0)
    param.setMaximum(1000, 0)
    param.setDisplayMinimum(-1000, 0)
    param.setDisplayMaximum(1000, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValueAtTime(0, 0, 0)
    param.setValueAtTime(413, 100, 0)
    lastNode.translate_x = param
    del param

    param = lastNode.createDoubleParam("translate_y", "Translate Y")
    param.setMinimum(-1000, 0)
    param.setMaximum(1000, 0)
    param.setDisplayMinimum(-1000, 0)
    param.setDisplayMaximum(1000, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValueAtTime(0, 0, 0)
    lastNode.translate_y = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    # Start of node "Output1"
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setLabel("Output")
    lastNode.setPosition(3082, 682)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupOutput1 = lastNode

    del lastNode
    # End of node "Output1"

    # Start of node "Input1"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Input1")
    lastNode.setLabel("Input1")
    lastNode.setPosition(764, -89)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupInput1 = lastNode

    del lastNode
    # End of node "Input1"

    # Start of node "Shuffle2"
    lastNode = app.createNode("net.sf.openfx.ShufflePlugin", 3, group)
    lastNode.setScriptName("Shuffle2")
    lastNode.setLabel("Shuffle2")
    lastNode.setPosition(764, -23)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.6, 0.24, 0.39)
    groupShuffle2 = lastNode

    param = lastNode.getParam("outputA")
    if param is not None:
        param.set("1")
        del param

    del lastNode
    # End of node "Shuffle2"

    # Start of node "Merge1"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge1")
    lastNode.setLabel("Merge1")
    lastNode.setPosition(2674, 256)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge1 = lastNode

    param = lastNode.getParam("operation")
    if param is not None:
        param.set("stencil")
        del param

    del lastNode
    # End of node "Merge1"

    # Start of node "Transform3"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("Transform3")
    lastNode.setLabel("Transform3")
    lastNode.setPosition(764, 63)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupTransform3 = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(94.99000000000001, 0)
        param.setValue(0, 1)
        del param

    param = lastNode.getParam("rotate")
    if param is not None:
        param.setValue(-2.3, 0)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "Transform3"

    # Start of node "Dot1"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot1")
    lastNode.setLabel("Dot1")
    lastNode.setPosition(2725, -12)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot1 = lastNode

    del lastNode
    # End of node "Dot1"

    # Start of node "Merge1_2"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge1_2")
    lastNode.setLabel("Merge1_2")
    lastNode.setPosition(1153, 128)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge1_2 = lastNode

    param = lastNode.getParam("operation")
    if param is not None:
        param.set("stencil")
        del param

    del lastNode
    # End of node "Merge1_2"

    # Start of node "Transform1"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("Transform1")
    lastNode.setLabel("Transform1")
    lastNode.setPosition(1337, 140)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupTransform1 = lastNode

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValue(0.6512499999999999, 0)
        param.setValue(0.6512499999999999, 1)
        del param

    del lastNode
    # End of node "Transform1"

    # Start of node "Transform3_2"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("Transform3_2")
    lastNode.setLabel("Transform3_2")
    lastNode.setPosition(1152, 201)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupTransform3_2 = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(47.495, 0)
        param.setValue(0, 1)
        del param

    param = lastNode.getParam("rotate")
    if param is not None:
        param.setValue(-1.15, 0)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "Transform3_2"

    # Start of node "Merge3"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge3")
    lastNode.setLabel("Merge3")
    lastNode.setPosition(1152, 449)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge3 = lastNode

    del lastNode
    # End of node "Merge3"

    # Start of node "Dot3"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot3")
    lastNode.setLabel("Dot3")
    lastNode.setPosition(807, 471)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot3 = lastNode

    del lastNode
    # End of node "Dot3"

    # Start of node "Dot4"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot4")
    lastNode.setLabel("Dot4")
    lastNode.setPosition(1198, -14)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot4 = lastNode

    del lastNode
    # End of node "Dot4"

    # Start of node "Merge1_2_2"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge1_2_2")
    lastNode.setLabel("Merge1_2_2")
    lastNode.setPosition(1616, 160)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge1_2_2 = lastNode

    param = lastNode.getParam("operation")
    if param is not None:
        param.set("stencil")
        del param

    del lastNode
    # End of node "Merge1_2_2"

    # Start of node "Transform1_2"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("Transform1_2")
    lastNode.setLabel("Transform1_2")
    lastNode.setPosition(1801, 172)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupTransform1_2 = lastNode

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValue(0.7675, 0)
        param.setValue(0.7675, 1)
        del param

    del lastNode
    # End of node "Transform1_2"

    # Start of node "Transform3_2_2"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("Transform3_2_2")
    lastNode.setLabel("Transform3_2_2")
    lastNode.setPosition(1615, 234)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupTransform3_2_2 = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(31.66333333333334, 0)
        param.setValue(0, 1)
        del param

    param = lastNode.getParam("rotate")
    if param is not None:
        param.setValue(-0.7666666666666667, 0)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "Transform3_2_2"

    # Start of node "Merge3_2"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge3_2")
    lastNode.setLabel("Merge3_2")
    lastNode.setPosition(1615, 449)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge3_2 = lastNode

    del lastNode
    # End of node "Merge3_2"

    # Start of node "Dot4_2"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot4_2")
    lastNode.setLabel("Dot4_2")
    lastNode.setPosition(1661, -14)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot4_2 = lastNode

    del lastNode
    # End of node "Dot4_2"

    # Start of node "Merge1_2_2_2"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge1_2_2_2")
    lastNode.setLabel("Merge1_2_2_2")
    lastNode.setPosition(2131, 176)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge1_2_2_2 = lastNode

    param = lastNode.getParam("operation")
    if param is not None:
        param.set("stencil")
        del param

    del lastNode
    # End of node "Merge1_2_2_2"

    # Start of node "Transform1_2_2"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("Transform1_2_2")
    lastNode.setLabel("Transform1_2_2")
    lastNode.setPosition(2315, 176)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupTransform1_2_2 = lastNode

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValue(0.88375, 0)
        param.setValue(0.88375, 1)
        del param

    del lastNode
    # End of node "Transform1_2_2"

    # Start of node "Transform3_2_2_2"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("Transform3_2_2_2")
    lastNode.setLabel("Transform3_2_2_2")
    lastNode.setPosition(2131, 251)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupTransform3_2_2_2 = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(23.7475, 0)
        param.setValue(0, 1)
        del param

    param = lastNode.getParam("rotate")
    if param is not None:
        param.setValue(-0.5750000000000001, 0)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "Transform3_2_2_2"

    # Start of node "Merge3_2_2"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge3_2_2")
    lastNode.setLabel("Merge3_2_2")
    lastNode.setPosition(2130, 444)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge3_2_2 = lastNode

    del lastNode
    # End of node "Merge3_2_2"

    # Start of node "Dot4_2_2"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot4_2_2")
    lastNode.setLabel("Dot4_2_2")
    lastNode.setPosition(2176, -14)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot4_2_2 = lastNode

    del lastNode
    # End of node "Dot4_2_2"

    # Start of node "Merge2"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge2")
    lastNode.setLabel("Merge2")
    lastNode.setPosition(2674, 444)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge2 = lastNode

    del lastNode
    # End of node "Merge2"

    # Start of node "Shape"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Shape")
    lastNode.setLabel("Shape")
    lastNode.setPosition(1340, -235)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupShape = lastNode

    del lastNode
    # End of node "Shape"

    # Start of node "Dot2"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot2")
    lastNode.setLabel("Dot2")
    lastNode.setPosition(1382, -112)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot2 = lastNode

    del lastNode
    # End of node "Dot2"

    # Start of node "Dot5"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot5")
    lastNode.setLabel("Dot5")
    lastNode.setPosition(1848, -112)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot5 = lastNode

    del lastNode
    # End of node "Dot5"

    # Start of node "Dot6"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot6")
    lastNode.setLabel("Dot6")
    lastNode.setPosition(2360, -112)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot6 = lastNode

    del lastNode
    # End of node "Dot6"

    # Start of node "Dot7"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot7")
    lastNode.setLabel("Dot7")
    lastNode.setPosition(2861, -112)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot7 = lastNode

    del lastNode
    # End of node "Dot7"

    # Start of node "Dot8"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot8")
    lastNode.setLabel("Dot8")
    lastNode.setPosition(2861, 281)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot8 = lastNode

    del lastNode
    # End of node "Dot8"

    # Start of node "Merge4"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge4")
    lastNode.setLabel("Merge4")
    lastNode.setPosition(3082, 444)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge4 = lastNode

    del lastNode
    # End of node "Merge4"

    # Start of node "Dot9"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot9")
    lastNode.setLabel("Dot9")
    lastNode.setPosition(3127, -12)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot9 = lastNode

    del lastNode
    # End of node "Dot9"

    # Start of node "Crop2"
    lastNode = app.createNode("net.sf.openfx.CropPlugin", 1, group)
    lastNode.setScriptName("Crop2")
    lastNode.setLabel("Crop2")
    lastNode.setPosition(3082, 530)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupCrop2 = lastNode

    param = lastNode.getParam("NatronParamFormatChoice")
    if param is not None:
        param.set("PC_Video")
        del param

    del lastNode
    # End of node "Crop2"

    # Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, groupCrop2)
    groupShuffle2.connectInput(0, groupInput1)
    groupMerge1.connectInput(0, groupDot1)
    groupMerge1.connectInput(1, groupDot8)
    groupTransform3.connectInput(0, groupShuffle2)
    groupDot1.connectInput(0, groupDot4_2_2)
    groupMerge1_2.connectInput(0, groupDot4)
    groupMerge1_2.connectInput(1, groupTransform1)
    groupTransform1.connectInput(0, groupDot2)
    groupTransform3_2.connectInput(0, groupMerge1_2)
    groupMerge3.connectInput(0, groupDot3)
    groupMerge3.connectInput(1, groupTransform3_2)
    groupDot3.connectInput(0, groupTransform3)
    groupDot4.connectInput(0, groupShuffle2)
    groupMerge1_2_2.connectInput(0, groupDot4_2)
    groupMerge1_2_2.connectInput(1, groupTransform1_2)
    groupTransform1_2.connectInput(0, groupDot5)
    groupTransform3_2_2.connectInput(0, groupMerge1_2_2)
    groupMerge3_2.connectInput(0, groupMerge3)
    groupMerge3_2.connectInput(1, groupTransform3_2_2)
    groupDot4_2.connectInput(0, groupDot4)
    groupMerge1_2_2_2.connectInput(0, groupDot4_2_2)
    groupMerge1_2_2_2.connectInput(1, groupTransform1_2_2)
    groupTransform1_2_2.connectInput(0, groupDot6)
    groupTransform3_2_2_2.connectInput(0, groupMerge1_2_2_2)
    groupMerge3_2_2.connectInput(0, groupMerge3_2)
    groupMerge3_2_2.connectInput(1, groupTransform3_2_2_2)
    groupDot4_2_2.connectInput(0, groupDot4_2)
    groupMerge2.connectInput(0, groupMerge3_2_2)
    groupMerge2.connectInput(1, groupMerge1)
    groupDot2.connectInput(0, groupShape)
    groupDot5.connectInput(0, groupDot2)
    groupDot6.connectInput(0, groupDot5)
    groupDot7.connectInput(0, groupDot6)
    groupDot8.connectInput(0, groupDot7)
    groupMerge4.connectInput(0, groupDot9)
    groupMerge4.connectInput(1, groupMerge2)
    groupDot9.connectInput(0, groupDot1)
    groupCrop2.connectInput(0, groupMerge4)

    param = groupTransform3.getParam("translate")
    param.setExpression("x = thisGroup.translate_x.curve(frame)\ny = thisGroup.translate_y.curve(frame)\n\nif dimension == 0:\n\tret = x\nelse:\n\tret = y", True, 0)
    param.setExpression("x = thisGroup.translate_x.curve(frame)\ny = thisGroup.translate_y.curve(frame)\n\nif dimension == 0:\n\tret = x\nelse:\n\tret = y", True, 1)
    del param
    param = groupTransform3.getParam("rotate")
    param.setExpression("thisGroup.rotate.curve(frame)", False, 0)
    del param
    param = groupTransform1.getParam("scale")
    param.setExpression("expand = ( 1 - thisGroup.inside_expand.get() )\nleftover = 1 - expand\n\ncurrent_slide = 1\nslide_amount = 4\nappend = leftover / slide_amount\n\nret = expand + append * current_slide", True, 0)
    param.setExpression("expand = ( 1 - thisGroup.inside_expand.get() )\nleftover = 1 - expand\n\ncurrent_slide = 1\nslide_amount = 4\nappend = leftover / slide_amount\n\nret = expand + append * current_slide", True, 1)
    del param
    param = groupTransform3_2.getParam("translate")
    param.setExpression("x = thisGroup.translate_x.curve(frame)\ny = thisGroup.translate_y.curve(frame)\n\ncurrent = 2\n\nif dimension == 0:\n\tret = x / current\nelse:\n\tret = y / current", True, 0)
    param.setExpression("x = thisGroup.translate_x.curve(frame)\ny = thisGroup.translate_y.curve(frame)\n\ncurrent = 2\n\nif dimension == 0:\n\tret = x / current\nelse:\n\tret = y / current", True, 1)
    del param
    param = groupTransform3_2.getParam("rotate")
    param.setExpression("thisGroup.rotate.curve(frame) / 2", False, 0)
    del param
    param = groupTransform1_2.getParam("scale")
    param.setExpression("expand = ( 1 - thisGroup.inside_expand.get() )\nleftover = 1 - expand\n\ncurrent_slide = 2\nslide_amount = 4\nappend = leftover / slide_amount\n\nret = expand + append * current_slide", True, 0)
    param.setExpression("expand = ( 1 - thisGroup.inside_expand.get() )\nleftover = 1 - expand\n\ncurrent_slide = 2\nslide_amount = 4\nappend = leftover / slide_amount\n\nret = expand + append * current_slide", True, 1)
    del param
    param = groupTransform3_2_2.getParam("translate")
    param.setExpression("x = thisGroup.translate_x.curve(frame)\ny = thisGroup.translate_y.curve(frame)\n\ncurrent = 3\n\nif dimension == 0:\n\tret = x / current\nelse:\n\tret = y / current", True, 0)
    param.setExpression("x = thisGroup.translate_x.curve(frame)\ny = thisGroup.translate_y.curve(frame)\n\ncurrent = 3\n\nif dimension == 0:\n\tret = x / current\nelse:\n\tret = y / current", True, 1)
    del param
    param = groupTransform3_2_2.getParam("rotate")
    param.setExpression("thisGroup.rotate.curve(frame) / 3", False, 0)
    del param
    param = groupTransform1_2_2.getParam("scale")
    param.setExpression("expand = ( 1 - thisGroup.inside_expand.get() )\nleftover = 1 - expand\n\ncurrent_slide = 3\nslide_amount = 4\nappend = leftover / slide_amount\n\nret = expand + append * current_slide", True, 0)
    param.setExpression("expand = ( 1 - thisGroup.inside_expand.get() )\nleftover = 1 - expand\n\ncurrent_slide = 3\nslide_amount = 4\nappend = leftover / slide_amount\n\nret = expand + append * current_slide", True, 1)
    del param
    param = groupTransform3_2_2_2.getParam("translate")
    param.setExpression("x = thisGroup.translate_x.curve(frame)\ny = thisGroup.translate_y.curve(frame)\n\ncurrent = 4\n\nif dimension == 0:\n\tret = x / current\nelse:\n\tret = y / current", True, 0)
    param.setExpression("x = thisGroup.translate_x.curve(frame)\ny = thisGroup.translate_y.curve(frame)\n\ncurrent = 4\n\nif dimension == 0:\n\tret = x / current\nelse:\n\tret = y / current", True, 1)
    del param
    param = groupTransform3_2_2_2.getParam("rotate")
    param.setExpression("thisGroup.rotate.curve(frame) / 4", False, 0)
    del param

    try:
        extModule = sys.modules["Depth_SeparationExt"]
    except KeyError:
        extModule = None
    if extModule is not None and hasattr(extModule ,"createInstanceExt") and hasattr(extModule.createInstanceExt,"__call__"):
        extModule.createInstanceExt(app,group)