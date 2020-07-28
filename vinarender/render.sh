renderer=$1
project=$2
first_frame=$3
last_frame=$4
extra=$5

# borra la extencion .ntp, para poder meterlo como argumento
# sin que lo reconosca el NatronRenderer
project="${project::-4}"
# ----------------------------

path=$(dirname "$0")

$renderer --clear-cache --no-settings $first_frame-$last_frame "$path/render.py" "$project" "$extra"
