#!/bin/bash

rm -rf /tmp/.X0-lock


Xvfb -shmem -screen 0 1280x1024x24 &

source /opt/jderobot/setup.bash
source /opt/ros/kinetic/setup.bash
source /opt/jderobot/share/jderobot/gazebo/gazebo-assets-setup.sh
export PYTHONPATH=$PYTHONPATH:/home/jderobot/.exercises

cd ~/gzweb
npm start &

cd ~/volume/user/exercise

jupyter nbextension enable hide_input/main --user
jupyter nbextension enable init_cell/main --user
jupyter notebook --ip=0.0.0.0 --allow-root &

cd ~

EXTENSION=`echo "$1" | cut -d'.' -f2`
if [ $EXTENSION = "world" ]
  then
    roscore &
fi

if ! [ -z "$2" ]
  then
    python ~/referees/$2 &
fi

if ! [ -z "$1" ]
  then
    EXTENSION=`echo "$1" | cut -d'.' -f2`
    if [ $EXTENSION = "launch" ]
      then
        roslaunch /opt/jderobot/share/jderobot/gazebo/launch/$1
    else
        rosrun gazebo_ros gazebo /opt/jderobot/share/jderobot/gazebo/worlds/$1
    fi
else
    tail -f /dev/null
fi
