from natron_extent import copy, warning, alert
from slides import get_slides, delete_slide, get_slide
from develop import update_post_fx, xdistance, generate_random_pictures, refresh


def divide_project(thisNode, workarea):
    # divide el proyecto en varias partes, asi evitamos que cuando renderizamos
    # cargue todas las slides, ya que natron
    # se demora mucho al abrir los proyectos pesados

    slide_range = [2, 5]

    keep_slides = range(slide_range[0], slide_range[-1] + 1)
    for i, slide in enumerate(get_slides(workarea)):

        if not i in keep_slides:
            delete_slide(workarea, i)

    update_post_fx(thisNode, workarea)


def production_slides(thisNode, app, workarea):
    amount = thisNode.production_slides.get()

    generated = generate_production_slides(thisNode, app, workarea, amount)
    if not generated:
        return

    update_post_fx(thisNode, workarea)
    generate_random_pictures(thisNode, app, workarea, amount)
    refresh(thisNode, app, workarea)

    alert('Ya se duplicaron las slide de Produccion.',
          'Duplicate from base slides.')


def generate_production_slides(thisNode, app, workarea, amount, force=False, reformat=True):
    # duplica los slides base, dependiendo de la
    # cantidad de fotos que importemos.
    base_amount = thisNode.amount_slide.get()

    base_slides, production_slides = get_slides(workarea, separate=True)
    base_count = len(base_slides)
    slides_count = base_count + len(production_slides)

    if not force:
        if not slides_count:
            warning(
                'Production Slides', 'No hay ninguna slide base creada.')
            return False

        if amount <= base_amount:
            warning(
                'Production Slides', 'La Cantidad de slides tiene que ser mayor que los slides base.')
            return False

        if amount == slides_count:
            warning(
                'Production Slides', 'Ya existen ' + str(amount) + ' slides.')
            return False

    count_delete_slide = None
    if amount <= slides_count:
        count_delete_slide = slides_count - amount
        if not force:
            message = 'La cantidad de slides es menor a la existente, se eliminaran ' + \
                str(count_delete_slide) + ' slides.'
            ok = question('Estas seguro de que quieres continuar ?', message)
            if not ok:
                return False

    if count_delete_slide:
        # borra las slides que sobran
        _range = range(slides_count - count_delete_slide, slides_count)
        delete_slide(workarea, _range)
    else:
        last_transition = None
        last_dot = None

        slide_obj = get_slide(workarea, slides_count - 1)
        last_base_transition = slide_obj['transition']
        last_base_dot = slide_obj['dot']

        current = 0
        posx = (xdistance * slides_count) + xdistance
        for i in range(amount - slides_count):
            index = i + slides_count

            slide = base_slides[current]['slide']
            transition = base_slides[current]['transition']

            if reformat:
                _reformat = base_slides[current]['reformat']

                new_reformat = copy(_reformat, workarea)
                new_reformat.setColor(.4, .5, .7)
                new_reformat.setPosition(posx, -200)
                new_reformat.setLabel('slide_' + str(index) + 'p_reformat')

            new_slide = copy(slide, workarea)
            new_slide.setPosition(posx, 0)
            new_slide.setLabel('slide_' + str(index) + 'p')
            if reformat:
                new_slide.connectInput(0, new_reformat)

            new_transition = copy(transition, workarea)
            new_transition.setColor(.7, .7, .4)
            new_transition.setPosition(posx, 200)
            new_transition.setLabel('slide_' + str(index) + 'p_transition')
            if last_transition:
                new_transition.connectInput(0, last_transition)
            else:
                new_transition.connectInput(0, last_base_transition)

            new_transition.connectInput(1, new_slide)

            dot = app.createNode('fr.inria.built-in.Dot', 2, workarea)
            dot_name = 'slide_' + str(index) + 'p_dot'
            dot.setLabel(dot_name)
            dot.setPosition(posx - 50, 100)

            if last_dot:
                dot.connectInput(0, last_dot)
            else:
                dot.connectInput(0, last_base_dot)

            new_transition.connectInput(2, dot)

            last_transition = new_transition
            last_dot = dot

            current += 1
            if current >= base_count:
                current = 0

            posx += xdistance

    return True
