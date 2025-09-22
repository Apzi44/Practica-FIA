import Mapa
import numpy as np
from abc import ABC, abstractmethod
from Coordenada import Coordenada

class Agente(ABC):
    def __init__(self, tipo, mapa, pos_x=0, pos_y=0):
        self.__tipo = tipo
        self.__posicion_x = pos_x
        self.__posicion_y = pos_y
        self.__mapa = mapa
        self.__direccion = 1
        self.__coste =0
        self.__valido = False

    @abstractmethod
    def moverUbicacion(self):
        pass

    @abstractmethod
    def actualizarVision(self):
        pass

class casillaCosto:
    def __init__(self, x, y, costo):
        self.x = x
        self.y = y
        self.costo = costo
        self.avanzable

class Agente1(Agente):
    def moverUbicacion(self):
        if self.__direccion == 1 or self.__direccion == 3:
            self.__posicion_y += 1 if self.__direccion == 1 else -1
        if self.__direccion == 2 or self.__direccion == 4:
            self.__posicion_x += 1 if self.__direccion == 2 else -1
        pass


    def rotarDerecha(self):
        if self.__direccion < 4:
            self.__direccion += 1
        else:
            self.__direccion = 1


    def actualizarVision(self):
        if self.__direccion == 1 or self.__direccion == 3:
            x = self.__posicion_x
            y = self.__posicion_y + 1 if self.__direccion == 1 else self.__posicion_y - 1
        if self.__direccion == 2 or self.__direccion == 4:
            x = self.__posicion_x + 1 if self.__direccion == 2 else self.__posicion_x - 1
            y = self.__posicion_y
        
        if (x<0) or (y<0) or (x>=self.__mapa.ancho) or (y>=self.__mapa.alto):
            pass
        coordenada: Coordenada = self.__mapa.obtenerCordenada(x,y)
        if coordenada.visible == False:
            coordenada.visible = True
            coordenada.costoViaje = self.calcularCosto(coordenada.terreno, self.__tipo)
            pass


        
    def calcularCosto(terreno, tipoAgente):
        if tipoAgente == 1:
            if terreno == 'A':
                return 1
            elif terreno == 'B':
                return 2
            elif terreno == 'C':
                return 5
            elif terreno == 'D':
                return np.inf
        elif tipoAgente == 2:
            if terreno == 'A':
                return 2
            elif terreno == 'B':
                return 1
            elif terreno == 'C':
                return 2
            elif terreno == 'D':
                return 5
        elif tipoAgente == 3:
            if terreno == 'A':
                return np.inf
            elif terreno == 'B':
                return 5
            elif terreno == 'C':
                return 1
            elif terreno == 'D':
                return 2


class Agente2(Agente):
    def moverUbicacion(self):
        # Implementar lógica de movimiento para Agente2
        pass

    def actualizarVision(self):
        # Implementar lógica de actualización de visión para Agente2
        pass

class Agente3(Agente):
    def moverUbicacion(self):
        # Implementar lógica de movimiento para Agente3
        pass

    def actualizarVision(self):
        # Implementar lógica de actualización de visión para Agente3
        pass