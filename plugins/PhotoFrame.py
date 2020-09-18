# -*- coding: utf-8 -*-
# DO NOT EDIT THIS FILE
# Natron PyPlug
# This file was automatically generated by Natron PyPlug exporter version 10.

# Hand-written code should be added in a separate file named PhotoFrameExt.py
# See http://natron.readthedocs.org/en/master/devel/groups.html#adding-hand-written-code-callbacks-etc
# Note that Viewers are never exported

import NatronEngine
import sys

# Try to import the extensions file where callbacks and hand-written code should be located.
try:
    from PhotoFrameExt import *
except ImportError:
    pass

def getPluginID():
    return "vv.PhotoFrame"

def getLabel():
    return "PhotoFrame"

def getVersion():
    return 1

def getIconPath():
    return "PhotoFrame.png"

def getGrouping():
    return "videovina/Draw"

def createInstance(app,group):
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    lastNode.setColor(0.7, 0.7, 0.7)
    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("photo_frame.main")
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
    param.setDefaultValue(2)
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
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

    param = lastNode.createSeparatorParam("sep5", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    lastNode.sep5 = param
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

    param = lastNode.createIntParam("duration_percent", "Duration Percent %")
    param.setMinimum(0, 0)
    param.setMaximum(100, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(100, 0)
    lastNode.duration_percent = param
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
    param.setAddNewLine(False)
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

    param = lastNode.createStringParam("texts_label", "")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)
    param.setDefaultValue("- - - - - - - >    TEXT :")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setEvaluateOnChange(False)
    param.setAnimationEnabled(False)
    lastNode.texts_label = param
    del param

    param = lastNode.createFileParam("font", "Font")
    param.setSequenceEnabled(False)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    param.setValue("/home/pancho/Documents/GitHub/videovina/private/fonts/Major Shift.ttf")
    lastNode.font = param
    del param

    param = lastNode.createSeparatorParam("sep8", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    lastNode.sep8 = param
    del param

    param = lastNode.createStringParam("title", "Title")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeDefault)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue("Title")
    lastNode.title = param
    del param

    param = lastNode.createStringParam("subtitle", "Subtitle")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeDefault)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue("Subtitle")
    lastNode.subtitle = param
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

    param = lastNode.createColorParam("title_color", "Title Color", False)
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
    param.setValue(0.1, 0)
    param.setValue(0.1, 1)
    param.setValue(0.1, 2)
    lastNode.title_color = param
    del param

    param = lastNode.createColorParam("subtitle_color", "Subtitle Color", False)
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
    param.setValue(0.3, 0)
    param.setValue(0.3, 1)
    param.setValue(0.3, 2)
    lastNode.subtitle_color = param
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

    param = lastNode.createDoubleParam("corner_radius", "Corner Radius")
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
    lastNode.corner_radius = param
    del param

    param = lastNode.createDoubleParam("frame_width", "Frame Width %")
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
    param.setValue(10, 0)
    lastNode.frame_width = param
    del param

    param = lastNode.createDoubleParam("bottom_margin", "Bottom Margin %")
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
    param.setValue(25, 0)
    lastNode.bottom_margin = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    # Start of node "Output1"
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setLabel("Output")
    lastNode.setPosition(909, 1261)
    lastNode.setSize(100, 29)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupOutput1 = lastNode

    del lastNode
    # End of node "Output1"

    # Start of node "Photo"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Photo")
    lastNode.setLabel("Photo")
    lastNode.setPosition(907, 89)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupPhoto = lastNode

    del lastNode
    # End of node "Photo"

    # Start of node "photo_mask"
    lastNode = app.createNode("net.sf.openfx.Rectangle", 2, group)
    lastNode.setScriptName("photo_mask")
    lastNode.setLabel("photo_mask")
    lastNode.setPosition(1161, 251)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupphoto_mask = lastNode

    param = lastNode.getParam("NatronParamFormatChoice")
    if param is not None:
        param.set("PC_Video")
        del param

    param = lastNode.getParam("bottomLeft")
    if param is not None:
        param.setValue(48, 0)
        param.setValue(48, 1)
        del param

    param = lastNode.getParam("size")
    if param is not None:
        param.setValue(1824, 0)
        param.setValue(984, 1)
        del param

    param = lastNode.getParam("cornerRadius")
    if param is not None:
        param.setValue(20, 0)
        param.setValue(20, 1)
        del param

    del lastNode
    # End of node "photo_mask"

    # Start of node "Shuffle1"
    lastNode = app.createNode("net.sf.openfx.ShufflePlugin", 3, group)
    lastNode.setScriptName("Shuffle1")
    lastNode.setLabel("Shuffle1")
    lastNode.setPosition(907, 251)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.6, 0.24, 0.39)
    groupShuffle1 = lastNode

    param = lastNode.getParam("outputA")
    if param is not None:
        param.set("A.uk.co.thefoundry.OfxImagePlaneColour.A")
        del param

    del lastNode
    # End of node "Shuffle1"

    # Start of node "Premult1"
    lastNode = app.createNode("net.sf.openfx.Premult", 2, group)
    lastNode.setScriptName("Premult1")
    lastNode.setLabel("Premult1")
    lastNode.setPosition(907, 359)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupPremult1 = lastNode

    del lastNode
    # End of node "Premult1"

    # Start of node "rectangle"
    lastNode = app.createNode("net.sf.openfx.Rectangle", 2, group)
    lastNode.setScriptName("rectangle")
    lastNode.setLabel("rectangle")
    lastNode.setPosition(646, 483)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.3, 0.5, 0.2)
    grouprectangle = lastNode

    param = lastNode.getParam("NatronParamFormatSize")
    if param is not None:
        param.setValue(1920, 0)
        param.setValue(1080, 1)
        del param

    param = lastNode.getParam("bottomLeft")
    if param is not None:
        param.setValue(-270, 1)
        del param

    param = lastNode.getParam("size")
    if param is not None:
        param.setValue(1350, 1)
        del param

    param = lastNode.getParam("cornerRadius")
    if param is not None:
        param.setValue(20, 0)
        param.setValue(20, 1)
        del param

    del lastNode
    # End of node "rectangle"

    # Start of node "Merge1"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge1")
    lastNode.setLabel("Merge1")
    lastNode.setPosition(907, 472)
    lastNode.setSize(100, 55)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge1 = lastNode

    param = lastNode.getParam("operation")
    if param is not None:
        param.set("under")
        del param

    del lastNode
    # End of node "Merge1"

    # Start of node "transform"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("transform")
    lastNode.setLabel("transform")
    lastNode.setPosition(909, 1106)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    grouptransform = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(108.6390532544379, 1)
        del param

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValue(0.7988165680473372, 0)
        param.setValue(0.7988165680473372, 1)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "transform"

    # Start of node "text_bbox"
    lastNode = app.createNode("net.sf.openfx.ConstantPlugin", 1, group)
    lastNode.setScriptName("text_bbox")
    lastNode.setLabel("text_bbox")
    lastNode.setPosition(1181, 511)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.3, 0.5, 0.2)
    grouptext_bbox = lastNode

    param = lastNode.getParam("extent")
    if param is not None:
        param.set("size")
        del param

    param = lastNode.getParam("NatronParamFormatChoice")
    if param is not None:
        param.set("PC_Video")
        del param

    param = lastNode.getParam("bottomLeft")
    if param is not None:
        param.setValue(48, 0)
        param.setValue(-246, 1)
        del param

    param = lastNode.getParam("size")
    if param is not None:
        param.setValue(1824, 0)
        param.setValue(270, 1)
        del param

    param = lastNode.getParam("color")
    if param is not None:
        param.setValue(0.632, 0)
        param.setValue(1, 1)
        param.setValue(0.632, 2)
        param.setValue(1, 3)
        del param

    del lastNode
    # End of node "text_bbox"

    # Start of node "merge"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("merge")
    lastNode.setLabel("merge")
    lastNode.setPosition(909, 715)
    lastNode.setSize(100, 55)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupmerge = lastNode

    del lastNode
    # End of node "merge"

    # Start of node "text_fit"
    lastNode = app.createNode("vv.TextFit", 1, group)
    lastNode.setScriptName("text_fit")
    lastNode.setLabel("text_fit")
    lastNode.setPosition(1181, 570)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.7, 0.7, 0.7)
    grouptext_fit = lastNode

    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("text_fit.main")
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
    param.setEnabled(False, 0)
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
    param.set("Full HD - 1920 x 1080")
    param.setEnabled(False, 0)
    lastNode.format = param
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

    param = lastNode.createSeparatorParam("sep5", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    param.setEnabled(False, 0)
    lastNode.sep5 = param
    del param

    param = lastNode.createStringParam("texts_label", "")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)
    param.setDefaultValue("- - - - - - - >    TEXT :")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setEvaluateOnChange(False)
    param.setAnimationEnabled(False)
    lastNode.texts_label = param
    del param

    param = lastNode.createStringParam("title", "Title")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeDefault)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue("Title")
    param.setEnabled(False, 0)
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
    param.setValue("Subtitle")
    param.setEnabled(False, 0)
    lastNode.subtitle = param
    del param

    param = lastNode.createFileParam("font", "Font")
    param.setSequenceEnabled(False)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    param.setValue("/home/pancho/Documents/GitHub/videovina/private/fonts/Major Shift.ttf")
    param.setEnabled(False, 0)
    lastNode.font = param
    del param

    param = lastNode.createSeparatorParam("sep7", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    param.setEnabled(False, 0)
    lastNode.sep7 = param
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

    param = lastNode.createIntParam("font_size_title", "Title Font Size")
    param.setMinimum(0, 0)
    param.setMaximum(2000, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(1000, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(133, 0)
    lastNode.font_size_title = param
    del param

    param = lastNode.createInt2DParam("title_position", "Title Position")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)
    param.setDisplayMinimum(0, 1)
    param.setDisplayMaximum(100, 1)
    param.setDefaultValue(0, 1)
    param.restoreDefaultValue(1)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    param.setValue(75, 0)
    param.setValue(25, 1)
    lastNode.title_position = param
    del param

    param = lastNode.createIntParam("title_max_size", "Title Max Size %")
    param.setMinimum(0, 0)
    param.setMaximum(100, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(78, 0)
    lastNode.title_max_size = param
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

    param = lastNode.createIntParam("font_size_subtitle", "Subtitle Font Size")
    param.setMinimum(0, 0)
    param.setMaximum(2000, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(1000, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(171, 0)
    lastNode.font_size_subtitle = param
    del param

    param = lastNode.createInt2DParam("subtitle_position", "Subtitle Position")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)
    param.setDisplayMinimum(0, 1)
    param.setDisplayMaximum(100, 1)
    param.setDefaultValue(0, 1)
    param.restoreDefaultValue(1)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    param.setValue(665, 0)
    param.setValue(15, 1)
    lastNode.subtitle_position = param
    del param

    param = lastNode.createIntParam("subtitle_max_size", "Subtitle Max Size %")
    param.setMinimum(0, 0)
    param.setMaximum(100, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(100, 0)
    lastNode.subtitle_max_size = param
    del param

    param = lastNode.createSeparatorParam("sep4", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    lastNode.sep4 = param
    del param

    param = lastNode.createChoiceParam("align", "Text Align")
    entries = [ ("Right", ""),
    ("Left", ""),
    ("Center", "")]
    param.setOptions(entries)
    del entries
    param.setDefaultValue("Center")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.align = param
    del param

    param = lastNode.createBooleanParam("one_line", "One Line")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    param.setValue(True)
    lastNode.one_line = param
    del param

    param = lastNode.createButtonParam("separate_text", "Separate Text")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setEvaluateOnChange(False)
    lastNode.separate_text = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode
    # End of node "text_fit"

    # Start of node "title_node"
    lastNode = app.createNode("net.fxarena.openfx.Text", 6, group)
    lastNode.setScriptName("title_node")
    lastNode.setLabel("title_node")
    lastNode.setPosition(1381, 570)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.3, 0.5, 0.2)
    grouptitle_node = lastNode

    param = lastNode.getParam("autoSize")
    if param is not None:
        param.setValue(True)
        del param

    param = lastNode.getParam("text")
    if param is not None:
        param.setValue("Title")
        del param

    param = lastNode.getParam("custom")
    if param is not None:
        param.setValue("/home/pancho/Documents/GitHub/videovina/private/fonts/Major Shift.ttf")
        del param

    param = lastNode.getParam("font")
    if param is not None:
        param.setValue("Major Snafu")
        del param

    param = lastNode.getParam("size")
    if param is not None:
        param.setValue(133, 0)
        del param

    param = lastNode.getParam("color")
    if param is not None:
        param.setValue(0.1, 0)
        param.setValue(0.1, 1)
        param.setValue(0.1, 2)
        del param

    del lastNode
    # End of node "title_node"

    # Start of node "subtitle_node"
    lastNode = app.createNode("net.fxarena.openfx.Text", 6, group)
    lastNode.setScriptName("subtitle_node")
    lastNode.setLabel("subtitle_node")
    lastNode.setPosition(1581, 570)
    lastNode.setSize(100, 29)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupsubtitle_node = lastNode

    param = lastNode.getParam("autoSize")
    if param is not None:
        param.setValue(True)
        del param

    param = lastNode.getParam("text")
    if param is not None:
        param.setValue("Subtitle")
        del param

    param = lastNode.getParam("custom")
    if param is not None:
        param.setValue("/home/pancho/Documents/GitHub/videovina/private/fonts/Major Shift.ttf")
        del param

    param = lastNode.getParam("font")
    if param is not None:
        param.setValue("Major Snafu")
        del param

    param = lastNode.getParam("size")
    if param is not None:
        param.setValue(171, 0)
        del param

    param = lastNode.getParam("color")
    if param is not None:
        param.setValue(0.3, 0)
        param.setValue(0.3, 1)
        param.setValue(0.3, 2)
        del param

    del lastNode
    # End of node "subtitle_node"

    # Start of node "title_transform"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("title_transform")
    lastNode.setLabel("title_transform")
    lastNode.setPosition(1381, 620)
    lastNode.setSize(100, 29)
    lastNode.setColor(0.7, 0.3, 0.1)
    grouptitle_transform = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(123, 0)
        param.setValue(-221, 1)
        del param

    param = lastNode.getParam("center")
    if param is not None:
        param.setValue(837, 0)
        param.setValue(110, 1)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "title_transform"

    # Start of node "subtitle_transform"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("subtitle_transform")
    lastNode.setLabel("subtitle_transform")
    lastNode.setPosition(1581, 620)
    lastNode.setSize(100, 29)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupsubtitle_transform = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(713, 0)
        param.setValue(-231, 1)
        del param

    param = lastNode.getParam("center")
    if param is not None:
        param.setValue(247, 0)
        param.setValue(120, 1)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "subtitle_transform"

    # Start of node "titles_merge"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("titles_merge")
    lastNode.setLabel("titles_merge")
    lastNode.setPosition(1581, 720)
    lastNode.setSize(100, 45)
    lastNode.setColor(0.3, 0.37, 0.776)
    grouptitles_merge = lastNode

    param = lastNode.getParam("userTextArea")
    if param is not None:
        param.setValue("<Natron>(over)</Natron>")
        del param

    del lastNode
    # End of node "titles_merge"

    # Start of node "photo_transform"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("photo_transform")
    lastNode.setLabel("photo_transform")
    lastNode.setPosition(907, 149)
    lastNode.setSize(100, 55)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupphoto_transform = lastNode

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValue(0.95, 0)
        param.setValue(0.95, 1)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "photo_transform"

    # Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, grouptransform)
    groupShuffle1.connectInput(0, groupphoto_transform)
    groupShuffle1.connectInput(1, groupphoto_mask)
    groupPremult1.connectInput(0, groupShuffle1)
    groupMerge1.connectInput(0, groupPremult1)
    groupMerge1.connectInput(1, grouprectangle)
    grouptransform.connectInput(0, groupmerge)
    groupmerge.connectInput(0, groupMerge1)
    groupmerge.connectInput(1, grouptitles_merge)
    grouptext_fit.connectInput(0, grouptext_bbox)
    grouptitle_transform.connectInput(0, grouptitle_node)
    groupsubtitle_transform.connectInput(0, groupsubtitle_node)
    grouptitles_merge.connectInput(0, grouptitle_transform)
    grouptitles_merge.connectInput(1, groupsubtitle_transform)
    groupphoto_transform.connectInput(0, groupPhoto)

    param = grouptext_fit.getParam("state_label")
    group.getParam("state_label").setAsAlias(param)
    del param
    param = grouptext_fit.getParam("format")
    group.getParam("format").setAsAlias(param)
    del param
    param = grouptext_fit.getParam("sep5")
    group.getParam("sep5").setAsAlias(param)
    del param
    param = grouptext_fit.getParam("title")
    group.getParam("title").setAsAlias(param)
    del param
    param = grouptext_fit.getParam("subtitle")
    group.getParam("subtitle").setAsAlias(param)
    del param
    param = grouptext_fit.getParam("font")
    group.getParam("font").setAsAlias(param)
    del param
    param = grouptext_fit.getParam("sep7")
    group.getParam("sep7").setAsAlias(param)
    del param

    try:
        extModule = sys.modules["PhotoFrameExt"]
    except KeyError:
        extModule = None
    if extModule is not None and hasattr(extModule ,"createInstanceExt") and hasattr(extModule.createInstanceExt,"__call__"):
        extModule.createInstanceExt(app,group)
