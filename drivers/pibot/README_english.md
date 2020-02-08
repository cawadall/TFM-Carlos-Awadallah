# PiBot


## Pibot - Driver

This document is user guide of driver **piBot.py**

First of all, we have to create our object named *robot* in this example. You can
choose the name you want. We do this as follow:

```
import piBot

robot = piBot.PiBot("PiCam")
```

This driver allows you to control all functionalities of your PiBot.

What will be told in the next lines is the specification of each method
of this driver, showing his header and the parameters it receive, with a brief usage example of him.

## 1º *avanzar*

The robot will go forward with a specificated speed.

### Header:

The header of this method is ``avanzar(vel)``.

### Parameters:

- **vel:** Velocity which you want the robot moves forward in meters per second. Velocity range
  is between 0 and 0.25 [m/s].

### Usage Example:

```
try:
  while(True):
    robot.avanzar(0.08)
    time.sleep(0.2)
except KeyboardInterrupt:
  robot.fin()
```

This will do that the robot goes forward with a speed of 0.08 meters per second until
user press ``ctrl+c``; then, the robot will stop. Later is explained the method *fin*.

## 2º *retroceder*

The robot will go back with a specificated speed.

### Header:

His header is ``retroceder(vel)``.

### Parameters:

**vel:** Velocity which you want the robot moves backward in meters per second.
  Velocity range is between 0 and 0.25 [m/s].

### Usage Example:

```
try:
  while(True):
    robot.retroceder(0.15)
    time.sleep(0.2)
except KeyboardInterrupt:
  robot.fin()
```

It will do that the robot goes backward with a speed of 0.15 meters per second until user press ``crtl+c``; then, the robot will stop.

## 3º *parar*

It will do that robot stops.

### Header:

His header is ``parar()``.

### Parameters:

As you can see, this method does not receive parameters.

### Usage Example:

```
while(True):
  robot.avanzar(0.05)
  time.sleep(5)
  robot.parar()
  time.sleep(2)
  robot.retroceder(0.05)
  time.sleep(5)
  robot.parar()
  time.sleep(2)
```

As you can observe, this code will do that robot goes forward during 5 seconds, later
it will stop during 2 seconds, then robot will go backward during 5 seconds and it will
stop during 2 sencond again. That secuence will be executing in an infinite loop.

## 4º *girarIzquierda*

This method will do that robot turns left.

### Header:

His header is ``girarIzquierda(velW)``.

### Parameters:

* **velW:** Angular speed that you want robot to turn. It is indicated in radians per second [rad/s].

### Usage Example:

```
Pi = 3.1416;
robot.girarIzquierda()
time.sleep(1.5)
```

This code serves to do turn left the robot with a speed of Pi/4 radians per second (45 degrees per second) during 1.5 seconds.

## 5º *girarDerecha*

His functionlity is to turn right the robot.

### Header:

His header is ``girarDerecha(velW)``.

### Parameters:

* **velW:** Angular speed that you want robot to turn. It is indicated in radians per second [rad/s].

### Usage Example:

```
Pi = 3.1416
robot.girarDerecha(Pi / 6)
time.sleep(1.5)
```

This code serves to do turn right the robot with a speed of Pi/6 radians per second (30 degrees per second) during 1.5 seconds.

## 6º *moverHasta*

This method serves to do robot to describe a linear movement to a
specificated position.

### Header:

His header is ``moverHasta(pos)``.

### Parameters:

* **pos:** Position which you want the robot moves, in meters. If *pos* has a positive value, robot will move forward; if *pos* has a negative value, robot will move backward.

### Usage Example:

```
robot.moverHasta(0.5)
robot.parar()
```

This code will do robot to go forward 0.5 meters and them, it will stop.

## 7º *girarHasta*

This method serves to do robot to turn an specificated angle.

### Header:

His header is ``girarHasta(angle)``.

### Parameters:

* **angle:** This is the angle, in radians, that robot has to turn. If angle value is positive, the robot will turn left; if angle value is negative, the robot will turn right.

### Usage Example:

```
Pi = 3.1416
robot.girarHasta(Pi / 2)
robot.girarHasta(-Pi)
```

This code will do robot to turn left 90 degrees (Pi / 2 radians) and after, it turn right 180 degrees (Pi radians).

## 8º *arcoHasta*

