from natron_utils import createNode, getNode
from util import jread
import os
import random
import wave
import NatronEngine
import json

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'video_import':
        import_videos(thisNode, app)
    if knob_name == 'refresh':
        refresh(thisNode)     
    if knob_name == 'mosaic_a':
        create_mosaic_a(thisNode)
    if knob_name == 'add_subtitles':
        add_subtitles(thisNode)

def refresh(thisNode):

    cuts_create(thisNode)

    for mosaic in get_all_mosaics(thisNode):
        for item in mosaic:
            crop = item['crop']
            userTextArea = str(crop.getParam('userTextArea').get())

            if userTextArea != '0':
                crop_data = userTextArea.replace('"', '').split(',')

                squared_videos = int(crop_data[0])
                mid = int(crop_data[1])
                double = int(crop_data[2])

                margin(thisNode, crop, mid=mid, double=double, squared_videos=squared_videos)

def add_subtitles(thisNode):

    subtitles_json = thisNode.getParam('subtitles').get()
    subtitles = jread(subtitles_json)

    posx = 200
    posy = 2200

    merge_all = createNode('merge', 'subtitles_merge_all', thisNode, position=[posx, posy + 200])
    merge = createNode('merge', 'subtitles_merge', thisNode, position=[0, posy + 200])

    global_merge = getNode(thisNode, 'global_merge')

    merge.connectInput(1, merge_all)
    merge.connectInput(0, global_merge)

    for i, text in enumerate(subtitles):

        title = createNode('text', 'title_' + str(i), thisNode, position=[posx, posy])
        title.getParam('text').set(text.title)

        subtitle = createNode('text', 'subtitle_' + str(i), thisNode, position=[posx, posy + 70])
        subtitle.connectInput(0, title)
        subtitle.getParam('text').set(text.subtitle)

        merge_all.connectInput(i + 3, subtitle)

        posx += 200

def audio_sync(thisNode):

    audio1 = jread('/home/pancho/Desktop/video_audio2.json')
    audio2 = jread('/home/pancho/Desktop/part.json')

    comps = []

    start = 0
    end = len(audio2)

    for frame in range(0, len(audio1) - end):
        comp = 0
        for i in range(0, end):
            value1 = audio2[i]
            try:
                value2 = audio1[i + frame]
            except:
                break

            comp += abs(value1-value2)

        comps.append([comp, frame])

    comps = sorted(comps)
    if len(comps):
        offset = comps[0][1]
    else:
        offset= 0

    curve = thisNode.getParam('curve')
    curve.restoreDefaultValue(0)
    curve.restoreDefaultValue(1)

    for frame, value in enumerate(audio1):
        curve.setValueAtTime(value, frame, 0)

    for frame, value in enumerate(audio2):
        curve.setValueAtTime(value, frame + offset , 1)
        
def get_pair_indexs(vertical, horizontal, amount, skip = []):
    # obtiene una lista de pares de index verticalmente

    _min = 0
    _max = vertical - 1

    pairs = []

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

        if not index1 in skip and not index2 in skip:
            pairs.append( [index1, index2] ) 

        _min += vertical
        _max += vertical

    pairs_no_repeat = random.sample( pairs, len(pairs) )

    # crea una lista nueva con la cantidad entrante, aleatoriamente
    _pairs = []
    for i, pair in enumerate(pairs_no_repeat):
        if i >= amount:
            break
        _pairs.append(pair)
    # ------------------

    return _pairs

def get_four_indexs(vertical, horizontal):

    total_images = vertical * horizontal
    index_4 = 1000
    while(index_4 >= total_images):
        
        four = get_pair_indexs(vertical, horizontal, 1)[0]

        index_3 = four[0] + vertical
        index_4 = four[0] + vertical + 1

    four.append(index_3)
    four.append(index_4)

    return four

def get_items(thisNode):
    items = []
    for i in range(200):
        reader = getNode(thisNode, 'reader_' + str(i))
        reformat = getNode(thisNode, 'reformat_' + str(i))

        if not reader:
            break
        item = {
            'reader': reader,
            'reformat': reformat
        }
        items.append(item)

    return items

def margin(thisNode, crop, mid = False, double = False, squared_videos = False):
    if not squared_videos:
        squared_videos = thisNode.getParam('squared_videos').get()
    margin = thisNode.getParam('margin').get()
    if double:
        margin /= 2

    if squared_videos == 3:
        margin = margin + (margin / 2)
    elif squared_videos == 4:
        margin *= 2 
    elif squared_videos == 5:
        margin = (margin * 2) + (margin / 2)       
    elif squared_videos == 6:
        margin *= 3      

    size = crop.getParam('size')
    bottom_left = crop.getParam('bottomLeft')

    if mid:
        mid_x = 1920 / 2
        mid_x_left = 1920 / 4 + margin
    else:
        mid_x = 1920 
        mid_x_left = margin

    margin_rigth = mid_x - (margin * 2) 
    margin_bottom = 1080 - (margin * 2) 

    size.set(margin_rigth, margin_bottom)
    bottom_left.set(mid_x_left , margin)

