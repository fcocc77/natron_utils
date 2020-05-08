# -*- coding: utf-8 -*-
# DO NOT EDIT THIS FILE
# Natron PyPlug
# This file was automatically generated by Natron PyPlug exporter version 10.

# Hand-written code should be added in a separate file named PostFXExt.py
# See http://natron.readthedocs.org/en/master/devel/groups.html#adding-hand-written-code-callbacks-etc
# Note that Viewers are never exported

import NatronEngine
import sys

# Try to import the extensions file where callbacks and hand-written code should be located.
try:
    from PostFXExt import *
except ImportError:
    pass

def getPluginID():
    return "vv.postfx"

def getLabel():
    return "PostFX"

def getVersion():
    return 1

def getIconPath():
    return "PostFX.png"

def getGrouping():
    return "videovina"

def createInstance(app,group):
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    lastNode.setColor(0.7, 0.7, 0.7)

    # Create the user parameters
    lastNode.control = lastNode.createPageParam("control", "Control")
    param = lastNode.createDoubleParam("chromatic_aberration", "Chromatic Aberration")
    param.setMinimum(0, 0)
    param.setMaximum(10, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(10, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(5, 0)
    lastNode.chromatic_aberration = param
    del param

    param = lastNode.createDoubleParam("vignete", "Vignete")
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
    param.setValue(0.5, 0)
    lastNode.vignete = param
    del param

    param = lastNode.createDoubleParam("vignete_softness", "Vignete Softness")
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
    param.setValue(1, 0)
    lastNode.vignete_softness = param
    del param

    param = lastNode.createDoubleParam("edge_blur", "Vignete Blur")
    param.setMinimum(0, 0)
    param.setMaximum(100, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(20, 0)
    lastNode.edge_blur = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    # Start of node "Output1"
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setLabel("Output")
    lastNode.setPosition(1239, 1074)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupOutput1 = lastNode

    del lastNode
    # End of node "Output1"

    # Start of node "Input1"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Input1")
    lastNode.setLabel("Input1")
    lastNode.setPosition(1241, -104)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupInput1 = lastNode

    del lastNode
    # End of node "Input1"

    # Start of node "Radial1"
    lastNode = app.createNode("net.sf.openfx.Radial", 2, group)
    lastNode.setScriptName("Radial1")
    lastNode.setLabel("Radial1")
    lastNode.setPosition(989, 22)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupRadial1 = lastNode

    param = lastNode.getParam("NatronParamFormatChoice")
    if param is not None:
        param.set("PC_Video")
        del param

    param = lastNode.getParam("softness")
    if param is not None:
        param.setValue(1, 0)
        del param

    param = lastNode.getParam("color0")
    if param is not None:
        param.setValue(1, 3)
        del param

    param = lastNode.getParam("color1")
    if param is not None:
        param.setValue(0, 0)
        param.setValue(0, 1)
        param.setValue(0, 2)
        param.setValue(0, 3)
        del param

    del lastNode
    # End of node "Radial1"

    # Start of node "Merge2"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge2")
    lastNode.setLabel("Merge2")
    lastNode.setPosition(1241, 80)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge2 = lastNode

    param = lastNode.getParam("mix")
    if param is not None:
        param.setValue(0.5, 0)
        del param

    del lastNode
    # End of node "Merge2"

    # Start of node "Blur1"
    lastNode = app.createNode("net.sf.cimg.CImgBlur", 4, group)
    lastNode.setScriptName("Blur1")
    lastNode.setLabel("Blur1")
    lastNode.setPosition(1241, 260)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.8, 0.5, 0.3)
    groupBlur1 = lastNode

    param = lastNode.getParam("size")
    if param is not None:
        param.setValue(20, 0)
        param.setValue(20, 1)
        del param

    param = lastNode.getParam("boundary")
    if param is not None:
        param.set("nearest")
        del param

    param = lastNode.getParam("expandRoD")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("cropToFormat")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("enableMask_Mask")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "Blur1"

    # Start of node "FrameHold1"
    lastNode = app.createNode("net.sf.openfx.FrameHold", 1, group)
    lastNode.setScriptName("FrameHold1")
    lastNode.setLabel("FrameHold1")
    lastNode.setPosition(989, 85)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.7, 0.65, 0.35)
    groupFrameHold1 = lastNode

    del lastNode
    # End of node "FrameHold1"

    # Start of node "Crop1"
    lastNode = app.createNode("net.sf.openfx.CropPlugin", 1, group)
    lastNode.setScriptName("Crop1")
    lastNode.setLabel("Crop1")
    lastNode.setPosition(1241, 184)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupCrop1 = lastNode

    param = lastNode.getParam("NatronParamFormatChoice")
    if param is not None:
        param.set("PC_Video")
        del param

    del lastNode
    # End of node "Crop1"

    # Start of node "red"
    lastNode = app.createNode("net.sf.openfx.ShufflePlugin", 3, group)
    lastNode.setScriptName("red")
    lastNode.setLabel("red")
    lastNode.setPosition(462, 550)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.6, 0.24, 0.39)
    groupred = lastNode

    param = lastNode.getParam("outputComponents")
    if param is not None:
        param.set("rgb")
        del param

    param = lastNode.getParam("outputG")
    if param is not None:
        param.set("0")
        del param

    param = lastNode.getParam("outputB")
    if param is not None:
        param.set("0")
        del param

    param = lastNode.getParam("outputA")
    if param is not None:
        param.set("0")
        del param

    del lastNode
    # End of node "red"

    # Start of node "green"
    lastNode = app.createNode("net.sf.openfx.ShufflePlugin", 3, group)
    lastNode.setScriptName("green")
    lastNode.setLabel("green")
    lastNode.setPosition(653, 552)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.6, 0.24, 0.39)
    groupgreen = lastNode

    param = lastNode.getParam("outputComponents")
    if param is not None:
        param.set("rgb")
        del param

    param = lastNode.getParam("outputR")
    if param is not None:
        param.set("0")
        del param

    param = lastNode.getParam("outputB")
    if param is not None:
        param.set("0")
        del param

    param = lastNode.getParam("outputA")
    if param is not None:
        param.set("0")
        del param

    del lastNode
    # End of node "green"

    # Start of node "blue"
    lastNode = app.createNode("net.sf.openfx.ShufflePlugin", 3, group)
    lastNode.setScriptName("blue")
    lastNode.setLabel("blue")
    lastNode.setPosition(872, 541)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.6, 0.24, 0.39)
    groupblue = lastNode

    param = lastNode.getParam("outputComponents")
    if param is not None:
        param.set("rgb")
        del param

    param = lastNode.getParam("outputR")
    if param is not None:
        param.set("0")
        del param

    param = lastNode.getParam("outputG")
    if param is not None:
        param.set("0")
        del param

    param = lastNode.getParam("outputA")
    if param is not None:
        param.set("0")
        del param

    del lastNode
    # End of node "blue"

    # Start of node "Merge1"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge1")
    lastNode.setLabel("Merge1")
    lastNode.setPosition(653, 742)
    lastNode.setSize(104, 57)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge1 = lastNode

    param = lastNode.getParam("AChannelsA")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("BChannelsA")
    if param is not None:
        param.setValue(False)
        del param

    del lastNode
    # End of node "Merge1"

    # Start of node "Dot1"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot1")
    lastNode.setLabel("Dot1")
    lastNode.setPosition(698, 448)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot1 = lastNode

    del lastNode
    # End of node "Dot1"

    # Start of node "Position1"
    lastNode = app.createNode("net.sf.openfx.Position", 1, group)
    lastNode.setScriptName("Position1")
    lastNode.setLabel("Position1")
    lastNode.setPosition(653, 616)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupPosition1 = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(-5, 0)
        del param

    del lastNode
    # End of node "Position1"

    # Start of node "Position2"
    lastNode = app.createNode("net.sf.openfx.Position", 1, group)
    lastNode.setScriptName("Position2")
    lastNode.setLabel("Position2")
    lastNode.setPosition(872, 622)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupPosition2 = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(5, 0)
        del param

    del lastNode
    # End of node "Position2"

    # Start of node "Dot2"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot2")
    lastNode.setLabel("Dot2")
    lastNode.setPosition(507, 448)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot2 = lastNode

    del lastNode
    # End of node "Dot2"

    # Start of node "Dot3"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot3")
    lastNode.setLabel("Dot3")
    lastNode.setPosition(917, 448)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot3 = lastNode

    del lastNode
    # End of node "Dot3"

    # Start of node "Dot4"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot4")
    lastNode.setLabel("Dot4")
    lastNode.setPosition(507, 763)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot4 = lastNode

    del lastNode
    # End of node "Dot4"

    # Start of node "Dot5"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot5")
    lastNode.setLabel("Dot5")
    lastNode.setPosition(917, 765)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot5 = lastNode

    del lastNode
    # End of node "Dot5"

    # Start of node "Switch1"
    lastNode = app.createNode("net.sf.openfx.switchPlugin", 1, group)
    lastNode.setScriptName("Switch1")
    lastNode.setLabel("Switch1")
    lastNode.setPosition(1239, 863)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupSwitch1 = lastNode

    param = lastNode.getParam("which")
    if param is not None:
        param.setValue(1, 0)
        del param

    del lastNode
    # End of node "Switch1"

    # Start of node "Dot7"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot7")
    lastNode.setLabel("Dot7")
    lastNode.setPosition(698, 356)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot7 = lastNode

    del lastNode
    # End of node "Dot7"

    # Start of node "Dot8"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot8")
    lastNode.setLabel("Dot8")
    lastNode.setPosition(1284, 356)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot8 = lastNode

    del lastNode
    # End of node "Dot8"

    # Start of node "Dot9"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot9")
    lastNode.setLabel("Dot9")
    lastNode.setPosition(698, 872)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot9 = lastNode

    del lastNode
    # End of node "Dot9"

    # Start of node "Shuffle1"
    lastNode = app.createNode("net.sf.openfx.ShufflePlugin", 3, group)
    lastNode.setScriptName("Shuffle1")
    lastNode.setLabel("Shuffle1")
    lastNode.setPosition(1031, 863)
    lastNode.setSize(104, 33)
    lastNode.setColor(0.6, 0.24, 0.39)
    groupShuffle1 = lastNode

    param = lastNode.getParam("outputA")
    if param is not None:
        param.set("A.uk.co.thefoundry.OfxImagePlaneColour.A")
        del param

    del lastNode
    # End of node "Shuffle1"

    # Start of node "Dot6"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot6")
    lastNode.setLabel("Dot6")
    lastNode.setPosition(1076, 356)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot6 = lastNode

    del lastNode
    # End of node "Dot6"

    # Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, groupSwitch1)
    groupMerge2.connectInput(0, groupInput1)
    groupMerge2.connectInput(1, groupFrameHold1)
    groupBlur1.connectInput(0, groupCrop1)
    groupBlur1.connectInput(1, groupFrameHold1)
    groupFrameHold1.connectInput(0, groupRadial1)
    groupCrop1.connectInput(0, groupMerge2)
    groupred.connectInput(0, groupDot2)
    groupgreen.connectInput(0, groupDot1)
    groupblue.connectInput(0, groupDot3)
    groupMerge1.connectInput(0, groupDot4)
    groupMerge1.connectInput(1, groupPosition1)
    groupMerge1.connectInput(3, groupDot5)
    groupDot1.connectInput(0, groupDot7)
    groupPosition1.connectInput(0, groupgreen)
    groupPosition2.connectInput(0, groupblue)
    groupDot2.connectInput(0, groupDot1)
    groupDot3.connectInput(0, groupDot1)
    groupDot4.connectInput(0, groupred)
    groupDot5.connectInput(0, groupPosition2)
    groupSwitch1.connectInput(0, groupDot8)
    groupSwitch1.connectInput(1, groupShuffle1)
    groupDot7.connectInput(0, groupDot6)
    groupDot8.connectInput(0, groupBlur1)
    groupDot9.connectInput(0, groupMerge1)
    groupShuffle1.connectInput(0, groupDot9)
    groupShuffle1.connectInput(1, groupDot6)
    groupDot6.connectInput(0, groupDot8)

    param = groupRadial1.getParam("softness")
    param.setExpression("thisGroup.vignete_softness.getValue()", False, 0)
    del param
    param = groupMerge2.getParam("mix")
    param.setExpression("thisGroup.vignete.get()", False, 0)
    del param
    param = groupBlur1.getParam("size")
    param.setExpression("thisGroup.edge_blur.get()", False, 0)
    param.setExpression("thisGroup.edge_blur.get()", False, 1)
    del param
    param = groupPosition1.getParam("translate")
    param.setExpression("-thisGroup.chromatic_aberration.getValue()", False, 0)
    del param
    param = groupPosition2.getParam("translate")
    param.setExpression("thisGroup.chromatic_aberration.get()", False, 0)
    del param
    param = groupSwitch1.getParam("which")
    param.setExpression("1 if thisGroup.chromatic_aberration.getValue() else 0", False, 0)
    del param

    try:
        extModule = sys.modules["PostFXExt"]
    except KeyError:
        extModule = None
    if extModule is not None and hasattr(extModule ,"createInstanceExt") and hasattr(extModule.createInstanceExt,"__call__"):
        extModule.createInstanceExt(app,group)