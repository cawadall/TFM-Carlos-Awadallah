#!/bin/bash
cd ~; hg clone https://bitbucket.org/osrf/gzweb

cd ~/gzweb
hg up gzweb_1.4.0
sed -i 's/"websocket": "^1.0.25"/"websocket": "1.0.26"/g' package.json
source /opt/jderobot/setup.bash
source /opt/ros/kinetic/setup.bash
source /opt/jderobot/share/jderobot/gazebo/gazebo-assets-setup.sh
Xvfb -shmem -screen 0 1280x1024x24 &
export DISPLAY=:0
npm run deploy --- -m local
npm install


rm -rf /tmp/.X0-lock
