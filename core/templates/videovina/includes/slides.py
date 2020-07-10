from natron_extent import getNode


def get_slide(workarea, index):
    _index = str(index)

    slide = getNode(workarea, 'slide_' + _index)
    transition = getNode(workarea, 'slide_' + _index + '_transition')
    dot = getNode(workarea, 'slide_' + _index + '_dot')

    production = False
    # si no no existe la slide base, busca la slide de produccion, si
    # es que all=True
    if not slide:
        slide = getNode(workarea, 'slide_' + _index + 'p')
        transition = getNode(workarea, 'slide_' + _index + 'p_transition')
        dot = getNode(workarea, 'slide_' + _index + 'p_dot')

        production = True
    # --------------------

    if not slide:
        return None

    return {
        'production': production,
        'slide': slide,
        'transition': transition,
        'dot': dot,
        'index': index
    }


def get_slides(workarea, production=True, base=True, separate=False):
    # si 'all' es False obtiene solo las slide de base
    production_list = []
    base_list = []
    all_list = []

    for i in range(100):
        obj = get_slide(workarea, i)
        if obj:
            all_list.append(obj)
            if obj['production']:
                production_list.append(obj)
            else:
                base_list.append(obj)

    if separate:
        return [base_list, production_list]
    elif production and base:
        return all_list
    elif production:
        return production_list
    elif base:
        return base_list


def get_last_slide(workarea):
    return get_slides(workarea)[-1]


def get_first_slide(workarea):
    return get_slides(workarea)[0]


def delete_slide(workarea, slide_number):
    # se usa .destroy() 2 veces ya que a veces
    # natron no borra el nodo
    def remove(index):
        obj = get_slide(workarea, index)
        if obj:
            for key, node in obj.iteritems():
                if node:
                    if not type(node) == bool and not type(node) == int:
                        node.destroy()

    if type(slide_number) is list:
        for i in slide_number:
            remove(i)
        for i in slide_number:
            remove(i)
    else:
        remove(slide_number)
        remove(slide_number)


def get_slide_position(index):
    return [200 * index, 0]
