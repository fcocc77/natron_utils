# -*- coding: utf-8 -*-
# DO NOT EDIT THIS FILE
# Natron PyPlug
# This file was automatically generated by Natron PyPlug exporter version 10.

# Hand-written code should be added in a separate file named ZoomTransitionExt.py
# See http://natron.readthedocs.org/en/master/devel/groups.html#adding-hand-written-code-callbacks-etc
# Note that Viewers are never exported

import NatronEngine
import sys

# Try to import the extensions file where callbacks and hand-written code should be located.
try:
    from ZoomTransitionExt import *
except ImportError:
    pass

def getPluginID():
    return "vv.ZoomTransition"

def getLabel():
    return "ZoomTransition"

def getVersion():
    return 1

def getIconPath():
    return "Transition.png"

def getGrouping():
    return "videovina/Transitions"

def createInstance(app,group):
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    lastNode.setColor(0.7, 0.7, 0.7)
    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("zoom_transition.main")
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
    param.setDefaultValue(1)
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
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

    param = lastNode.createIntParam("start_frame", "Start Frame")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(1, 0)
    lastNode.start_frame = param
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
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    param.setValue(100, 0)
    param.setValue(100, 1)
    param.setValue(25, 2)
    lastNode.durations = param
    del param

    param = lastNode.createSeparatorParam("sep6", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
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

    param = lastNode.createDoubleParam("src_scale", "Src Scale")
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
    lastNode.src_scale = param
    del param

    param = lastNode.createIntParam("src_rotate", "Src Rotate")
    param.setMinimum(-180, 0)
    param.setMaximum(180, 0)
    param.setDisplayMinimum(-180, 0)
    param.setDisplayMaximum(180, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    param.setValue(10, 0)
    lastNode.src_rotate = param
    del param

    param = lastNode.createDoubleParam("dst_scale", "Dst Scale")
    param.setMinimum(1, 0)
    param.setMaximum(5, 0)
    param.setDisplayMinimum(1, 0)
    param.setDisplayMaximum(5, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(3, 0)
    lastNode.dst_scale = param
    del param

    param = lastNode.createIntParam("dst_rotate", "Dst Rotate")
    param.setMinimum(-180, 0)
    param.setMaximum(180, 0)
    param.setDisplayMinimum(-180, 0)
    param.setDisplayMaximum(180, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    param.setValue(-10, 0)
    lastNode.dst_rotate = param
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

    param = lastNode.createDoubleParam("blur", "Blur")
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
    param.setValue(100, 0)
    lastNode.blur = param
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

    param = lastNode.createStringParam("flares_label", "")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)
    param.setDefaultValue("- - - - - - - >    FLARES :")
    param.restoreDefaultValue()

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setEvaluateOnChange(False)
    param.setAnimationEnabled(False)
    lastNode.flares_label = param
    del param

    param = lastNode.createPathParam("flares_folder", "Flares Folder")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setAddNewLine(True)
    param.setValue("/home/pancho/Documents/develop/videovina/private/assets/flares_transition")
    lastNode.flares_folder = param
    del param

    param = lastNode.createChoiceParam("flares", "Flares")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.flares = param
    del param

    param = lastNode.createButtonParam("reload_flares", "Reload Flares")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setEvaluateOnChange(False)
    lastNode.reload_flares = param
    del param

    param = lastNode.createDoubleParam("flares_opacity", "Flares Opacity")
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
    lastNode.flares_opacity = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    # Start of node "Output1"
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setLabel("Output")
    lastNode.setPosition(974, 911)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupOutput1 = lastNode

    del lastNode
    # End of node "Output1"

    # Start of node "A"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("A")
    lastNode.setLabel("A")
    lastNode.setPosition(757, 140)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupA = lastNode

    del lastNode
    # End of node "A"

    # Start of node "B"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("B")
    lastNode.setLabel("B")
    lastNode.setPosition(1148, 154)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupB = lastNode

    del lastNode
    # End of node "B"

    # Start of node "Dissolve1"
    lastNode = app.createNode("net.sf.openfx.DissolvePlugin", 1, group)
    lastNode.setScriptName("Dissolve1")
    lastNode.setLabel("Dissolve1")
    lastNode.setPosition(981, 344)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupDissolve1 = lastNode

    param = lastNode.getParam("which")
    if param is not None:
        param.setValueAtTime(0, 26, 0)
        param.setValueAtTime(0.3, 43.5, 0)
        param.setValueAtTime(1.7, 58.5, 0)
        param.setValueAtTime(2, 76, 0)
        del param

    del lastNode
    # End of node "Dissolve1"

    # Start of node "src_transform"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("src_transform")
    lastNode.setLabel("src_transform")
    lastNode.setPosition(757, 286)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupsrc_transform = lastNode

    param = lastNode.getParam("rotate")
    if param is not None:
        param.setValueAtTime(0, 1, 0)
        param.setValueAtTime(1.5, 36, 0)
        param.setValueAtTime(8.5, 66, 0)
        param.setValueAtTime(10, 101, 0)
        del param

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValueAtTime(1, 1, 0)
        param.setValueAtTime(0.85, 36, 0)
        param.setValueAtTime(0.15, 66, 0)
        param.setValueAtTime(0, 101, 0)
        param.setValueAtTime(1, 1, 1)
        param.setValueAtTime(0.85, 36, 1)
        param.setValueAtTime(0.15, 66, 1)
        param.setValueAtTime(0, 101, 1)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "src_transform"

    # Start of node "dst_transform"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("dst_transform")
    lastNode.setLabel("dst_transform")
    lastNode.setPosition(1148, 344)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupdst_transform = lastNode

    param = lastNode.getParam("rotate")
    if param is not None:
        param.setValueAtTime(-10, 1, 0)
        param.setValueAtTime(-8.5, 36, 0)
        param.setValueAtTime(-1.5, 66, 0)
        param.setValueAtTime(0, 101, 0)
        del param

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValueAtTime(3, 1, 0)
        param.setValueAtTime(2.7, 36, 0)
        param.setValueAtTime(1.3, 66, 0)
        param.setValueAtTime(1, 101, 0)
        param.setValueAtTime(3, 1, 1)
        param.setValueAtTime(2.7, 36, 1)
        param.setValueAtTime(1.3, 66, 1)
        param.setValueAtTime(1, 101, 1)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "dst_transform"

    # Start of node "src_blur"
    lastNode = app.createNode("net.sf.cimg.CImgBlur", 4, group)
    lastNode.setScriptName("src_blur")
    lastNode.setLabel("src_blur")
    lastNode.setPosition(757, 344)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.8, 0.5, 0.3)
    groupsrc_blur = lastNode

    param = lastNode.getParam("size")
    if param is not None:
        param.setValueAtTime(0, 1, 0)
        param.setValueAtTime(30, 36, 0)
        param.setValueAtTime(170, 66, 0)
        param.setValueAtTime(200, 101, 0)
        param.setValueAtTime(0, 1, 1)
        param.setValueAtTime(30, 36, 1)
        param.setValueAtTime(170, 66, 1)
        param.setValueAtTime(200, 101, 1)
        del param

    del lastNode
    # End of node "src_blur"

    # Start of node "reformat"
    lastNode = app.createNode("net.sf.openfx.Reformat", 1, group)
    lastNode.setScriptName("reformat")
    lastNode.setLabel("reformat")
    lastNode.setPosition(981, 246)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupreformat = lastNode

    param = lastNode.getParam("reformatType")
    if param is not None:
        param.set("box")
        del param

    param = lastNode.getParam("NatronParamFormatChoice")
    if param is not None:
        param.set("PC_Video")
        del param

    param = lastNode.getParam("NatronParamFormatSize")
    if param is not None:
        param.setValue(2560, 0)
        param.setValue(1440, 1)
        del param

    param = lastNode.getParam("boxSize")
    if param is not None:
        param.setValue(1920, 0)
        param.setValue(1080, 1)
        del param

    param = lastNode.getParam("boxFixed")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "reformat"

    # Start of node "limit"
    lastNode = app.createNode("net.sf.openfx.switchPlugin", 1, group)
    lastNode.setScriptName("limit")
    lastNode.setLabel("limit")
    lastNode.setPosition(974, 805)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.3, 0.37, 0.776)
    grouplimit = lastNode

    param = lastNode.getParam("which")
    if param is not None:
        param.setValueAtTime(0, 0, 0)
        param.setValueAtTime(1, 1, 0)
        param.setValueAtTime(1, 100, 0)
        param.setValueAtTime(2, 101, 0)
        del param

    del lastNode
    # End of node "limit"

    # Start of node "Merge1"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge1")
    lastNode.setLabel("Merge1")
    lastNode.setPosition(981, 442)
    lastNode.setSize(104, 55)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge1 = lastNode

    param = lastNode.getParam("operation")
    if param is not None:
        param.set("screen")
        del param

    param = lastNode.getParam("userTextArea")
    if param is not None:
        param.setValue("<Natron>(over)</Natron>")
        del param

    del lastNode
    # End of node "Merge1"

    # Start of node "FlareTransition"
    lastNode = app.createNode("vv.FlareTransition", 1, group)
    lastNode.setScriptName("FlareTransition")
    lastNode.setLabel("FlareTransition")
    lastNode.setPosition(1242, 453)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupFlareTransition = lastNode

    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("flare_transition.main")
        del param


    # Create the user parameters
    lastNode.control = lastNode.createPageParam("control", "Control")
    param = lastNode.createStringParam("state_label", "")
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
    param.setEnabled(False, 0)
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
    param.setEnabled(False, 0)
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
    param.setHelp("")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    param.setEnabled(False, 0)
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

    param = lastNode.createIntParam("start_frame", "Start Frame")
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
    param.setValue(1, 0)
    param.setEnabled(False, 0)
    lastNode.start_frame = param
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
    param.setValue(100, 0)
    param.setValue(100, 1)
    param.setValue(25, 2)
    param.setEnabled(False, 0)
    param.setEnabled(False, 1)
    param.setEnabled(False, 2)
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
    param.setEnabled(False, 0)
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

    param = lastNode.createPathParam("flares_folder", "Flares Folder")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setValue("/home/pancho/Documents/develop/videovina/private/assets/flares_transition")
    param.setEnabled(False, 0)
    lastNode.flares_folder = param
    del param

    param = lastNode.createChoiceParam("flares", "Flares")
    entries = [ ("1 - Colourful optical flares", "colourful_optical_flares"),
    ("2 - Cool flare bokeh wipes", "cool_flare_bokeh_wipes"),
    ("3 - Flare bokeh wipes", "flare_bokeh_wipes"),
    ("4 - Flare color gradient", "flare_color_gradient"),
    ("5 - More spectral colour flares", "more_spectral_colour_flares"),
    ("6 - Red flare", "red_flare"),
    ("7 - Spectral colour flares", "spectral_colour_flares"),
    ("8 - Two flares blue and red", "two_flares_blue_and_red")]
    param.setOptions(entries)
    del entries

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setEnabled(False, 0)
    lastNode.flares = param
    del param

    param = lastNode.createButtonParam("reload_flares", "Reload Flares")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setEvaluateOnChange(False)
    lastNode.reload_flares = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode
    # End of node "FlareTransition"

    # Start of node "Modulate1"
    lastNode = app.createNode("net.fxarena.openfx.Modulate", 1, group)
    lastNode.setScriptName("Modulate1")
    lastNode.setLabel("Modulate1")
    lastNode.setPosition(1150, 292)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupModulate1 = lastNode

    param = lastNode.getParam("hostMix")
    if param is not None:
        param.setValue(0, 0)
        del param

    del lastNode
    # End of node "Modulate1"

    # Start of node "Modulate1_2"
    lastNode = app.createNode("net.fxarena.openfx.Modulate", 1, group)
    lastNode.setScriptName("Modulate1_2")
    lastNode.setLabel("Modulate1_2")
    lastNode.setPosition(759, 229)
    lastNode.setSize(100, 32)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupModulate1_2 = lastNode

    param = lastNode.getParam("hostMix")
    if param is not None:
        param.setValue(0, 0)
        del param

    del lastNode
    # End of node "Modulate1_2"

    # Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, grouplimit)
    groupDissolve1.connectInput(0, groupsrc_blur)
    groupDissolve1.connectInput(1, groupreformat)
    groupDissolve1.connectInput(3, groupdst_transform)
    groupsrc_transform.connectInput(0, groupModulate1_2)
    groupdst_transform.connectInput(0, groupModulate1)
    groupsrc_blur.connectInput(0, groupsrc_transform)
    grouplimit.connectInput(0, groupA)
    grouplimit.connectInput(1, groupMerge1)
    grouplimit.connectInput(2, groupB)
    groupMerge1.connectInput(0, groupDissolve1)
    groupMerge1.connectInput(1, groupFlareTransition)
    groupModulate1.connectInput(0, groupB)
    groupModulate1_2.connectInput(0, groupA)

    param = groupMerge1.getParam("mix")
    param.slaveTo(group.getParam("flares_opacity"), 0, 0)
    del param
    param = groupFlareTransition.getParam("format")
    group.getParam("format").setAsAlias(param)
    del param
    param = groupFlareTransition.getParam("speed")
    group.getParam("speed").setAsAlias(param)
    del param
    param = groupFlareTransition.getParam("sep5")
    group.getParam("sep5").setAsAlias(param)
    del param
    param = groupFlareTransition.getParam("start_frame")
    group.getParam("start_frame").setAsAlias(param)
    del param
    param = groupFlareTransition.getParam("durations")
    group.getParam("durations").setAsAlias(param)
    del param
    param = groupFlareTransition.getParam("sep6")
    group.getParam("sep6").setAsAlias(param)
    del param
    param = groupFlareTransition.getParam("flares_folder")
    group.getParam("flares_folder").setAsAlias(param)
    del param
    param = groupFlareTransition.getParam("flares")
    group.getParam("flares").setAsAlias(param)
    del param

    try:
        extModule = sys.modules["ZoomTransitionExt"]
    except KeyError:
        extModule = None
    if extModule is not None and hasattr(extModule ,"createInstanceExt") and hasattr(extModule.createInstanceExt,"__call__"):
        extModule.createInstanceExt(app,group)
