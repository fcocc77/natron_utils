cd $(dirname $0)

sh ../install.sh

mkdir -p ../temp
testing_py="../temp/testing.py"
renderer="/opt/Natron2/NatronRenderer"
project="/home/pancho/Documents/GitHub/videovina/private/templates_base/testing/comp/ntp/testing_473-922.ntp"

echo "
from project import testing
testing(
    app=app,
    project='$project',
    slide_range=[2, 6],
    format=2,  # quarter, half, hd, 4k
    speed=0  # Slow, Normal, Fast
)" >$testing_py

$renderer $testing_py
