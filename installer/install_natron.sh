#!/usr/bin/env sh
path="$(dirname "$0")"

natron_tar="/mnt/server_01/software/natron/installer/Natron2.tar.gz"

yum -y install libXi libXrender libXrandr libXcursor libXinerama libSM lcms2

dst='/opt'

rm -rf ~/.cache/INRIA/Natron
rm -rf $dst/Natron2
tar zxvf $natron_tar -C $dst

chown root:root -R $dst/Natron2
chmod 755 -R $dst/Natron2
