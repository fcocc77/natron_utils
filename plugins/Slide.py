# -*- coding: utf-8 -*-
# DO NOT EDIT THIS FILE
# Natron PyPlug
# This file was automatically generated by Natron PyPlug exporter version 10.

# Hand-written code should be added in a separate file named SlideExt.py
# See http://natron.readthedocs.org/en/master/devel/groups.html#adding-hand-written-code-callbacks-etc
# Note that Viewers are never exported

import NatronEngine
import sys

# Try to import the extensions file where callbacks and hand-written code should be located.
try:
    from SlideExt import *
except ImportError:
    pass

def getPluginID():
    return "vv.slide"

def getLabel():
    return "Slide"

def getVersion():
    return 1

def getGrouping():
    return "videovina"

def createInstance(app,group):
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    lastNode.setColor(0.7, 0.7, 0.7)
    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("videovina.main")
        del param


    # Create the user parameters
    lastNode.control = lastNode.createPageParam("control", "Control")
    param = lastNode.createIntParam("input_amount", "Extra Pictures Input")
    param.setMinimum(0, 0)
    param.setMaximum(10, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(10, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.input_amount = param
    del param

    param = lastNode.createButtonParam("generate_inputs", "Generate")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setEvaluateOnChange(False)
    lastNode.generate_inputs = param
    del param

    param = lastNode.createInt2DParam("FrameRangeframeRange", "Frame Range")
    param.setDefaultValue(1, 0)
    param.restoreDefaultValue(0)
    param.setDefaultValue(1, 1)
    param.restoreDefaultValue(1)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    param.setValue(100, 1)
    lastNode.FrameRangeframeRange = param
    del param

    param = lastNode.createDoubleParam("rscale", "Resolution Scale")
    param.setMinimum(0.1, 0)
    param.setMaximum(4, 0)
    param.setDisplayMinimum(0.1, 0)
    param.setDisplayMaximum(4, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(1, 0)
    lastNode.rscale = param
    del param

    param = lastNode.createColorParam("color", "Color", False)
    param.setMinimum(-2147483648, 0)
    param.setMaximum(2147483647, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(1, 0)
    param.setMinimum(-2147483648, 1)
    param.setMaximum(2147483647, 1)
    param.setDisplayMinimum(0, 1)
    param.setDisplayMaximum(1, 1)
    param.setMinimum(-2147483648, 2)
    param.setMaximum(2147483647, 2)
    param.setDisplayMinimum(0, 2)
    param.setDisplayMaximum(1, 2)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(1, 0)
    param.setValue(1, 1)
    param.setValue(1, 2)
    lastNode.color = param
    del param

    param = lastNode.createStringParam("text_label", "")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)
    param.setDefaultValue("TEXT:")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setEvaluateOnChange(False)
    param.setAnimationEnabled(False)
    lastNode.text_label = param
    del param

    param = lastNode.createStringParam("title", "Title")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeDefault)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.title = param
    del param

    param = lastNode.createStringParam("subtitle", "Subtitle")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeDefault)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.subtitle = param
    del param

    param = lastNode.createStringParam("font", "Font")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeDefault)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.font = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    # Start of node "Output1"
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setLabel("Output")
    lastNode.setPosition(-207, 1075)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupOutput1 = lastNode

    del lastNode
    # End of node "Output1"

    # Start of node "Image"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Image")
    lastNode.setLabel("Image")
    lastNode.setPosition(-207, 3)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupImage = lastNode

    del lastNode
    # End of node "Image"

    # Start of node "FrameRange"
    lastNode = app.createNode("net.sf.openfx.FrameRange", 1, group)
    lastNode.setScriptName("FrameRange")
    lastNode.setLabel("FrameRange")
    lastNode.setPosition(-207, 990)
    lastNode.setSize(104, 45)
    lastNode.setColor(0.7, 0.65, 0.35)
    groupFrameRange = lastNode

    param = lastNode.getParam("frameRange")
    if param is not None:
        param.setValue(100, 1)
        del param

    param = lastNode.getParam("before")
    if param is not None:
        param.set("hold")
        del param

    param = lastNode.getParam("after")
    if param is not None:
        param.set("hold")
        del param

    param = lastNode.getParam("userTextArea")
    if param is not None:
        param.setValue("<Natron>(1 - 100)</Natron>")
        del param

    del lastNode
    # End of node "FrameRange"

    # Start of node "TimeOffset"
    lastNode = app.createNode("net.sf.openfx.timeOffset", 1, group)
    lastNode.setScriptName("TimeOffset")
    lastNode.setLabel("TimeOffset")
    lastNode.setPosition(-207, 918)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.65, 0.35)
    groupTimeOffset = lastNode

    param = lastNode.getParam("timeOffset")
    if param is not None:
        param.setValue(1, 0)
        del param

    del lastNode
    # End of node "TimeOffset"

    # Start of node "Merge1"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge1")
    lastNode.setLabel("Merge1")
    lastNode.setPosition(-207, 701)
    lastNode.setSize(104, 55)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge1 = lastNode

    param = lastNode.getParam("userTextArea")
    if param is not None:
        param.setValue("<Natron>(over)</Natron>")
        del param

    del lastNode
    # End of node "Merge1"

    # Start of node "FX"
    lastNode = app.createNode("fr.inria.built-in.Group", 1, group)
    lastNode.setScriptName("FX")
    lastNode.setLabel("FX")
    lastNode.setPosition(-564, 466)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupFX = lastNode

    del lastNode
    # End of node "FX"

    groupgroup = groupFX
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = groupgroup
    lastNode.setColor(0.7, 0.7, 0.7)
    del lastNode

    # Start of node "Output1"
    lastNode = app.createNode("fr.inria.built-in.Output", 1, groupgroup)
    lastNode.setLabel("Output")
    lastNode.setPosition(1180, 609)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupgroupOutput1 = lastNode

    del lastNode
    # End of node "Output1"

    # Start of node "Input1"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, groupgroup)
    lastNode.setScriptName("Input1")
    lastNode.setLabel("Input1")
    lastNode.setPosition(1180, 509)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupgroupInput1 = lastNode

    del lastNode
    # End of node "Input1"

    # Now that all nodes are created we can connect them together, restore expressions
    groupgroupOutput1.connectInput(0, groupgroupInput1)


    # Start of node "Dot1"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot1")
    lastNode.setLabel("Dot1")
    lastNode.setPosition(-519, 721)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot1 = lastNode

    del lastNode
    # End of node "Dot1"

    # Start of node "Backdrop1"
    lastNode = app.createNode("fr.inria.built-in.BackDrop", 1, group)
    lastNode.setScriptName("Backdrop1")
    lastNode.setLabel("Backdrop1")
    lastNode.setPosition(-725, 380)
    lastNode.setSize(317, 268)
    lastNode.setColor(0.45, 0.45, 0.45)
    groupBackdrop1 = lastNode

    param = lastNode.getParam("Label")
    if param is not None:
        param.setValue("<font size=\"6\" color=\"#000000\" face=\"Droid Sans\">Efectos, formas y otros que no necesitan la imagen de entrada</font>")
        del param

    del lastNode
    # End of node "Backdrop1"

    # Start of node "Merge2"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge2")
    lastNode.setLabel("Merge2")
    lastNode.setPosition(-207, 814)
    lastNode.setSize(104, 55)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge2 = lastNode

    param = lastNode.getParam("mix")
    if param is not None:
        param.setValue(0, 0)
        del param

    param = lastNode.getParam("userTextArea")
    if param is not None:
        param.setValue("<Natron>(over)</Natron>")
        del param

    del lastNode
    # End of node "Merge2"

    # Start of node "Backdrop2"
    lastNode = app.createNode("fr.inria.built-in.BackDrop", 1, group)
    lastNode.setScriptName("Backdrop2")
    lastNode.setLabel("Backdrop2")
    lastNode.setPosition(56, 364)
    lastNode.setSize(329, 302)
    lastNode.setColor(0.45, 0.45, 0.45)
    groupBackdrop2 = lastNode

    param = lastNode.getParam("Label")
    if param is not None:
        param.setValue("<font size=\"6\" color=\"#000000\" face=\"Droid Sans\">Textos</font>")
        del param

    del lastNode
    # End of node "Backdrop2"

    # Start of node "Dot3"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot3")
    lastNode.setLabel("Dot3")
    lastNode.setPosition(216, 566)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot3 = lastNode

    del lastNode
    # End of node "Dot3"

    # Start of node "Dot2"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot2")
    lastNode.setLabel("Dot2")
    lastNode.setPosition(216, 834)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot2 = lastNode

    del lastNode
    # End of node "Dot2"

    # Start of node "Dot4"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot4")
    lastNode.setLabel("Dot4")
    lastNode.setPosition(-519, 219)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot4 = lastNode

    del lastNode
    # End of node "Dot4"

    # Start of node "Dot5"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot5")
    lastNode.setLabel("Dot5")
    lastNode.setPosition(-162, 219)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot5 = lastNode

    del lastNode
    # End of node "Dot5"

    # Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, groupFrameRange)
    groupFrameRange.connectInput(0, groupTimeOffset)
    groupTimeOffset.connectInput(0, groupMerge2)
    groupMerge1.connectInput(0, groupDot5)
    groupMerge1.connectInput(1, groupDot1)
    groupFX.connectInput(0, groupDot4)
    groupDot1.connectInput(0, groupFX)
    groupMerge2.connectInput(0, groupMerge1)
    groupMerge2.connectInput(1, groupDot2)
    groupDot2.connectInput(0, groupDot3)
    groupDot4.connectInput(0, groupDot5)
    groupDot5.connectInput(0, groupImage)

    param = groupFrameRange.getParam("frameRange")
    group.getParam("FrameRangeframeRange").setAsAlias(param)
    del param
    param = groupTimeOffset.getParam("timeOffset")
    param.setExpression("thisGroup.FrameRange.frameRange.getValue(0)", False, 0)
    del param
    param = groupMerge2.getParam("mix")
    param.setExpression("# si tiene titulo o subtitle, mezcla los textos\nif thisGroup.title.get() or thisGroup.subtitle.get():\n\tret = 1\nelse:\n\tret = 0", True, 0)
    del param

    try:
        extModule = sys.modules["SlideExt"]
    except KeyError:
        extModule = None
    if extModule is not None and hasattr(extModule ,"createInstanceExt") and hasattr(extModule.createInstanceExt,"__call__"):
        extModule.createInstanceExt(app,group)
