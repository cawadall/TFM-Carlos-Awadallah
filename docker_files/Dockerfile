FROM ubuntu:xenial

ARG DEV
ARG VERSION
## Build Date at the end of the file
LABEL version=$VERSION

SHELL ["/bin/bash", "-c"]

RUN apt update && apt install -y python3-all python3-pip python-all python-pip && rm -rf /var/lib/apt/lists/*

RUN pip2 install --upgrade pip && pip3 install --upgrade pip

RUN pip2 install matplotlib

RUN pip3 install jupyter

RUN python2 -m pip install ipykernel
RUN python2 -m ipykernel install

## Jupyter widgets and extensions
RUN pip2 install ipywidgets
RUN pip2 install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --system
RUN jupyter nbextension enable --py widgetsnbextension

### REPOSITORIES ###
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list

RUN sh -c 'echo deb http://zeroc.com/download/apt/ubuntu16.04 stable main > /etc/apt/sources.list.d/zeroc.list'
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 5E6DA83306132997

RUN sh -c 'echo "deb http://wiki.jderobot.org/apt xenial main" > /etc/apt/sources.list.d/jderobot.list'
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 24E521A4

RUN echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable xenial main" > /etc/apt/sources.list.d/gazebo-stable.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 67170598AF249743


### DEPS ###
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654
RUN apt update && apt install -y jderobot-comm-python ros-kinetic-rospy ros-kinetic-rosbash ros-kinetic-mavros && rm -rf /var/lib/apt/lists/*

RUN pip install  pyyaml


### REFEREES DEPS ###

RUN apt update && apt install -y git && rm -rf /var/lib/apt/lists/*
RUN pip2 install git+https://github.com/dpallot/simple-websocket-server.git

### EXERCISES DEPS ###

RUN python2 -m pip install scipy

### SIMULATION DEPS ###

RUN apt update && apt install -y jderobot-gazebo && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y jderobot-gazebo-assets && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y ros-kinetic-gazebo-ros  ros-kinetic-gazebo-plugins ros-kinetic-gazebo-msgs && rm -rf /var/lib/apt/lists/* 

# dependencies needed by librealsense. `deb -i` will not resolve these
RUN apt update && apt install -y binutils cpp cpp-5 dkms fakeroot gcc gcc-5 kmod libasan2 libatomic1 libc-dev-bin libc6-dev libcc1-0 libcilkrts5 libfakeroot libgcc-5-dev libgmp10 libgomp1 libisl15 libitm1 liblsan0 libmpc3 libmpfr4 libmpx0 libquadmath0 libssl-dev libssl-doc libtsan0 libubsan0 libusb-1.0-0 libusb-1.0-0-dev libusb-1.0-doc linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic linux-headers-generic linux-libc-dev make manpages manpages-dev menu patch zlib1g-dev
RUN apt update && apt install -y libssl-dev libssl-doc libusb-1.0-0 libusb-1.0-0-dev libusb-1.0-doc linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic linux-headers-generic zlib1g-dev

# modify librealsense deb (unpack, replace script, repack)
RUN apt update && apt download ros-kinetic-librealsense
RUN dpkg-deb -R ros-kinetic-librealsense*.deb ros-rslib/

RUN wget https://gist.githubusercontent.com/dizz/404ef259a15e1410d692792da0c27a47/raw/3769e80a051b5f2ce2a08d4ee6f79c766724f495/postinst
RUN chmod +x postinst
RUN cp postinst ros-rslib/DEBIAN
RUN dpkg-deb -b ./ros-rslib/ ros-kinetic-librealsense_1.12.1-0xenial-20190830_icrlab_amd64.deb

# install container friendly libsense
RUN dpkg -i ros-kinetic-librealsense_1.12.1-0xenial-20190830_icrlab_amd64.deb

# lock from updates
RUN apt-mark hold ros-kinetic-librealsense
RUN apt update && apt install -y ros-kinetic-librealsense
RUN apt update && apt install -y ros-kinetic-realsense-camera
RUN apt update && apt install -y ros-kinetic-turtlebot

### ROSBRIDGE FOR JAVASCRIPT ###
RUN apt-get update && apt-get install -y ros-kinetic-rosbridge-suite

# Deleting monaco models because break gzweb
RUN rm -rf /opt/jderobot/share/jderobot/gazebo/models/monaco*

### GZWEB DEPS ###

RUN apt update && apt install -y gazebo9 libgazebo9-dev && rm -rf /var/lib/apt/lists/*

### UPDATING NPM AND NODE ###
RUN apt update && apt install curl
RUN curl -sL https://deb.nodesource.com/setup_8.x | sudo bash -
RUN apt update && apt install -y libjansson-dev nodejs libboost-dev imagemagick libtinyxml-dev mercurial cmake build-essential && rm -rf /var/lib/apt/lists/*
RUN  apt update && apt install -y xvfb && rm -rf /var/lib/apt/lists/*


### COPY files ###
COPY installGzweb.sh /
COPY entrypoint_mixed_execution.sh /

### REMOVING GUI FROM ROSLAUNCH ###
RUN  sed -i 's/name="gui" value="true"/name="gui" value="false"/g' /opt/jderobot/share/jderobot/gazebo/launch/*.launch 
### Create User And Group ###
RUN useradd -ms /bin/bash jderobot
RUN groupadd -g 555 kibotics
RUN usermod -g kibotics jderobot
RUN usermod -a -G jderobot jderobot
USER jderobot
## All commands launch after this will be launch as jderobot ##
WORKDIR /home/jderobot

### CLONE GZWEB ###
RUN /installGzweb.sh

# ocultar barra lateral del simulador
RUN sed -i "s/globalEmitter.emit('openTab', 'mainMenu', 'mainMenu');/globalEmitter.emit('openTab', 'mainMenu', 'mainMenu');globalEmitter.emit('closeTabs', true);/g" gzweb/http/client/gz3d.gui.js

# copiar todos los modelos bien
RUN cp -r /opt/jderobot/share/jderobot/gazebo/models/* /home/jderobot/gzweb/http/client/assets/

### Adding Sources ### 
RUN echo "source /opt/ros/kinetic/setup.bash" >> .bashrc
RUN echo "source /opt/jderobot/setup.bash" >> .bashrc  
RUN echo "source /opt/jderobot/share/jderobot/gazebo/gazebo-assets-setup.sh" >> .bashrc  
# Estan en el entrypoint

### CONFIG JUPYTER ### 
ADD --chown=jderobot:kibotics jupyter .jupyter

RUN mkdir -p volume/user/exercise

USER jderobot

### WEBSOCKETS ###
COPY web_sockets_server /opt/jderobot/lib/python2.7/web_sockets_server

### TELLO ###

COPY compiled/tello /opt/jderobot/lib/python2.7/tello
USER root
WORKDIR /opt/jderobot/lib/python2.7/tello/scripts
RUN ./linux_install.sh
WORKDIR /home/jderobot
USER jderobot

### EXTRAS ###
#COPY tmp/f1_2robots_simplecircuit.world /opt/jderobot/share/jderobot/gazebo/worlds/


RUN cp /home/jderobot/gzweb/http/client/assets/RedArDrone2/meshes/quadrotor/quadrotor_4.dae /home/jderobot/gzweb/http/client/assets/RedArDrone2/meshes/quadrotor/red_quadrotor.dae
### install ENTRYPOINTS ###
ENTRYPOINT /entrypoint_mixed_execution.sh

# BUILD DATE
ARG BUILD_DATE

LABEL build-date=$BUILD_DATE


