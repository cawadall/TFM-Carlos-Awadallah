# PiBot


## Pibot - Driver

Este documento es una guía de usuario del driver **piBot.py**.

Lo primero de todo, es necesario crear nuestro objeto,, al que llamaremos *robot* en este ejemplo. Tú puedes elegir el nombre que desees. Lo haremos de la siguiente manera:

```
import piBot

robot = piBot.PiBot("PiCam")
```

Este driver te permitirá controlar todas las funcionalidades de tu PiBot.

## 1º *avanzar*

El robot se moverá hacia adelante a la velocidad especificada.

### Cabecera:

La cabecera de este método es ``avanzar(vel)``.

### Parámetros:

- **vel:** Velocidad a la que deseas que el robot avance, en metros por segundo. El rango de velocidades comprende entre 0 y 0.25 [m/s] aproximadamente.

### Ejemplo de Uso:

```
try:
  while(True):
    robot.avanzar(0.08)
    time.sleep(0.2)
except KeyboardInterrupt:
  robot.fin()
```

Este código hará que el robot avance con ua velocidad de 0.08 metros por segundo hasta que el usuario presione ``ctrl+c``; en ese momento, el robot se detendrá. Más adelante se explica el método *fin*.

## 2º *retroceder*

El robot irá hacia atrás a una velocidad especificada.

### Cabecera:

Su cabecera es ``retroceder(vel)``.

### Parámetros:

* **vel:** Velocidad a la que deseas que el robot retroceda, en metros por segundo. El rango de velocidades oscila entre 0 y 0.25 [m/s] aproximadamente.

### Ejemplo de Uso:

```
try:
  while(True):
    robot.retroceder(0.15)
    time.sleep(0.2)
except KeyboardInterrupt:
  robot.fin()
```

Esto hará que el robot retroceda con una velocidad de 0.15 metros por segundo hasta que el usuario presione ``ctrl+c`` entonces, el robot se parará.

## 3º *parar*

Hará que el robot se detenga.

### Cabecera:

Su cabecera es ``parar()``.

### Parámetros:

Como puedes ver, este método no tecibe ningún parámetro.

### Ejemplo de Uso:

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

Tal y como puedes observar, este código provocará que tu robot avance durante 5 segundos, después se pare durante 2 segundos, posteriormente retroceda durante 5 segundos y, por último, se detenga otros dos segundos. Esta secuencia se repetirá sin parar porque se encuentra dentro de la estructura ``while(True)``.

## 4º *girarIzquierda*

Este método hará que el robot gire a la izquierda.

### Cabecera:

Su cabecera es ``girarIzquierda(velW)``.

### Parámetros:

* **velW:** Velocidad angular a la queremos que gire el robot. Se indica en radianes por segundo [rad/s].

### Ejemplo de Uso:

```
Pi = 3.1416;
robot.girarIzquierda(Pi / 4)
time.sleep(1.5)
```

Este código sirve para hacer girar al robot a la izquierda a una velocidad angular de Pi/4 radianes por segundo (45 grados por segundo) durante 1.5 segundos.

## 5º *girarDerecha*

Este método hará que el robot gire a la derecha.

### Cabecera:

His Cabecera is ``girarDerecha(velW)``.

### Parámetros:

* **velW:** Velocidad angular a la queremos que gire el robot. Se indica en radianes por segundo [rad/s].

### Ejemplo de Uso:

```
Pi = 3.1416
robot.girarDerecha(Pi / 6)
time.sleep(1.5)
```

Este código sirve para hacer girar al robot a la derecha a una velocidad angular de Pi/6 radianes por segundo (30 grados por segundo) durante 1.5 segundos.

## 6º *moverHasta*

Este método sirve para hacer que el robot describa un movimiento lineal (en línea recta) a una posición determinada.

### Cabecera:

Su cabecera es ``moverHasta(pos)``.

### Parámetros:

* **pos:** Posición a la que deseas que el robot se mueva, en metros. Si *pos* es un valor positivo, el robot se moverá hacia adelante; si *pos* tiene un valor negativo, el robot se moverá hacia atrás.

### Ejemplo de Uso:

```
robot.moverHasta(0.5)
robot.parar()
```

Este código hará que nuestro robot avance o.5 metros y entonces, se pare.

## 7º *girarHasta*

Este método sirve para hacer que el robot gire un ángulo determinado.

### Cabecera:

Su cabecera es ``girarHasta(angle)``.

### Parámetros:

- **angle:** Este es el ángulo, en radianes, que el robot girará. Si el valor de *angle* es positivo, PiBot girará a la hizquierda (sentido antihorario); si su valor es negativo, PiBot girará hacia la derecha (sentido horario);

### Ejemplo de Uso:

```
Pi = 3.1416
robot.girarHasta(Pi / 2)
robot.girarHasta(-Pi)
```

Este código hará que el robot gire 90 grados a la izquierda y, después, gire 180 grados a la derecha.

## 8º *arcoHasta*

*arcoHasta* te permite mover el robot a una localización específica. Esta localización en el plano funciona de la siguiente manera:

Por un lado, hay una posicion lineal dada por una posición en X y en Y (ejes de coordenadas). Por otro lado, existe una posición angular dada por un ángulo ("theta", por ejemplo).

