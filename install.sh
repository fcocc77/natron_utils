#! /usr/bin/sh
cd $(dirname "$0") # Directorio Raiz

plugins="/usr/share/Natron/Plugins"
vinarender="$(cat /etc/vinarender)/modules/natron"

mkdir -p $plugins
rm -rf $plugins/*

mkdir -p $vinarender
rm -rf $vinarender/*

# copia el core a la carpeta plugins de natron
cp -rf ./core $plugins
cp -rf ./plugins $plugins
cp -rf ./testing $plugins

cp -rf ./vinarender/* $vinarender

# inserta la ruta de la instancia a init.py
init="$plugins/core/init.py"
sed -i "s|{path}|$plugins|g" $init

chmod 777 -R $plugins
