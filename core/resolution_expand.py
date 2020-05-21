def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        width = thisNode.boxSize.getValue(0)
        height = thisNode.boxSize.getValue(1)

        blur = thisNode.blur.getValue()

        thisNode.Blur1.size.set(blur, blur)

        thisNode.Reformat2.boxSize.set(1920 / 7, 1080 / 7)
        thisNode.Reformat3.boxSize.set(width, height)
        thisNode.Reformat4.boxSize.set(width, height)
        thisNode.Reformat5.boxSize.set(width, height)

        # si la imagen es vertical cambia el switch a los reformat correspondientes
        add_alpha = thisNode.add_alpha

        _width = add_alpha.getOutputFormat().width()
        _height = add_alpha.getOutputFormat().height()

        switch = thisNode.Switch1.which
        vertical = _width < _height

        aspect = 1920.0 / 1080.0 # aspecto de referencia
        aspect_input = float(_width) / float(_height)

        if vertical:
            switch.set(1)
        else:
            if aspect >= aspect_input:
                switch.set(0)
            else:
                switch.set(2)
        # ------------------------