# -*- coding: utf-8 -*-
# DO NOT EDIT THIS FILE
# Natron PyPlug
# This file was automatically generated by Natron PyPlug exporter version 10.

# Hand-written code should be added in a separate file named SubtleMoveExt.py
# See http://natron.readthedocs.org/en/master/devel/groups.html#adding-hand-written-code-callbacks-etc
# Note that Viewers are never exported

import NatronEngine
import sys

# Try to import the extensions file where callbacks and hand-written code should be located.
try:
    from SubtleMoveExt import *
except ImportError:
    pass

def getPluginID():
    return "vv.SubtleMove"

def getLabel():
    return "SubtleMove"

def getVersion():
    return 1

def getIconPath():
    return "Animation.png"

def getGrouping():
    return "videovina/Animations"

def createInstance(app,group):
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    lastNode.setColor(0.702, 0.702, 0.702)
    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("subtle_move.main")
        del param


    # Create the user parameters
    lastNode.control = lastNode.createPageParam("control", "Control")
    param = lastNode.createStringParam("state_label", "State")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)
    param.setDefaultValue("- - - - - - - >    STATE :")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setEvaluateOnChange(False)
    param.setAnimationEnabled(False)
    lastNode.state_label = param
    del param

    param = lastNode.createChoiceParam("format", "Format")
    entries = [ ("Quarter HD - 480 x 270", ""),
    ("Half HD - 960 x 540", ""),
    ("Full HD - 1920 x 1080", ""),
    ("4K - 3840 x 2160", "")]
    param.setOptions(entries)
    del entries
    param.setDefaultValue("Full HD - 1920 x 1080")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.format = param
    del param

    param = lastNode.createChoiceParam("speed", "Speed")
    entries = [ ("Slow", ""),
    ("Normal", ""),
    ("Fast", "")]
    param.setOptions(entries)
    del entries
    param.setDefaultValue("Normal")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    lastNode.speed = param
    del param

    param = lastNode.createButtonParam("link", "Link To Parent")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setEvaluateOnChange(False)
    lastNode.link = param
    del param

    param = lastNode.createButtonParam("refresh", "Refresh")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setEvaluateOnChange(False)
    lastNode.refresh = param
    del param

    param = lastNode.createSeparatorParam("sep3", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    lastNode.sep3 = param
    del param

    param = lastNode.createStringParam("time_label", "")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)
    param.setDefaultValue("- - - - - - - >    TIME :")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setEvaluateOnChange(False)
    param.setAnimationEnabled(False)
    lastNode.time_label = param
    del param

    param = lastNode.createInt3DParam("durations", "Durations")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)
    param.setDisplayMinimum(0, 1)
    param.setDisplayMaximum(100, 1)
    param.setDefaultValue(0, 1)
    param.restoreDefaultValue(1)
    param.setDisplayMinimum(0, 2)
    param.setDisplayMaximum(100, 2)
    param.setDefaultValue(0, 2)
    param.restoreDefaultValue(2)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(150, 0)
    param.setValue(100, 1)
    param.setValue(50, 2)
    lastNode.durations = param
    del param

    param = lastNode.createSeparatorParam("sep6", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    lastNode.sep6 = param
    del param

    param = lastNode.createStringParam("settings_label", "")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)
    param.setDefaultValue("- - - - - - - >    SETTINGS :")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setEvaluateOnChange(False)
    param.setAnimationEnabled(False)
    lastNode.settings_label = param
    del param

    param = lastNode.createChoiceParam("movement", "Movement")
    entries = [ ("Left - Right", ""),
    ("Right - Left", ""),
    ("Up - Down", ""),
    ("Down - Up", ""),
    ("Zoom In", ""),
    ("Zoom Out", ""),
    ("Rotate to Right", ""),
    ("Rotate to Left", ""),
    ("", "")]
    param.setOptions(entries)
    del entries
    param.setDefaultValue("Zoom In")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.set("Left - Right")
    lastNode.movement = param
    del param

    param = lastNode.createDoubleParam("level", "Level")
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
    param.setValue(3, 0)
    lastNode.level = param
    del param

    param = lastNode.createDoubleParam("scale_offset", "Scale Offset")
    param.setMinimum(-2147483648, 0)
    param.setMaximum(2147483647, 0)
    param.setDisplayMinimum(-1, 0)
    param.setDisplayMaximum(1, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    lastNode.scale_offset = param
    del param

    param = lastNode.createBooleanParam("center", "Center From Input")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("Centra el pivote a partir del formato de la imagen.")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.center = param
    del param

    param = lastNode.createBooleanParam("image_within_format", "Image Within Format")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("Mantiene la imagen dentro del formato.")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    lastNode.image_within_format = param
    del param

    param = lastNode.createSeparatorParam("sep7", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    lastNode.sep7 = param
    del param

    param = lastNode.createDoubleParam("exaggeration", "Exaggeration")
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
    param.setValue(0.7, 0)
    lastNode.exaggeration = param
    del param

    param = lastNode.createIntParam("break_point", "Break Point")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("Porcentaje donde la animacion va a tener un quebre rapido")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(50, 0)
    lastNode.break_point = param
    del param

    param = lastNode.createIntParam("break_point_duration", "Break Point Duration")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    param.setValue(20, 0)
    lastNode.break_point_duration = param
    del param

    param = lastNode.createSeparatorParam("sep9", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    lastNode.sep9 = param
    del param

    param = lastNode.createStringParam("shaker_label", "")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)
    param.setDefaultValue("- - - - - - - >    SHAKER:")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setEvaluateOnChange(False)
    param.setAnimationEnabled(False)
    lastNode.shaker_label = param
    del param

    param = lastNode.createDoubleParam("translate_shaker", "Translate Shaker")
    param.setMinimum(-2147483648, 0)
    param.setMaximum(2147483647, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.translate_shaker = param
    del param

    param = lastNode.createDoubleParam("scale_shaker", "Scale Shaker")
    param.setMinimum(0, 0)
    param.setMaximum(2147483647, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(1, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.scale_shaker = param
    del param

    param = lastNode.createDoubleParam("rotate_shaker", "Rotate Shaker")
    param.setMinimum(0, 0)
    param.setMaximum(180, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(180, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.rotate_shaker = param
    del param

    param = lastNode.createSeparatorParam("sep10", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    lastNode.sep10 = param
    del param

    param = lastNode.createDoubleParam("frequency", "Frequency")
    param.setMinimum(1, 0)
    param.setMaximum(100, 0)
    param.setDisplayMinimum(1, 0)
    param.setDisplayMaximum(100, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(50, 0)
    lastNode.frequency = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    # Start of node "Output1"
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setLabel("Output")
    lastNode.setPosition(767, 295)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupOutput1 = lastNode

    del lastNode
    # End of node "Output1"

    # Start of node "Image"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Image")
    lastNode.setLabel("Image")
    lastNode.setPosition(767, 171)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupImage = lastNode

    del lastNode
    # End of node "Image"

    # Start of node "Transform"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("Transform")
    lastNode.setLabel("Transform")
    lastNode.setPosition(767, 253)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupTransform = lastNode

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "Transform"

    # Start of node "Modulate1"
    lastNode = app.createNode("net.fxarena.openfx.Modulate", 1, group)
    lastNode.setScriptName("Modulate1")
    lastNode.setLabel("Modulate1")
    lastNode.setPosition(769, 211)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupModulate1 = lastNode

    param = lastNode.getParam("hostMix")
    if param is not None:
        param.setValue(0, 0)
        del param

    del lastNode
    # End of node "Modulate1"

    # Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, groupTransform)
    groupTransform.connectInput(0, groupModulate1)
    groupModulate1.connectInput(0, groupImage)

    try:
        extModule = sys.modules["SubtleMoveExt"]
    except KeyError:
        extModule = None
    if extModule is not None and hasattr(extModule ,"createInstanceExt") and hasattr(extModule.createInstanceExt,"__call__"):
        extModule.createInstanceExt(app,group)
