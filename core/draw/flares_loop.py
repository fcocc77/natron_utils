from base import link_to_parent, children_refresh, get_rscale, get_duration, get_format
from nx import getNode, reload_read, get_current_choice, set_choice_list
import os
from animations import back_and_forth_animation


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)
    if knob_name == 'reload_flares':
        reload_flares(thisNode)


def reload_flares(thisNode):
    folder = thisNode.flares_folder.get()
    set_choice_list(thisNode.flares, os.listdir(folder))


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    width, height = get_format(thisNode)

    # Read
    read = getNode(thisNode, 'read')
    filename = read.getParam('filename')

    folder = thisNode.flares_folder.get()
    flare_name = get_current_choice(thisNode.flares)
    flare_path = folder + '/' + flare_name + '/' + flare_name + '_####.jpg'

    filename.set(flare_path)
    read.getParam('before').set(1)
    read.getParam('after').set(1)
    reload_read(read)
    file_last_frame = read.getParam('lastFrame').get()
    #
    #

    # Reformat
    scale = getNode(thisNode, 'transform').getParam('scale')
    rscale *= 2
    scale.set(rscale, rscale)
    #