### Cabecera:

La cabecerad  este método es `arcoHasta(x, y, theta)`.

### Parámetros:

- **x:** Posición en metros en el eje x a la que deseas que el robot se mueva
- **y:** Posición en metros en el eje y a la que deseas que el robot se mueva
- **theta:** Ángulo en radianes que quieres que el robot gire.

### ejemplo de Uso:

```
Pi = 3.1416

x = 0.3
y = 0.4
t = Pi / 2
robot.arcoHasta(x, y, t)
```

El robot se moverá a la posicón relativa (0.3, 0.4, Pi / 2).

## 9º *fin*

Este método elimina el objeto "robot".

### Cabecera:

Su cabecera es ``fin()``.

### Parámetros:

No recibe ningún parámetro.

## 10º *move*

Este método te permite mover el robot con un control en velocidad. Puedes mover tu PiBot con unas velocidades lineal y angular específicas.

Dependiendo de los signos de cada parámetro, el robot trazará diferentes arcos en distintas direcciones.

### Cabecera:

Su cabecera es ``move(velV, velW)``.

### Parameters:

- **velV:** Velocidad lineal, en metros por segundo, a la que deseas que se mueva el robot.
- **velW:**  Velocidad angular, en radianes por segundo, a la que deseas que se mueva el robot.

### Ejemplo de Uso:

```
robot.move(0.05, 0.8)
time.sleep(4)
robot.fin()
```

Este código hará que el robot se mueva describiendo un arco en sentido contrario a las agujas del reloj con una velocidad lineal de 0.05 metros por segundo y 0.8 radianes por segundo de velocidad angular

## 11º *leerIRSiguelineas*

Este método sirve para leer el estado de los sensores de infrarrojos. El PiBot tiene dos sensores infrarrojos y cada uno de ellos es capaz de detectar si se encuentra sobre una superficie blanca o negra. Por lo tanto, hay cuatro posibles casos y, el método *leerIRSigueLineas* devuelve un número diferente dependiendo de cada una de esas posibilidades.El código numérico que este método devuelve es el que se muestra a continuación:

| Estado Snsor Izquierdo | Estado Sensor Derecho | Valor Devuelto |
| ----------------- | ------------------ | -------------- |
| 0                 | 0                  | 3              |
| 0                 | 1                  | 2              |
| 1                 | 0                  | 1              |
| 1                 | 1                  | 0              |

### Cabecera:

Su cabecera es ``leerIRSigueLineas()``.

### Parameters:

Este método no recibe ningún parámetro.

### Ejemplo de Uso:

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

Este código hará que el robot avance mientras esté sobre la línea negra. Si no, el robot girará a la derecha.

## 12º *leerUltrasonido*

Devuelve la distancia (en metros) a la que se encuentra un obstáculo del robot.

### Cabecera:

Su cabecera es ``leerUltrasonido()``

### Parámetros:

Este método no recibe ningún parámetro.

### Ejemplo de Uso:

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

Este código hará que el robot avance mientras no exista ningún obstáculo más cerca de 15 cm (0.15 m) y, si no, girará a la izquierda 90 grados (Pi / 2). Además, las diferentes distancias leídas por el sensor se irán mostrando por pantalla.

## 13º *DameImagen*

Devuelve la imagen que la cámara está capturando en ese instante.

### Cabecera:

Su cabecera es ``dameImagen()``.

### Parámetros:

Este méetodo no recibe ningún parámetro.

### Ejemplo de Uso:

En la explicación del siguiente método hay un ejemplo sobre cómo mostrar por la pantalla lo que la cámara está capturando.

## 14º *mostrarImagen*

Este método muestra por la pantalla una imagen previamente capturada por la cámara del PiBot.

### Cabecera:

Su cabecera es ``mostrarImagen()``.

### Parámetros:

Este método no recibe parámetros.

### Ejemplo de Uso:

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

Este método devuelve dos cosas. Una de ellas es el centro del objeto (con el formato **(x,y)**) cuyo color es especificado por parámetro, y el otro es su área (en número de píxeles).

### Cabecera:

Su cabecera es ``dameObjeto(lower, upper, showImageFiltered)``.

### Parámetros:

- **lower:** Es un array que contiene los valores HSV inferiores del color que deseas detectar.
- **upper:** Es un array que contiene los valores HSV superiores del color que deseas detectar.
- **showImageFiltered:** Este parámetro tendrá que ser "True" o "False", y sirve para mostrar la imagen filtrada o no.

**Nota:** Todos los parámetros son opcionales. Si usas el método *dameObjeto* sin parámetros, *lower* y *upper* tendrán valores por defecto para detectar un objeto de color naranja, y *showImageFiltered* tednrá el valor "False".

### Ejemplo de Uso:

```
try:

    (center, area) = robot.dameObjeto
    print "center:", center, "area:", area
    time.sleep(0.5)

except KeyboardInterrupt:
    robot.fin()
```

Este programa muestra por pantalla el centro y el área de un objeto de color naranja. Si quisiéramos detectar un objeto azul, por ejemplo, deberíamos hacerlo de la siguiente manera:

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
