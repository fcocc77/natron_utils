import random
from transition import directional_transition


def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        distribute(thisNode)


def distribute(thisNode):

    # parametros del grupo
    repetitions = thisNode.repetitions.get()
    gap = thisNode.gap.get()
    start_frame = thisNode.start_frame.get()
    duration = thisNode.duration.get()
    initial_translate = thisNode.initial_translate.get()
    end_translate = thisNode.end_translate.get()
    initial_rotate = thisNode.initial_rotate.get()
    initial_width = thisNode.initial_width.get()
    direction = thisNode.direction.get()
    sort = thisNode.sort.get()
    seed = thisNode.seed.get()
    # ------------------------

    # obtiene el desfase correcto dependiendo de la duracion
    gap = (duration * float(gap)) / 100
    # -----------------------

    # modifica la duracion quitandole la cola que queda a causa del desfase
    tail_duration = repetitions * gap
    duration -= tail_duration
    # ----------------------

    # le quita a la duracion el desface del stencil self
    if thisNode.getParam('stencil_self').get():
        stencil_gap = thisNode.getParam('stencil_self_gap').get()
        stencil_gap = (duration * float(stencil_gap)) / 50
        duration -= stencil_gap
    # ------------------

    width = thisNode.format.boxSize.getValue(0)
    hight = thisNode.format.boxSize.getValue(1)

    # ajusta la direccion de la forma
    rotate = thisNode.getNode('direction_transform').getParam('rotate')
    center = thisNode.getNode('direction_transform').getParam('center')
    center.set(width / 2, width / 2)

    if direction == 0:
        rotate.setValue(180)
    elif direction == 1:
        rotate.setValue(0)
    elif direction == 2:
        rotate.setValue(90)
    elif direction == 3:
        rotate.setValue(-90)
    # ---------------------------

    # adapta algunos de los valores a la resolucion correspondiente, tomando como base 1920x1080
    end_translate = (width * end_translate) / 1920
    initial_translate = (width * initial_translate) / 1920
    # ------------------------

    new_width = width + end_translate

    if thisNode.getParam('lineal_animation').get():
        exaggeration_time = 0
        exaggeration_value = 0
    else:
        exaggeration_time = 0.7
        exaggeration_value = 0.7

    part = new_width / repetitions
    left_translate = -end_translate

    rotate_src = initial_rotate
    rotate_dst = 0

    max_width = new_width / repetitions

    total_gap = 0

    for i in range(2, 8):
        thisNode.getNode('merge_' + str(i)).getParam('mix').set(0)

    for i in range(1, repetitions + 1):
        width_translate = thisNode.getNode(
            'shape_width_' + str(i)).getParam('translate')

        transform = thisNode.getNode('transform_' + str(i))
        rotate = transform.getParam('rotate')
        translate = transform.getParam('translate')
        center = transform.getParam('center')

        center.set(new_width - (max_width / 2), width / 2)
        thisNode.getNode('merge_' + str(i)).getParam('mix').set(1)
        _start_frame = start_frame + total_gap

        directional_transition(rotate, duration, exaggeration_time,
                               exaggeration_value, _start_frame, [rotate_src, rotate_dst])

        position_dst = -left_translate
        position_src = position_dst - initial_translate
        directional_transition(translate, duration, exaggeration_time,
                               exaggeration_value, _start_frame, [position_src, position_dst])

        if sort == 1:  # Formas ordenadas
            width_src = -initial_width
            width_dst = -(part + 1)
            directional_transition(width_translate, duration, exaggeration_time,
                                   exaggeration_value, _start_frame, [width_src, width_dst])
        else:  # Formas Random
            random.seed(seed + 100 * i)
            width_src = -random.randint(0, new_width / 5)
            random.seed(seed + 1000 * i)
            width_dst = -random.randint(0, new_width / 5)

            directional_transition(width_translate, duration, exaggeration_time,
                                   exaggeration_value, _start_frame, [width_src, width_dst])

        total_gap += gap
        left_translate += part