*arcoHasta* allows you to move the robot to a specific location. The location in the plane is as follow:

On one hand, there is an "linear" position, given by 'x' position and 'y' position. On the other hand, there is an "angular" position, given by an angle ("theta", for example).

### Header:

The header of this method is `arcoHasta(x, y, theta)`.

### Parameters:

- **x:** Position in meters of the "x" axis that you want the robot to move.
- **y:** Position in meters of the "y" axis that you want the robot to move.
- **theta:** Angle in radians that you want the robot turn.

### Usage Example:

```
Pi = 3.1416

x = 0.3
y = 0.4
t = Pi / 2
robot.arcoHasta(x, y, t)
```

The robot will move to the relative position (0.3, 0.4, Pi / 2).

## 9º *fin*

This method delete the "robot" object.

### Header:

His header is ``fin()``.

### Parameters:

This method does receive any parameter.

## 10º *move*

This method allows you to move the robot with a speed control. You can move the robot with a specificated linear and angular velocity.

Depending on the the sign of each parameter, the robot will do different arcs in different directions.

### Header:

His header is ``move(velV, velW)``.

### Parameters:

- **velV:** Linear speed, in meters per second, that you want the robot to move.
- **velW:** Angular speed, in radians per second, that you want the robot to move.

### Usage Example:

```
robot.move(0.05, 0.8)
time.sleep(4)
robot.fin()
```

This code will do the robot to move describing an arc countercloskwise with linear speed of 0.05 meters per second and 0.8 radians per second of angular speed.

## 11º *leerIRSiguelineas*

This method serves to read the state of the infrared sensors.
PiBot has two infrared sensors and each of them is capable of detect if it is being over a black place. So there is four possible cases and, method *leerIRSigueLineas* returns a different number depending on each possibility.
The number code that this method returns is as follow:

| Left Sensor State | Right Sensor State | Returned Value |
| ----------------- | ------------------ | -------------- |
| 0                 | 0                  | 3              |
| 0                 | 1                  | 2              |
| 1                 | 0                  | 1              |
| 1                 | 1                  | 0              |

### Header:

His header is ``leerIRSigueLineas()``.

### Parameters:

This method does receive any parameter.

### Usage Example:

```
try:

  while(True):
    if(robot.leerIRSigueLineas() == 1):
      robot.avanzar(0.05)
    else:
      robot.girarDerecha()
    time.sleep(0.1)

except KeyboardInterrupt:
  robot.fin()
```

This code will do the robot to go forward while robot is over the black line. If not, robot will turn right.

## 12º *leerUltrasonido*

It returns the distance (in meters) between robot and an object.

### Header:

His header is ``leerUltrasonido()``

### Parameters:

This method does receive any parameter.

### Usage Example:

```
try:

  while(True):
    dist = robot.leerUltrasonido()
    print(dist)
    if(dist > 0.15)
      robot.avanzar(0.08)
    else:
      girarHasta(Pi / 2)

    time.sleep(0.2)

except KeyboardInterrupt:
  pass
```

This code will do the robot to go forward while there is not an object nearer than 15 cm (0.15 m), and else, turn left 90 degrees (Pi / 2). In addition, it will we printed on the screen the different distances that sensor reads.

## 13º *DameImagen*

It returns the frame that camera is capturing in that instant.

### Header:

His header is ``dameImagen()``.

### Parameters:

This method does receive any parameters.

### Usage Example:

At the next method explanation, there is an example about how to show by the screen what camera is capturing.

## 14º *mostrarImagen*

This method shows by screen an image previously captured by the PiBot's camera.

### Header:

His header is ``mostrarImagen()``.

### Parameters:

This method does receive any parameters.

### Usage Example:

```
try:
    while(True):
        frame = robot.dameImagen()
        robot.mostrarImagen()
        time.sleep(0.2)

except KeyboardInterrupt:
    robot.fin()
```

## 15º *dameObjeto*

This method returns two things. One of them is the center of the object (in **(x,y)** format) whose color
is specificated by parameter, and the other is his area (in pixels).

### Header:

His header is ``dameObjeto(lower, upper, showImageFiltered)``.

### Parameters:

- **lower:** This is an array that contains HSV lower values of the color that you want to detect.
- **upper:** This is an array that contains HSV high values of the color that you want to detect.
- **showImageFiltered:** This parameters have to be "True" or "False" and it serves to show the image filtered or not.

