renderer=$1
data=$2

path=$(dirname "$0")

$renderer -b "$path/production_ntp.py" "$data"
