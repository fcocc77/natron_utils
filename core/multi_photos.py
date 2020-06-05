from natron_utils import createNode, getNode
import os
import random

vertical = 5
horizontal = 5

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'generate':
        create(thisNode, app)
    if knob_name == 'update':
        update(thisNode)

def get_pair_indexs(vertical, horizontal, amount):
    # obtiene una lista de pares de index verticalmente

    _min = 0
    _max = vertical - 1

    pairs = []

    # deja una lista desordenada
    def random_sin_repetir(lista):
        for _ in range(0,len(lista)):
            result = random.choice(lista)
            yield result
            lista.remove(result)
    # --------------------

    for i in range(horizontal):
        rand = random.randint(_min, _max)

        index1 = rand
        index2 = rand + 1
        
        if index2 > _max:
            rand = random.randint(_min, _max)
            index1 = rand
            index2 = rand + 1
            if index2 > _max:
                index1 -= 1
                index2 -= 1

        pairs.append( [index1, index2] ) 

        _min += vertical
        _max += vertical

    # crea una lista nueva con la cantidad entrante, aleatoriamente
    _pairs = []
    for i, pair in enumerate(random_sin_repetir(pairs)):
        if i >= amount:
            break
        _pairs.append(pair)
    # ------------------

    return _pairs

def get_four_indexs(vertical, horizontal, amount):

    four = get_pair_indexs(vertical, horizontal, 1)[0]
    
    four.append(four[0] + vertical)
    four.append(four[0] + vertical + 1)

    return [four]

def get_items(thisNode):
    items = []
    for i in range(200):
        reader = getNode(thisNode, 'reader_' + str(i))
        transform = getNode(thisNode, 'transform_' + str(i))

        if not reader:
            break
        item = {
            'reader': reader,
            'transform': transform
        }
        items.append(item)

    return items

def update(thisNode):

    hide = get_four_indexs(vertical, horizontal, 2)
    scale = 1.0 / horizontal
    
    for i, item in enumerate(get_items(thisNode)):
        scale_param = item['transform'].getParam('scale')

        scale_param.set(scale, scale)

        for pair in hide:
            if i in pair:
                scale_param.set(0, 0)
            
            # sube la escala al primer item 
            if i == pair[0]:
                new_scale = scale * 2
                scale_param.set(new_scale, new_scale)
            
            # --------------

def create(thisNode, app):
    videos_folder = thisNode.videos_dir.get()
    videos = os.listdir(videos_folder)

    merge = createNode('merge', 'merge', thisNode, position=[0, 300])

    margin = 10
    scale = 1.0 / horizontal
    left_pos = 1920 / horizontal
    up_pos = 1080 * scale

    posx = 0

    left = 0
    conections = 3
    video_index = 0
    for l in range(horizontal):
        
        up = 0
        for u in range(vertical):
            index = str(video_index)

            picture = videos_folder + '/' + videos[video_index]
            reader = app.createReader( picture, thisNode )
            reader.setPosition(posx, -300)
            reader.setLabel('reader_' + index)

            # para ajustar el reformat
            _width = reader.getOutputFormat().width()
            _height = reader.getOutputFormat().height()
            aspect = 1920.0 / 1080.0 # aspecto de referencia
            aspect_input = float(_width) / float(_height)
            # -------------

            reformat = createNode('reformat', 'reformat_' + index, thisNode, position=[posx, -150])
            reformat.getParam('reformatType').set(1)
            reformat.getParam('boxFixed').set(1)
            reformat.getParam('boxSize').set(1920, 1080)

            if aspect <= aspect_input:
                reformat.getParam('resize').set(2)
            reformat.connectInput(0, reader)

            transform = createNode('transform', 'transform_' + index, thisNode, position=[posx, 0])
            transform.getParam('scale').set(scale, scale)
            transform.getParam('center').set(0,0)

            transform.getParam('translate').set(left, up)
            transform.connectInput(0, reformat)
            
            conections += 1
            merge.connectInput(conections, transform)
            
            up += up_pos
            posx += 200
            video_index += 1

        left += left_pos
        
