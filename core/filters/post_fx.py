from base import link_to_parent, children_refresh
import os
from nx import getNode


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)
    elif knob_name == 'reload_assets':
        reload_assets(thisNode)


def refresh(thisNode):
    files_refresh(thisNode, 'film')
    files_refresh(thisNode, 'flare')


def get_current_choice(choice_param):
    index = choice_param.getValue()
    option = choice_param.getOption(index)

    return option.split('- ')[-1].replace(' ', '_').lower()


def set_choice_list(choice_param, list):
    items = []
    for i, item_name in enumerate(list):
        name = str(i + 1) + ' - ' + item_name.replace('_', ' ').capitalize()
        items.append((name, item_name))

    choice_param.setOptions(items)


def reload_assets(thisNode):
    assets_folder = thisNode.getParam('assets_folder').get()
    flares_folder = assets_folder + '/flares'
    textures_folder = assets_folder + '/textures'
    films_folder = assets_folder + '/films'

    flare_choice = thisNode.getParam('flare')
    films_choice = thisNode.getParam('film')

    set_choice_list(flare_choice, os.listdir(flares_folder))
    set_choice_list(films_choice, os.listdir(films_folder))


def files_refresh(thisNode, param_name):
    folder = thisNode.getParam('assets_folder').get() + '/' + param_name + 's'

    file_node = getNode(thisNode, param_name + '_file')
    filename = file_node.getParam('filename')

    name = get_current_choice(thisNode.getParam(param_name))

    file_path = folder + '/' + name + '/' + name + '_####.jpg'
    filename.set(file_path)
