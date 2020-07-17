#! /usr/bin/sh
cd $(dirname "$0") # Directorio Raiz

function install() {
    mkdir -p $1
    rm -rf $1/*

    # copia el core a la carpeta plugins de natron
    cp -rf ./core $1
    cp -rf ./plugins $1
    cp -rf ./vinarender $1
    cp -rf ./testing $1

    # inserta la ruta de la instancia a init.py
    init="$1/core/init.py"
    sed -i "s|{path}|$1|g" $init

    chmod 777 -R $1
}

plugins="/usr/share/Natron/Plugins"
install "$plugins"
