from nx import set_option


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'MergeMatteMainchannels':
        change_channels(thisNode)


def change_channels(thisNode):

    mask_merge = thisNode.MergeMatteMain

    channels = mask_merge.channels
    channel_index = channels.getValue()
    channel_option = channels.getOption(channel_index)

    set_option(mask_merge.B_channels, channel_option)

    stencil_matte = thisNode.stencil_matte
    set_option(stencil_matte.channels, channel_option)
    set_option(stencil_matte.B_channels, channel_option)

    over_matte = thisNode.over_matte
    set_option(over_matte.channels, channel_option)
    set_option(over_matte.B_channels, channel_option)

    shuffle_matte = thisNode.shuffle_matte
    set_option(shuffle_matte.outputR, 'B.' + channel_option + '.R')
    set_option(shuffle_matte.outputA, 'B.' + channel_option + '.R')
