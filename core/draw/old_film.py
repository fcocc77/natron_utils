from base import link_to_parent, children_refresh, get_rscale, get_format
from nx import getNode, reload_read,  get_current_choice, set_choice_list
import os


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)
    if knob_name == 'reload_films':
        reload_films(thisNode)


def reload_films(thisNode):
    folder = thisNode.films_folder.get()
    set_choice_list(thisNode.films, os.listdir(folder))


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    width, height = get_format(thisNode)

    # Read
    read = getNode(thisNode, 'read')
    filename = read.getParam('filename')

    folder = thisNode.films_folder.get()
    film_name = get_current_choice(thisNode.films)
    film_path = folder + '/' + film_name + '/' + film_name + '_####.jpg'

    filename.set(film_path)
    read.getParam('before').set(1)
    read.getParam('after').set(1)
    reload_read(read)
    file_last_frame = read.getParam('lastFrame').get()
    #
    #

    # Reformat
    scale = getNode(thisNode, 'transform').getParam('scale')
    scale.set(rscale, rscale)
    #
