# -*- coding: utf-8 -*-
# DO NOT EDIT THIS FILE
# Natron PyPlug
# This file was automatically generated by Natron PyPlug exporter version 10.

# Hand-written code should be added in a separate file named NoiserTransitionExt.py
# See http://natron.readthedocs.org/en/master/devel/groups.html#adding-hand-written-code-callbacks-etc
# Note that Viewers are never exported

import NatronEngine
import sys

# Try to import the extensions file where callbacks and hand-written code should be located.
try:
    from NoiserTransitionExt import *
except ImportError:
    pass

def getPluginID():
    return "vv.NoisierTransition"

def getLabel():
    return "NoisierTransition"

def getVersion():
    return 1

def getIconPath():
    return "Noisier.png"

def getGrouping():
    return "videovina/Transitions"

def createInstance(app,group):
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    lastNode.setColor(0.7, 0.7, 0.7)
    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("noisier_transition.main")
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

    param = lastNode.createChoiceParam("direction", "Direction")
    entries = [ ("Left", ""),
    ("Right", ""),
    ("Up", ""),
    ("Down", "")]
    param.setOptions(entries)
    del entries

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.direction = param
    del param

    param = lastNode.createDoubleParam("noise_size", "Noise Size")
    param.setMinimum(-2147483648, 0)
    param.setMaximum(2147483647, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(1000, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(963, 0)
    lastNode.noise_size = param
    del param

    param = lastNode.createDoubleParam("dir_blur", "Directional Blur")
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
    param.setValue(27.2, 0)
    lastNode.dir_blur = param
    del param

    param = lastNode.createDoubleParam("lacunarity", "Lacunarity")
    param.setMinimum(1, 0)
    param.setMaximum(10, 0)
    param.setDisplayMinimum(1, 0)
    param.setDisplayMaximum(10, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(2.12, 0)
    lastNode.lacunarity = param
    del param

    param = lastNode.createDoubleParam("evolution", "Evolution")
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
    param.setValue(0.058, 0)
    lastNode.evolution = param
    del param

    param = lastNode.createDoubleParam("crushed", "Crushed")
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
    param.setValue(0.894, 0)
    lastNode.crushed = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    # Start of node "Output1"
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setLabel("Output")
    lastNode.setPosition(535, 1226)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupOutput1 = lastNode

    del lastNode
    # End of node "Output1"

    # Start of node "A"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("A")
    lastNode.setLabel("A")
    lastNode.setPosition(242, 26)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupA = lastNode

    del lastNode
    # End of node "A"

    # Start of node "B"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("B")
    lastNode.setLabel("B")
    lastNode.setPosition(872, -4)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupB = lastNode

    del lastNode
    # End of node "B"

    # Start of node "KeyMix3"
    lastNode = app.createNode("net.sf.openfx.KeyMix", 1, group)
    lastNode.setScriptName("KeyMix3")
    lastNode.setLabel("KeyMix3")
    lastNode.setPosition(884, 729)
    lastNode.setSize(80, 32)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupKeyMix3 = lastNode

    param = lastNode.getParam("enableMask_Mask")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "KeyMix3"

    # Start of node "noise"
    lastNode = app.createNode("net.sf.openfx.SeNoise", 1, group)
    lastNode.setScriptName("noise")
    lastNode.setLabel("noise")
    lastNode.setPosition(1256, 484)
    lastNode.setSize(80, 32)
    lastNode.setColor(0.75, 0.75, 0.75)
    groupnoise = lastNode

    param = lastNode.getParam("noiseSize")
    if param is not None:
        param.setValue(963, 0)
        param.setValue(963, 1)
        del param

    param = lastNode.getParam("noiseZSlope")
    if param is not None:
        param.setValue(0.0058, 0)
        del param

    param = lastNode.getParam("fbmLacunarity")
    if param is not None:
        param.setValue(2.12, 0)
        del param

    param = lastNode.getParam("transformTranslate")
    if param is not None:
        param.setValueAtTime(0, 1, 0)
        param.setValueAtTime(-432.0000000000001, 36, 0)
        param.setValueAtTime(-2448, 66, 0)
        param.setValueAtTime(-2880, 101, 0)
        del param

    param = lastNode.getParam("transformScale")
    if param is not None:
        param.setValue(0.106, 1)
        del param

    del lastNode
    # End of node "noise"

    # Start of node "noise_keyer"
    lastNode = app.createNode("net.sf.openfx.KeyerPlugin", 1, group)
    lastNode.setScriptName("noise_keyer")
    lastNode.setLabel("noise_keyer")
    lastNode.setPosition(1244, 617)
    lastNode.setSize(104, 55)
    lastNode.setColor(0, 1, 0)
    groupnoise_keyer = lastNode

    param = lastNode.getParam("softnessLower")
    if param is not None:
        param.setValue(0, 0)
        del param

    param = lastNode.getParam("toleranceLower")
    if param is not None:
        param.setValueAtTime(-0.8, 1, 0)
        param.setValueAtTime(-0.71, 36, 0)
        param.setValueAtTime(-0.29, 66, 0)
        param.setValueAtTime(-0.2, 101, 0)
        del param

    del lastNode
    # End of node "noise_keyer"

    # Start of node "noise_blur"
    lastNode = app.createNode("net.sf.cimg.CImgBlur", 4, group)
    lastNode.setScriptName("noise_blur")
    lastNode.setLabel("noise_blur")
    lastNode.setPosition(1244, 721)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.8, 0.5, 0.3)
    groupnoise_blur = lastNode

    param = lastNode.getParam("size")
    if param is not None:
        param.setValue(27.2, 0)
        del param

    param = lastNode.getParam("boundary")
    if param is not None:
        param.set("nearest")
        del param

    del lastNode
    # End of node "noise_blur"

    # Start of node "duplicate_a"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("duplicate_a")
    lastNode.setLabel("duplicate_a")
    lastNode.setPosition(427, 106)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupduplicate_a = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(1920, 0)
        del param

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValue(-1, 0)
        del param

    del lastNode
    # End of node "duplicate_a"

    # Start of node "duplicate_b"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("duplicate_b")
    lastNode.setLabel("duplicate_b")
    lastNode.setPosition(1104, 84)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupduplicate_b = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(-1920, 0)
        del param

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValue(-1, 0)
        del param

    del lastNode
    # End of node "duplicate_b"

    # Start of node "Merge1"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge1")
    lastNode.setLabel("Merge1")
    lastNode.setPosition(242, 276)
    lastNode.setSize(104, 55)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge1 = lastNode

    del lastNode
    # End of node "Merge1"

    # Start of node "Dot3"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot3")
    lastNode.setLabel("Dot3")
    lastNode.setPosition(287, 115)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot3 = lastNode

    del lastNode
    # End of node "Dot3"

    # Start of node "Dot4"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot4")
    lastNode.setLabel("Dot4")
    lastNode.setPosition(917, 93)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot4 = lastNode

    del lastNode
    # End of node "Dot4"

    # Start of node "Merge2"
    lastNode = app.createNode("net.sf.openfx.MergePlugin", 1, group)
    lastNode.setScriptName("Merge2")
    lastNode.setLabel("Merge2")
    lastNode.setPosition(872, 273)
    lastNode.setSize(104, 55)
    lastNode.setColor(0.3, 0.37, 0.776)
    groupMerge2 = lastNode

    del lastNode
    # End of node "Merge2"

    # Start of node "transform_a"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("transform_a")
    lastNode.setLabel("transform_a")
    lastNode.setPosition(242, 357)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    grouptransform_a = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValueAtTime(0, 1, 0)
        param.setValueAtTime(-288.0000000000001, 36, 0)
        param.setValueAtTime(-1632, 66, 0)
        param.setValueAtTime(-1920, 101, 0)
        del param

    del lastNode
    # End of node "transform_a"

    # Start of node "transform_b"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("transform_b")
    lastNode.setLabel("transform_b")
    lastNode.setPosition(872, 352)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    grouptransform_b = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValueAtTime(1920, 1, 0)
        param.setValueAtTime(1632, 36, 0)
        param.setValueAtTime(288.0000000000001, 66, 0)
        param.setValueAtTime(0, 101, 0)
        del param

    del lastNode
    # End of node "transform_b"

    # Start of node "Dot1"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot1")
    lastNode.setLabel("Dot1")
    lastNode.setPosition(287, 738)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot1 = lastNode

    del lastNode
    # End of node "Dot1"

    # Start of node "limit"
    lastNode = app.createNode("net.sf.openfx.switchPlugin", 1, group)
    lastNode.setScriptName("limit")
    lastNode.setLabel("limit")
    lastNode.setPosition(535, 998)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.3, 0.37, 0.776)
    grouplimit = lastNode

    param = lastNode.getParam("which")
    if param is not None:
        param.setValueAtTime(0, 1, 0)
        param.setValueAtTime(1, 2, 0)
        param.setValueAtTime(1, 101, 0)
        param.setValueAtTime(2, 102, 0)
        del param

    del lastNode
    # End of node "limit"

    # Start of node "TwelveRender1"
    lastNode = app.createNode("vv.TwelveRender", 1, group)
    lastNode.setScriptName("TwelveRender1")
    lastNode.setLabel("TwelveRender1")
    lastNode.setPosition(1601, 721)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupTwelveRender1 = lastNode

    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("twelve_render.main")
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

    param = lastNode.createButtonParam("link_to_connected", "Link To Connected")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("Vincula todos los nodos conectados que tengan,\nlos atributos de videovina.")
    param.setAddNewLine(False)
    param.setEvaluateOnChange(False)
    lastNode.link_to_connected = param
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

    param = lastNode.createIntParam("duration_percent", "Duration Percent %")
    param.setMinimum(25, 0)
    param.setMaximum(100, 0)
    param.setDisplayMinimum(25, 0)
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
    param.setEnabled(False, 0)
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

    param = lastNode.createChoiceParam("sequence_type", "Sequence Type")
    entries = [ ("PNG", ""),
    ("JPG", "")]
    param.setOptions(entries)
    del entries

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.sequence_type = param
    del param

    param = lastNode.createChoiceParam("filter", "Reformat Filter")
    entries = [ ("Cubic", ""),
    ("Impulse", ""),
    ("Notch", "")]
    param.setOptions(entries)
    del entries

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    lastNode.filter = param
    del param

    param = lastNode.createStringParam("prefix", "Prefix")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeDefault)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.prefix = param
    del param

    param = lastNode.createBooleanParam("current_state", "Current State")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    lastNode.current_state = param
    del param

    param = lastNode.createBooleanParam("current_speed", "Current Speed")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("Renderiza solo una velocidad con los 3 formatos.")
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    lastNode.current_speed = param
    del param

    param = lastNode.createButtonParam("render", "Render")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(False)
    param.setEvaluateOnChange(False)
    lastNode.render = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode
    # End of node "TwelveRender1"

    # Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, grouplimit)
    groupKeyMix3.connectInput(0, groupDot1)
    groupKeyMix3.connectInput(1, grouptransform_b)
    groupKeyMix3.connectInput(2, groupnoise_blur)
    groupnoise_keyer.connectInput(0, groupnoise)
    groupnoise_blur.connectInput(0, groupnoise_keyer)
    groupduplicate_a.connectInput(0, groupDot3)
    groupduplicate_b.connectInput(0, groupDot4)
    groupMerge1.connectInput(0, groupDot3)
    groupMerge1.connectInput(1, groupduplicate_a)
    groupDot3.connectInput(0, groupA)
    groupDot4.connectInput(0, groupB)
    groupMerge2.connectInput(0, groupDot4)
    groupMerge2.connectInput(1, groupduplicate_b)
    grouptransform_a.connectInput(0, groupMerge1)
    grouptransform_b.connectInput(0, groupMerge2)
    groupDot1.connectInput(0, grouptransform_a)
    grouplimit.connectInput(0, groupA)
    grouplimit.connectInput(1, groupKeyMix3)
    grouplimit.connectInput(2, groupB)
    groupTwelveRender1.connectInput(0, groupnoise_blur)

    param = groupnoise.getParam("fbmLacunarity")
    param.slaveTo(group.getParam("lacunarity"), 0, 0)
    del param
    param = groupTwelveRender1.getParam("state_label")
    group.getParam("state_label").setAsAlias(param)
    del param
    param = groupTwelveRender1.getParam("format")
    group.getParam("format").setAsAlias(param)
    del param
    param = groupTwelveRender1.getParam("speed")
    group.getParam("speed").setAsAlias(param)
    del param
    param = groupTwelveRender1.getParam("sep5")
    group.getParam("sep5").setAsAlias(param)
    del param
    param = groupTwelveRender1.getParam("duration_percent")
    group.getParam("duration_percent").setAsAlias(param)
    del param
    param = groupTwelveRender1.getParam("durations")
    group.getParam("durations").setAsAlias(param)
    del param
    param = groupTwelveRender1.getParam("sep6")
    group.getParam("sep6").setAsAlias(param)
    del param

    try:
        extModule = sys.modules["NoiserTransitionExt"]
    except KeyError:
        extModule = None
    if extModule is not None and hasattr(extModule ,"createInstanceExt") and hasattr(extModule.createInstanceExt,"__call__"):
        extModule.createInstanceExt(app,group)
