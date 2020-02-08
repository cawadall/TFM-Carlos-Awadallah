# Estudio Carga Computacional PiBot en Ejecución Real

Este estudio consistirá en diversas pruebas para medir el rendimiento computacional de la Raspberry Pi.
Estas pruebas constarán en la ejecución de diversos programas.

**Nota:** Los resultados son valores aproximados, ya que los valores son cambiantes en cada instante.

## Prueba 1

* Durante esta prueba, el robot únicamente avanzará hacia adelante.
* Solamente se encuentran en funcionamiento ambos servomotores.

### Código de la prueba:

```
try:

    robot = PiBot()
    if __name__ == "__main__":
        while(True):

            robot.avanzar(0.8)
            time.sleep(0.2)

except KeyboardInterrupt:
    robot.parar()
    pass
```

### Resultados:

2.5% de uso medio de CPU.

## Prueba 2

* El robot avanza hacia adelante y hacia atrás alternativamente.
* Sólo se encuentran en funcionamiento los servomotores.

### Código de la Prueba:

```
try:

    robot = PiBot()
    if __name__ == "__main__":
        while(True):

            robot.avanzar(0.08)
            time.sleep(2)
            robot.retroceder(0.08)
            time.sleep(2)

except KeyboardInterrupt:
    robot.parar()
    pass
```

### Resultados:

2.5% de uso medio de CPU.

## Prueba 3
* Obtención de distancias mediante sensor de ultrasonidos.
* Únicamente estará activo el sensor de ultrasonidos.

### Código de la Prueba:

```
try:

    robot = PiBot()
    if __name__ == "__main__":
        while(True):

            us = robot.leerUltrasonido()
            time.sleep(0.2)

except KeyboardInterrupt:
    robot.parar()
    pass
```

### Resultados:

3.5% de uso medio de CPU.

## Prueba 4

* Ejecución del ejercicio Choca-Gira.
* En funcionamiento motores y sensor de ultrasonidos.

### Código de la Prueba:

```
try:
    Pi = 3.14
    robot = PiBot()
    if __name__ == "__main__":
        while(True):

            us = robot.leerUltrasonido()

            if(us >= 0.15):
                robot.avanzar(0.5)
            else:
                #Retrocedo
                robot.retroceder(0.5)
                time.sleep(1.2)
                #Giro
                robot.girarIzquierda(Pi / 4)
                time.sleep(2)

                robot.parar()

            time.sleep(0.2)

except KeyboardInterrupt:
    robot.parar()
    pass
```

### Resultados:
3.75% de uso medio de CPU. Ningún núcleo excede los 13.0% de uso.

## Prueba 5

* Ejecución del ejercicio Sigue Pelota.
* En funcionamiento cámara y motores.

### Código de la Prueba:

```
robot = PiBot()
#Constantes:
Pi = 3.14
XPixels = 160 #400
Centro = XPixels / 2
AreaMax = 1000 #1000

while True:
    centro, area = robot.dameObjeto()
    if(centro != None):
        if(centro[0] > (XPixels / 3) and centro[0] < (XPixels * 2 / 3)):
            if(area < AreaMax):
                robot.avanzar(0.5)
            else:
                robot.retroceder(0.5)
        elif(centro[0] < (XPixels / 3)):
            robot.girarIzquierda(Pi / 4)
        else:
            robot.girarDerecha(Pi / 4)
    else:
        robot.parar()
    time.sleep(0.005)
```

### Resultados:
20% de uso medio de CPU. Ningún núcleo excede de los 55% de uso.

## Prueba 6

* Ejecución de un ejercicio que se trata de seguir la pelota usando la cámara y los motores y a la vez de leer distancias con el sensor de ultrasonidos.
* En funcionamiento, cámara, motores y sensor de ultrasonidos.

### Código de la Prueba:

```
robot = PiBot()
#Constantes:
Pi = 3.14
XPixels = 160 #400
Centro = XPixels / 2
AreaMax = 1000 #1000

while True:
    centro, area = robot.dameObjeto()
    us = robot.leerUltrasonido()
    if(centro != None):
        if(centro[0] > (XPixels / 3) and centro[0] < (XPixels * 2 / 3)):
            if(area < AreaMax):
                robot.avanzar(0.5)
            else:
                robot.retroceder(0.5)
        elif(centro[0] < (XPixels / 3)):
            robot.girarIzquierda(Pi / 4)
        else:
            robot.girarDerecha(Pi / 4)
    else:
        robot.parar()
    time.sleep(0.005)
```

### Resultados:
25% de uso medio de CPU. Ningún núcleo excede el 60% de uso.
