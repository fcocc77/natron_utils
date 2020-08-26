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
    elif knob_name == 'film_isolate':
        isolate(thisNode, 'film')
    elif knob_name == 'flare_isolate':
        isolate(thisNode, 'flare')
    elif knob_name == 'texture_isolate':
        isolate(thisNode, 'texture')


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
    filename.reloadFile()
    filename.reloadFile()

    file_node.getParam('after').set(1)
    file_node.getParam('before').set(1)


def isolate(thisNode, name):
    display = getNode(thisNode, 'display').getParam('which')

    if name == 'film':
        display.set(1)
    elif name == 'flare':
        display.set(2)
    elif name == 'texture':
        display.set(3)

    for _name in ['film', 'flare', 'texture']:
        param = thisNode.getParam(_name + '_isolate')

        if _name == name:
            if param.get() == 0:
                param.set(0)
                display.set(0)
            else:
                param.set(1)
        else:
            param.set(0)