def add_transition(thisNode, mosaic_index, start_frame, out=False):
    mosaic = get_all_mosaics(thisNode)[mosaic_index]

    horizontal = NatronEngine.Natron.KeyframeTypeEnum.eKeyframeTypeHorizontal
    
    random_difference = thisNode.getParam('random_difference').get()
    duration = thisNode.getParam('transition_frames').get()

    def add(param, _from, _to, start):
        for dimension in range( param.getNumDimensions() ):
            param.setValueAtTime(_from, start, dimension)
            param.setInterpolationAtTime(start,  horizontal, dimension)

            param.setValueAtTime(_to, start + duration, dimension)
            param.setInterpolationAtTime(start + duration,  horizontal, dimension)

    for item in mosaic:
        which = item['dissolve'].getParam('which')
        blur = item['blur'].getParam('size')
        
        start = start_frame + random.randint(start_frame, start_frame + random_difference )

        if out:
            add(which, 1, 0, start)
            add(blur, 0, 100, start)
        else:
            add(which, 0, 1, start)
            add(blur, 100, 0, start)

def cuts_create(thisNode):

    # encuentra todos los merges de los mosaicos
    merges = []
    for index in range(100):
        name = 'merge_' + str(index)
        merge = getNode(thisNode, name)
        if merge:
            merges.append(merge)
    # -------------------------

    total_frames = 250

    global_merge = getNode(thisNode, 'global_merge')
    if not global_merge:
        global_merge = createNode('merge', 'global_merge', thisNode, position=[0, 2000])

    for i, merge in enumerate(merges):
        global_merge.disconnectInput(i + 3)
        global_merge.connectInput(i + 3, merge)

    time_range = thisNode.getParam('time_range').get()
    transition_separation = thisNode.getParam('transition_separation').get()
    cut_frame = 0
    connections_random = random.sample(range(len(merges)), len(merges)) # rango random sin repetir

    def reset_all_transition():
        for mosaic in get_all_mosaics(thisNode):
            for item in mosaic:
                which = item['dissolve'].getParam('which')
                which.restoreDefaultValue(0)

                blur = item['blur'].getParam('size')
                blur.restoreDefaultValue(0)
                blur.restoreDefaultValue(1)

    reset_all_transition()

    last_connection = 0
    i = 0
    for frame in range(total_frames):
        if cut_frame == frame:
            if i >= len(connections_random):
                i = 0

            connection = connections_random[i]

            if cut_frame > 0:
                add_transition(thisNode, last_connection, frame - transition_separation  , out=True)

            add_transition(thisNode, connection, frame)

            cut_frame += random.randint(time_range[0], time_range[1])
            
            i += 1
            last_connection = connection 

def include_multi_index(thisNode, items):

    squared_videos = thisNode.getParam('squared_videos').get()
    vertical = squared_videos
    horizontal = squared_videos

    # si la cantidad de imagenes es mayor a 4 crea las slide de 4 imagenes
    fours = []
    if (squared_videos * squared_videos ) > 4:
        fours = get_four_indexs(vertical, horizontal) 
    # ----------------
    
    pairs_amount = thisNode.getParam('pairs_indexs').get()
    pairs = get_pair_indexs(vertical, horizontal, pairs_amount, skip=fours)

    scale = 1.0 / horizontal
    
    for index, item in enumerate(items):
        crop, transform = item
        userTextArea = crop.getParam('userTextArea')

        scale_param = transform.getParam('scale')
        translate = transform.getParam('translate')
        size = crop.getParam('size')
        
        scale_param.set(scale, scale)
        margin(thisNode, crop)

        crop_data = str(squared_videos) + ', 0, 0'
        userTextArea.set(crop_data)
        
        # slide con 4 imagenes
        if len(fours):
            if index in fours:
                size.set(0, 0)
                userTextArea.set('0')

            if index == fours[0]:
                new_scale = scale * 2
                scale_param.set(new_scale, new_scale)
                margin(thisNode, crop, double=True)
                crop_data = str(squared_videos) + ', 0, 1'
                userTextArea.set(crop_data)
        # ----------------
        
        # slide con 2 imagenes
        for pair in pairs:
            if index in pair:
                size.set(0, 0)
                userTextArea.set('0')
            
            # sube la escala al primer item 
            if index == pair[0]:
                new_scale = scale * 2
                scale_param.set(new_scale, new_scale)                
                margin(thisNode, crop, mid=True, double=True)

                # restamos la mitad de la imagen para que quede centrada
                translate_x = translate.getValue() - (( 1920 * scale ) / 2)
                # -----------------
                translate.setValue(translate_x)

                crop_data = str(squared_videos) + ', 1, 1'
                userTextArea.set(crop_data)                
            
            # --------------

