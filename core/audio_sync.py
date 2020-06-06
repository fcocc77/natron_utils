from scipy.io import wavfile
import json
import os
import subprocess

def sh(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
    return str(proc.communicate()[0])

def wave(wav, frame_rate = 30 ):
    fs, data = wavfile.read(wav)

    # obtiene duracion del audio
    meta = sh('ffprobe -show_streams "' + wav + '"')
    seconds = float(meta.split('duration=')[1].split("\\")[0])
    # -------------------
    print(seconds)
    count = len(data)

    # segundos a frames
    frames = (seconds * frame_rate)
    # ---------

    accuracy = 20

    # separacion de los datos del wav para usarlos como frames
    each = count / frames
    # ---------------------

    # crea una lista nueva solo con el primer canal del stereo,
    # y convirtiendo todos los datos negativos - en positivos +
    curve_points = []
    for i in range(0, count, int(each / accuracy)):
        value = abs( data[i][0] / fs )
        curve_points.append(value)
    # ----------------------

    def smooth(data):
        smooth = 10 * accuracy

        count = len(data)

        # crea una lista con el promedio de cada valor,
        # a partir del valor de smooth hacia la derecha y a la izquierda
        # para emparejar los valores a los valores anteriores y siguientes.
        curve = []
        for frame, value in enumerate(data):
            average = 0
            average += value

            average_count = 1
            for i in range(smooth):
                plus_index = frame + i
                if plus_index < count:
                    average += data[plus_index]
                    average_count += 1

                less_index = frame - i
                if less_index > 0:
                    average += data[less_index]
                    average_count += 1

            curve.append(average / average_count)
        # ------------------------

        # conviete los valores numpy.float a float normal
        out_list = []
        for i in range(0, count, accuracy ):
            value = curve[i]
            out_list.append(float(value))
        # ------------------------

        return out_list

    final_curve = smooth(curve_points)

    out_data = json.dumps( final_curve )
    output = wav.split('.')[0] + '.json'
    f = open(output, 'w')
    f.write(out_data)
    f.close()

    return final_curve

def wav_create(video):
    wav = video.split('.')[0] + '.wav'
    os.system('ffmpeg -y -i "' + video + '" "' + wav + '"')
    return wav

video_base = '/home/pancho/Desktop/video_audio2.mov'
audio_base = wav_create(video_base)
json_base = wave(audio_base)

video_sync = '/home/pancho/Desktop/part.mov'
audio_sync = wav_create(video_sync)
json_sync = wave(audio_sync)

