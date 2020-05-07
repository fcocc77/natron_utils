import os
import shutil
import re
import fnmatch
import NatronEngine
import NatronGui
from PySide import QtCore

def collect_files():
    app = NatronGui.natron.getGuiInstance(0)

    project_path = os.path.dirname( os.path.dirname( app.getProjectParam('projectPath').get() ) )
    footage = project_path + '/footage'
    relative_base = '[Project]/../footage'

    reconect_files = ''
    index = 0
    for node in app.getSelectedNodes():
        filename_param = node.getParam('filename')
        if filename_param:
            filename = filename_param.get()

            if relative_base in filename:
                continue

            dirpath = os.path.dirname( filename )
            dirname = os.path.basename( dirpath )
            basename = os.path.basename( filename )

            # Padding
            padding = re.search('(#+)|(%\d\d?d)', filename)
            padding = padding.group(0) if padding else ''
            #-----------------------------------------------

            dst_dir = footage + '/' + dirname
                
            if not os.path.isdir(dst_dir):
                os.makedirs(dst_dir)

            src = filename
            if padding:
                _basename =  basename.replace( padding, '' ).split('.')[0] 
                # encuentra todos los archivos que contengas la base de la secuencia
                sequence = sorted( fnmatch.filter( os.listdir( dirpath ), _basename + '*' ) )
                # ------------------------

                for _file in sequence:
                    _src = dirpath + '/' + _file
                    dst = dst_dir + '/' + _file
                    if not os.path.isfile(dst):
                        shutil.copy2( _src, dst )
            else:
                dst = dst_dir + '/' + basename

                if not os.path.isfile(dst):
                    shutil.copy2(src, dst)

            relative = relative_base + '/' + dirname + '/' + basename
            filename_param.set(relative)

            index += 1
            reconect_files += str( index ) + ' - ' + src + '  --->  ' + relative + '\n\n'
            
    if reconect_files:
        NatronGui.natron.informationDialog('Collect Files', reconect_files)



NatronGui.natron.addMenuCommand('Videovina/Collect Files', 'collect_files.collect_files',
                                QtCore.Qt.Key.Key_F, QtCore.Qt.KeyboardModifier.ShiftModifier)
