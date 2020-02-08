#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tello import Tello
from math import pi as PI
import math

V_MAX = 1.5 # m/s
W_MAX = PI/2 # rad/s

class Drone:

    def __init__(self, local_ip, local_port):

        self.drone = Tello(local_ip, local_port)
    
    def close(self):
        self.drone.close()
    
    def dame_imagen(self):
        return self.drone.get_image()

    def dame_objeto(self):
        return self.drone.get_object(showImageFiltered=True)

# ------------ EXTRA ------------

    def despegar(self):
        return self.drone.takeoff()

    def aterrizar(self):
        return self.drone.land()

# ------------ CONTROL EN VELOCIDAD ------------

    def to_rc(self, v):
        return math.floor((100 * v) / V_MAX)

    def to_rc_rot(self, w):
        return math.floor((100 * w) / W_MAX)

    # Las 4 funciones: velocidad, avanzar, retroceder y lateral_izquierda
    # son bloqueantes, avanzan hasta una determinada posición y paran
    # y después ejecutan la siguiente instrucción (no hay movimiento contínuo)
    #def velocidad(self, vel):
    #    return self.set_speed(vel)
        
    #def avanzar(self, vel):
    #    self.drone.forward_speed(vel)
    
    #def retroceder(self, vel):
    #    self.drone.backward_speed(vel)

    #def lateral_izquierda(self, vel):
    #    self.drone.left_speed(vel)

    # Modo RadioControl, movimiento constante con rangos de velocidades
    # -100 a 100 (simulando un stick analógico). He hecho pruebas y la velocidad
    # máxima de avance (con vx = 100) es de aprox. 1.5 m/s (igual que si pilotas en la app
    # del móvil) aunque en los foros y la  documentación pone que es máximo 1 m/s.
    # La velocidad máxima teórica del Tello es de 10 m/s pero está capado (hay que tocar el
    # firmware). 
    # Con el API solo se puede ir en modo lento (velocidad max de 1 m/s), y con la app
    # del movil se puede poner el modo rápido que tiene una velocidad maxima de 3 m/s.
    def _rc(self, vy, vx, vz, rot):
        
        self.drone.set_velocities(vy, vx, vz, rot)

    def avanzar(self, vx):
        vx = self.to_rc(vx)
        self._rc(0,vx,0,0)
    
    def retroceder(self, vx):
        vx = self.to_rc(vx)*(-1)
        self._rc(0,vx,0,0)
    
    def lateral_izquierda(self, vy):
        vy = self.to_rc(vy)
        self._rc(vy,0,0,0)
    
    def lateral_derecha(self, vy):
        vy = self.to_rc(vy)*(-1)
        self._rc(vy,0,0,0)
    
    def subir(self, vz):
        vz = self.to_rc(vz)
        self._rc(0,0,vz,0)
    
    def bajar(self, vz):
        vz = self.to_rc(vz)*(-1)
        self._rc(0,0,vz,0)

    def girar_izquierda(self, rot):
        rot = self.to_rc_rot(rot)
        self._rc(0,0,0,rot)
    
    def girar_derecha(self, rot):
        rot = self.to_rc_rot(rot)*(-1)
        self._rc(0,0,0,rot)
    
    def movimiento_libre(self, vx, vy, vz, rot):
        self._rc(self.to_rc(vy), self.to_rc(vx), self.to_rc(vz), self.to_rc_rot(rot))

    def parar(self):
        self.drone.stop()



# ------------ CONTROL EN POSICION ------------

    def girar_derecha_hasta(self, grados):
        return self.drone.rotate_cw(grados)

    #def girar_derecha(self, grados):
    #    return self.rotate_cw(grados)

    def girar_izquierda_hasta(self, grados):
        return self.drone.rotate_ccw(grados)

    #def girar_izquierda(self, grados):
    #    return self.rotate_ccw(grados)

    def retrocecer_hasta(self, distancia):
        return self.drone.move_backward(distancia)

    def bajar_hasta(self, distancia):
        return self.drone.move_down(distancia)

    def avanzar_hasta(self, distancia):
        return self.drone.move_forward(distancia)

    def izquierda_hasta(self, distancia):
        return self.drone.move_left(distancia)

    def derecha_hasta(self, distancia):
        return self.drone.move_right(distancia)

    def subir_hasta(self, distancia):
        return self.drone.move_up(distancia)

# ------ METODOS INFORMATIVOS ------

    def altura_actual(self):
        return self.drone.get_height()

    def bateria_restante(self):
        return self.drone.get_battery()
    
    def tiempo_de_vuelo(self):
        return self.drone.get_flight_time()

    def velocidad_actual(self):
        return self.drone.get_speed()
