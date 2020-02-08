# Docker Unibotics-Mixed_Execution 
 
## Build

### Build for production
```bash
docker build --rm --build-arg VERSION=$(tail -1 README.md | cut -d' ' -f2) --build-arg BUILD_DATE=$(date '+%Y-%m-%d_%H:%M:%S') --build-arg DEV=1 --tag unibotics/mixed_execution .
```

### Build for development
```bash
docker build --rm --build-arg BUILD_DATE=$(date '+%Y-%m-%d_%H:%M:%S') --build-arg DEV=1 --tag unibotics/mixed-execution:dev .
```

### Run by terminal
```bash
docker run --name pruebas -e DISPLAY=:0 -e JDEROBOT_SIMULATION_TYPE=REMOTE --entrypoint /entrypoint_mixed_execution.sh -v /tmp/siguelineaIR:/home/jderobot/volume/user/exercise:rw --privileged -v /dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -p 8888:8888 -p 8080:8080 -it unibotics/mixed_execution
```

## Changelog

* 1.0.0 - Mixed Execution Support
* 2.0.0 - Local Simulation (ICE+ROS)
* 2.1.0 - Multi-User Local Simulation (competitive exercises)
* 2.2.0 - Real Robot Support
* 2.2.1 - PiBot management
* 2.2.2 - Tello management
* 2.2.3 - TurtleBot2 management