**Note:** All the parameters are optional. If you use the method *dameObjeto* without parameters, *lower* and *upper* have default values to detect an orange object, and *showImageFiltered* has "False" value.

### Usage Example:

```
try:

    (center, area) = robot.dameObjeto
    print "center:", center, "area:", area
    time.sleep(0.5)

except KeyboardInterrupt:
    robot.fin()
```

This program prints by screen the center and the area of an orange object. If we want to detect a blue object, for example, we should do it as follow:

```
import numpy

lower_blue = numpy.array([100,65,75], dtype=numpy.uint8)
upper_blue = numpy.array([130, 255, 255], dtype=numpy.uint8)

try:

    (center, area) = robot.dameObjeto(lower=lower_blue, upper=upper_blue)
    print "center:", center, "area:", area
    time.sleep(0.5)

except KeyboardInterrupt:
    robot.fin()
```





## API Kibotics

## PiBot simulado
API pública para programar el robot "PiBot" simulado. Este API tiene partes comunes con otros robots como el MBot. Este documento es temporal hasta que se asiente toda la infraestructura y se documenten todas las funciones y se genere de forma automática el API, por lo que algunas funciones pueden tener efectos diferentes en real y en simulado.

### Actuadores

Funciones que manejan los actuadores del robot: motores, servos, leds, etc.

#### Servos
```
moverServo(*args)
    Función que hace girar el servo a un ángulo dado como parámetro.
    (Actualmente no soportado en simulación)
    @args: lista
    @params: lista de argumentos:
    args[0]: puerto al que está conectado el controlador del servo
    args[1]: banco al que está conectado el servo en el controlador
    args[2]: ángulo de giro del servo, entre 0 y 180º.
```
#### Motores
```
avanzar(vel)
    Función que hace avanzar al robot en línea recta a una velocidad dada como parámetro
    @type vel: entero
    @param vel: velocidad de avance del robot (unidades por determinar)
```
```
retroceder(vel)
    Función que hace retroceder al robot en línea recta a una velocidad dada como parámetro
    @type vel: entero
    @param vel: velocidad de retroceso del robot (unidades por determinar)
```
```
parar()
    Función que hace detenerse al robot
```
```
girarIzquierda(vel)
    Función que hace rotar al robot sobre su propio eje hacia la izquierda a una velocidad dada como parámetro
    @type vel: entero
    @param vel: velocidad de giro del robot (unidades por determinar)
```
```
girarDerecha(vel)
    Función que hace rotar al robot sobre su propio eje hacia la derecha a una velocidad dada como parámetro
    @type vel: entero
    @param vel: velocidad de giro del robot (unidades por determinar)
```
```
move(velV, velW)
    Función que hace avanzar y girar al robot al mismo tiempo según las velocidades v,w dadas como parámetro
    @type velV, velW: entero
    @param velV: velocidad de avance en línea recta (unidades por determinar)
    @param velW: velocidad de giro (unidades por determinar)
```

### Sensores
Funciones que obtienen información sensorial del robot: cámaras, IR, ultrasonidos,etc.

#### Cámaras
```
dameImagen()
    Función que muestra una imagen por pantalla.
    @return: imagen obtenida por la picam
    @rtype: imagen openCV (Mat)
```
```
leerIRSigueLineas()
    Función que devuelve las lecturas del sensor siguelíneas (asumiendo que el sensor consta de dos sensores IR integrados), con la siguiente codificación:
        0: ambos sensores están sobre la línea
        1: sólo el sensor izquierdo está sobre la línea
        2: sólo el sensor derecho está sobre la línea
        3: ningún sensor está sobre la línea
    @return: valor codificado de las lecturas del sensor siguelíneas
    @rtype: entero
    NOTA: dependiendo de la máquina en la que se ejecute gazebo, este sensór será más responsivo o menos.
```
```
leerUltrasonido()
    Función que devuelve el valor numérico obtenido de las lecturas del sensor ultrasonidos
    @return: valor de distancia entre el sensor de ultrasonidos y un obstáculo en su trayectoria.
    @rtype: entero
```

### Genéricos
Funciones genéricas no relacionadas con sensores o actuadores

```
quienSoy()
    Función que imprime por consola una cadena de caracteres indicando qué instancia del robot se está utilizando: real o simulado
```