def get_all_mosaics(thisNode):
    mosaics = []
    for mosaic_index in range(100):
        mosaic = []
        for slide_index in range(100):
            index = '_' + str(mosaic_index) + '_' + str(slide_index)
            crop = getNode(thisNode, 'crop' + index)
            transform = getNode(thisNode, 'transform' + index)
            blur = getNode(thisNode, 'blur' + index)
            dissolve = getNode(thisNode, 'dissolve' + index)

            if not transform:
                break

            mosaic.append({
                'crop': crop,
                'transform': transform,
                'blur': blur,
                'dissolve': dissolve
            })
        
        if len(mosaic):
            mosaics.append(mosaic)
        else:
            break

    return mosaics

def import_videos(thisNode, app):
    videos_folder = thisNode.videos_dir.get()

    posx = 0
    for index, video in enumerate(os.listdir(videos_folder)):
        picture = videos_folder + '/' + video
        reader = app.createReader( picture, thisNode )
        reader.setPosition(posx - 12, -300)
        reader.setLabel('reader_' + str(index))
        reader.getParam('outputComponents').set(0)

        # para ajustar el reformat
        _width = reader.getOutputFormat().width()
        _height = reader.getOutputFormat().height()
        aspect = 1920.0 / 1080.0 # aspecto de referencia
        aspect_input = float(_width) / float(_height)
        # -------------

        reformat = createNode('reformat', 'reformat_' + str(index), thisNode, position=[posx, -150])
        reformat.getParam('reformatType').set(1)
        reformat.getParam('boxFixed').set(1)
        reformat.getParam('boxSize').set(1920, 1080)

        if aspect <= aspect_input:
            reformat.getParam('resize').set(2)
        reformat.connectInput(0, reader)

        posx += 150

def create_mosaic_a(thisNode):
    amount = thisNode.getParam('mosaic_a_amount').get()

    # obtiene la ultimo slide del ultimo mosaico para sacar la ultima posicion
    all_mosaics = get_all_mosaics(thisNode)
    if len(all_mosaics):
        last_slide = all_mosaics[-1][-1]
        transform = last_slide['transform']
        posx = transform.getPosition()[0] + 150
    else:
        posx = -200

    for i in range(amount):
        index = len(all_mosaics) + i
        posx = create_one_mosaic_a(thisNode, str(index), posx + 200)

    cuts_create(thisNode)

def create_one_mosaic_a(thisNode, name, posx = 0):
    
    squared_videos = thisNode.getParam('squared_videos').get()
    vertical = squared_videos
    horizontal = squared_videos

    scale = 1.0 / horizontal
    left_pos = 1920 / horizontal
    up_pos = 1080 * scale

    items = get_items(thisNode)
    items_random = random.sample(items, len(items)) # random sin repetir

    posy = 500

    merge = createNode('merge', 'merge_' + name, thisNode, position=[posx, posy + 500])

    created_items = []
    left = 0
    conections = 3
    video_index = 0
    for l in range(horizontal):
        up = 0
        for u in range(vertical):
            index = str(video_index)
            
            reformat = items_random[video_index]['reformat']
            crop = createNode('crop', 'crop_' + name + '_' + index, thisNode, position=[posx, posy])
            crop.connectInput(0, reformat)

            transform = createNode('transform', 'transform_' + name + '_' + index, thisNode, position=[posx, posy + 150])
            transform.getParam('scale').set(scale, scale)
            transform.getParam('center').set(0,0)

            transform.getParam('translate').set(left, up)
            transform.connectInput(0, crop)

            blur = createNode('blur', 'blur_' + name + '_' + index, thisNode, position=[posx, posy + 200])
            blur.getParam('NatronOfxParamProcessA').set(1)
            blur.connectInput(0, transform)
            
            dissolve = createNode('dissolve', 'dissolve_' + name + '_' + index, thisNode, position=[posx, posy + 250])
            dissolve.connectInput(1, blur)
            dissolve.getParam('which').set(1)

            created_items.append([crop, transform])
            
            conections += 1
            merge.connectInput(conections, dissolve)
            
            up += up_pos
            posx += 120
            video_index += 1

        left += left_pos
    
    include_multi_index(thisNode, created_items)

    return posx