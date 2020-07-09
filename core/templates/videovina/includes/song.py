
def play_song(thisNode, play=True):
    if not play:
        os.system('pkill -9 vlc')
        return

    cmd = 'vlc --qt-start-minimized "' + get_current_song(thisNode)[1] + '"'

    os.system('pkill -9 vlc')
    os.popen2(cmd)


def get_type_song(thisNode, song_name):
    for option in thisNode.getParam('default_song').getOptions():
        if song_name in option:
            song_type = option.split('-')[1].strip().lower()
            return song_type


def get_current_song(thisNode):
    default_song = thisNode.getParam('default_song')
    private = thisNode.getParam('videovina_root').get() + '/private'

    song = default_song.getOption(default_song.get())
    song_type = song.split('-')[1].strip().lower()
    song_name = song.split('-')[0].strip()
    song_path = private + '/music/' + song_type + '/' + song_name + '.mp3'

    return [song_name, song_path, song_type]
