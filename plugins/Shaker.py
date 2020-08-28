# -*- coding: utf-8 -*-
# DO NOT EDIT THIS FILE
# Natron PyPlug
# This file was automatically generated by Natron PyPlug exporter version 10.

# Hand-written code should be added in a separate file named ShakerExt.py
# See http://natron.readthedocs.org/en/master/devel/groups.html#adding-hand-written-code-callbacks-etc
# Note that Viewers are never exported

import NatronEngine
import sys

# Try to import the extensions file where callbacks and hand-written code should be located.
try:
    from ShakerExt import *
except ImportError:
    pass

def getPluginID():
    return "vv.Shaker"

def getLabel():
    return "Shaker"

def getVersion():
    return 1

def getIconPath():
    return "Shaker.png"

def getGrouping():
    return "videovina/Transform"

def createInstance(app,group):
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    lastNode.setColor(0.7, 0.7, 0.7)
    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("base.main")
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

    param = lastNode.createSeparatorParam("sep5", "")

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
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

    param = lastNode.createDoubleParam("translate", "Translate")
    param.setMinimum(0, 0)
    param.setMaximum(1000, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(1000, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(50, 0)
    lastNode.translate = param
    del param

    param = lastNode.createDoubleParam("rotate", "Rotate")
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
    param.setValue(2, 0)
    lastNode.rotate = param
    del param

    param = lastNode.createDoubleParam("scale", "Scale")
    param.setMinimum(0, 0)
    param.setMaximum(2147483647, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(5, 0)

    # Add the param to the page
    lastNode.control.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.scale = param
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

    param = lastNode.createDoubleParam("frequency", "Frequency")
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
    param.setValue(50, 0)
    lastNode.frequency = param
    del param

    lastNode.exp = lastNode.createPageParam("exp", "Exp")
    param = lastNode.createInt2DParam("current_format", "Current Format")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)
    param.setDisplayMinimum(0, 1)
    param.setDisplayMaximum(100, 1)
    param.setDefaultValue(0, 1)
    param.restoreDefaultValue(1)

    # Add the param to the page
    lastNode.exp.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(1920, 0)
    param.setValue(1080, 1)
    lastNode.current_format = param
    del param

    param = lastNode.createIntParam("duration", "Current Duration")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(0, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.exp.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(100, 0)
    lastNode.duration = param
    del param

    param = lastNode.createDoubleParam("rscale", "Rscale")
    param.setMinimum(-2147483648, 0)
    param.setMaximum(2147483647, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)

    # Add the param to the page
    lastNode.exp.addParam(param)

    # Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    param.setValue(1, 0)
    lastNode.rscale = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['control', 'exp', 'Node', 'Settings'])
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

    # Start of node "Input1"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Input1")
    lastNode.setLabel("Input1")
    lastNode.setPosition(767, 154)
    lastNode.setSize(104, 30)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupInput1 = lastNode

    del lastNode
    # End of node "Input1"

    # Start of node "Transform"
    lastNode = app.createNode("net.sf.openfx.TransformPlugin", 1, group)
    lastNode.setScriptName("Transform")
    lastNode.setLabel("Transform")
    lastNode.setPosition(767, 221)
    lastNode.setSize(104, 32)
    lastNode.setColor(0.7, 0.3, 0.1)
    groupTransform = lastNode

    param = lastNode.getParam("translate")
    if param is not None:
        param.setValue(-9.273945201799439, 0)
        param.setValue(4.988368024089517, 1)
        del param

    param = lastNode.getParam("rotate")
    if param is not None:
        param.setValue(-0.6314643113169951, 0)
        del param

    param = lastNode.getParam("scale")
    if param is not None:
        param.setValue(1, 0)
        param.setValue(1, 1)
        del param

    param = lastNode.getParam("center")
    if param is not None:
        param.setValue(960, 0)
        param.setValue(540, 1)
        del param

    param = lastNode.getParam("transformCenterChanged")
    if param is not None:
        param.setValue(True)
        del param

    del lastNode
    # End of node "Transform"

    # Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, groupTransform)
    groupTransform.connectInput(0, groupInput1)

    param = groupTransform.getParam("translate")
    param.setExpression("import random\n\nfrequency = thisGroup.frequency.get()\ndurations = thisGroup.durations.get()\nspeed = thisGroup.speed.get()\nfrequency = vina.value_by_durations(frequency, durations, True)[speed]\n\namplitude = thisGroup.translate.curve(frame) * thisGroup.rscale.get()\ncomplexity = 10\nseed = 10 + dimension * 10\nfps = 24\n\nvalue = 0\n\n# Wiggle Expression\nfor x in range( 1 , complexity):\n\trandom.seed(seed)\n\toffset = random.randint(1,1000)\n\tt = (offset + float( frame )) / fps\n\tfactor = 0.8 ** x\n\tvalue += sin( t * factor * frequency ) * amplitude / complexity\nret = value", True, 0)
    param.setExpression("import random\n\nfrequency = thisGroup.frequency.get()\ndurations = thisGroup.durations.get()\nspeed = thisGroup.speed.get()\nfrequency = vina.value_by_durations(frequency, durations, True)[speed]\n\namplitude = thisGroup.translate.curve(frame) * thisGroup.rscale.get()\ncomplexity = 10\nseed = 10 + dimension * 10\nfps = 24\n\nvalue = 0\n\n# Wiggle Expression\nfor x in range( 1 , complexity):\n\trandom.seed(seed)\n\toffset = random.randint(1,1000)\n\tt = (offset + float( frame )) / fps\n\tfactor = 0.8 ** x\n\tvalue += sin( t * factor * frequency ) * amplitude / complexity\nret = value", True, 1)
    del param
    param = groupTransform.getParam("rotate")
    param.setExpression("import random\n\nfrequency = thisGroup.frequency.get()\ndurations = thisGroup.durations.get()\nspeed = thisGroup.speed.get()\nfrequency = vina.value_by_durations(frequency, durations, True)[speed]\n\namplitude = thisGroup.rotate.curve(frame) * thisGroup.rscale.get()\ncomplexity = 10\nseed = 50\nfps = 24\n\nvalue = 0\n\n# Wiggle Expression\nfor x in range( 1 , complexity):\n\trandom.seed(seed)\n\toffset = random.randint(1,1000)\n\tt = (offset + float( frame )) / fps\n\tfactor = 0.8 ** x\n\tvalue += sin( t * factor * frequency ) * amplitude / complexity\nret = value", True, 0)
    del param
    param = groupTransform.getParam("scale")
    param.setExpression("import random\n\nfrequency = thisGroup.frequency.get()\ndurations = thisGroup.durations.get()\nspeed = thisGroup.speed.get()\nfrequency = vina.value_by_durations(frequency, durations, True)[speed]\n\namplitude = thisGroup.scale.curve(frame) * thisGroup.rscale.get()\ncomplexity = 10\nseed = 200\nfps = 24\n\nvalue = 0\n\n# Wiggle Expression\nfor x in range( 1 , complexity):\n\trandom.seed(seed)\n\toffset = random.randint(1,1000)\n\tt = (offset + float( frame )) / fps\n\tfactor = 0.8 ** x\n\tvalue += sin( t * factor * frequency ) * amplitude / complexity\nret = value + 1", True, 0)
    param.setExpression("import random\n\nfrequency = thisGroup.frequency.get()\ndurations = thisGroup.durations.get()\nspeed = thisGroup.speed.get()\nfrequency = vina.value_by_durations(frequency, durations, True)[speed]\n\namplitude = thisGroup.scale.curve(frame) * thisGroup.rscale.get()\ncomplexity = 10\nseed = 200\nfps = 24\n\nvalue = 0\n\n# Wiggle Expression\nfor x in range( 1 , complexity):\n\trandom.seed(seed)\n\toffset = random.randint(1,1000)\n\tt = (offset + float( frame )) / fps\n\tfactor = 0.8 ** x\n\tvalue += sin( t * factor * frequency ) * amplitude / complexity\nret = value + 1", True, 1)
    del param
    param = groupTransform.getParam("center")
    param.setExpression("thisGroup.current_format.get()[dimension] / 2", False, 0)
    param.setExpression("thisGroup.current_format.get()[dimension] / 2", False, 1)
    del param

    param = group.getParam("current_format")
    param.setExpression("index = thisNode.format.get()\nret = general.formats[index][dimension]", True, 0)
    param.setExpression("index = thisNode.format.get()\nret = general.formats[index][dimension]", True, 1)
    del param
    param = group.getParam("duration")
    param.setExpression("index = thisNode.speed.get()\nret = thisNode.durations.get()[index]", True, 0)
    del param
    param = group.getParam("rscale")
    param.setExpression("index = thisNode.format.get()\nret = general.rscale[index]", True, 0)
    del param
    try:
        extModule = sys.modules["ShakerExt"]
    except KeyError:
        extModule = None
    if extModule is not None and hasattr(extModule ,"createInstanceExt") and hasattr(extModule.createInstanceExt,"__call__"):
        extModule.createInstanceExt(app,group)