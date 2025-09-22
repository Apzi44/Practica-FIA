import Mapa
import numpy as np
from abc import ABC, abstractmethod
from Coordenada import Coordenada
from tkinter import filedialog, messagebox

class Agente(ABC):
    def __init__(self, tipo, mapa, pos_x=0, pos_y=0):
        self.tipo = tipo
        self.posicion_x = pos_x
        self.posicion_y = pos_y
        self.mapa = mapa
        self.direccion = 1
        self.coste = 0
        self.listaOpcionesMovimiento = list()

    def inicializarPosicion(self):
        coordenadaInicial: Coordenada = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
        coordenadaInicial.visitado = True
        coordenadaInicial.puntoActual = True
        coordenadaInicial.visible = True
        coordenadaInicial.costoViaje = self.calcularCosto(coordenadaInicial.valor, self.tipo)
        self.coste += coordenadaInicial.costoViaje
        self.actualizarVision()
    
    def calcularCosto(self, terreno, tipoAgente):
        if tipoAgente == 1:
            if terreno == 0:
                return 1
            if terreno == 1:
                return 1
            elif terreno == 2:
                return 2
            elif terreno == 3:
                return 5
            elif terreno == 4:
                return 1
        elif tipoAgente == 2:
            if terreno == 1:
                return 2
            elif terreno == 2:
                return 1
            elif terreno == 3:
                return 2
            elif terreno == 4:
                return 5
        elif tipoAgente == 3:
            if terreno == 1:
                return 1
            elif terreno == 2:
                return 5
            elif terreno == 3:
                return 1
            elif terreno == 4:
                return 2

        pass


    @abstractmethod
    def actualizarVision(self):
        pass

class casillaCosto:
    def __init__(self, x, y, costo, avanzable):
        self.x = x
        self.y = y
        self.costo = costo
        self.avanzable = avanzable

class Agente1(Agente):
    def __init__(self, tipo, mapa, pos_x=0, pos_y=0):
        super().__init__(tipo, mapa, pos_x, pos_y)
        self.inicializarPosicion()

    def moverUbicacion(self):
        if not self.listaOpcionesMovimiento:
            messagebox.showinfo("Error", "No hay opciones de movimiento disponibles")
            return
            
        coordenadaActual: Coordenada = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
        # Obtener la última opción de movimiento
        ultimaOpcion = self.listaOpcionesMovimiento[-1]
        
        if ultimaOpcion.avanzable == True:
            # Se cambia el punto actual de la coordenada anterior a falso
            coordenadaActual.puntoActual = False
            
            # Actualizar posición del agente
            self.posicion_x = ultimaOpcion.x
            self.posicion_y = ultimaOpcion.y

            # Obtener la nueva coordenada y actualizar
            coordenadaNueva = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
            self.coste += ultimaOpcion.costo
            coordenadaNueva.visitado = True
            coordenadaNueva.puntoActual = True
            self.listaOpcionesMovimiento.clear()
            self.actualizarVision()
        else:
            messagebox.showinfo("Error", f"Movimiento no válido, estas fuera del mapa o en una barrera")

    def rotarDerecha(self):
        if self.direccion < 4:
            self.direccion += 1
        else:
            self.direccion = 1
        self.actualizarVision()

    def actualizarVision(self):
        coordenadaActual: Coordenada = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)

        if self.direccion == 1 or self.direccion == 3:
            x = self.posicion_x
            y = self.posicion_y - 1 if self.direccion == 1 else self.posicion_y + 1
        if self.direccion == 2 or self.direccion == 4:
            x = self.posicion_x + 1 if self.direccion == 2 else self.posicion_x - 1
            y = self.posicion_y

        # Si la casilla de vision esta fuera se añade a la lista pero se indica que no es avanzable y con coste infinito
        if (x<0) or (y<0) or (x>=self.mapa.ancho) or (y>=self.mapa.alto):
            casillaCostoNueva = casillaCosto(x,y, np.inf, False)
            self.listaOpcionesMovimiento.append(casillaCostoNueva)
            return
        
        # Si la casilla de vision esta dentro del mapa se actualiza su visibilidad y coste
        coordenada: Coordenada = self.mapa.obtenerCoordenada(x,y)
        if coordenada.visible == False:
            coordenada.visible = True
            coordenada.costoViaje = self.calcularCosto(coordenada.valor, self.tipo)
            casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable)
            self.listaOpcionesMovimiento.append(casillaCostoNueva)

        if len(self.listaOpcionesMovimiento) > 1:
            coordenadaActual.puntoDecision = True

class Agente2(Agente):
    def moverUbicacion(self):
        # Implementar lógica de movimiento para Agente2
        pass

    def actualizarVision(self):
        # Implementar lógica de actualización de visión para Agente2
        pass

class Agente3(Agente):
    def __init__(self, tipo, mapa, pos_x=0, pos_y=0):
        super().__init__(tipo, mapa, pos_x, pos_y)
        self.inicializarPosicion()

    def moverUbicacion(self, direccion):
        if not self.listaOpcionesMovimiento:
            messagebox.showinfo("Error", "No hay opciones de movimiento disponibles")
            return
        coordenadaActual: Coordenada = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)

        # Obtener la opcion de enfrente
        if direccion == 'frente':
            coordCost = self.listaOpcionesMovimiento[2]
        if direccion == 'atras':
            coordCost = self.listaOpcionesMovimiento[3]
        if direccion == 'izquierda':
            coordCost = self.listaOpcionesMovimiento[0]
        if direccion == 'derecha':
            coordCost = self.listaOpcionesMovimiento[1]
        
        if coordCost.avanzable == True:
            # Se cambia el punto actual de la coordenada anterior a falso
            coordenadaActual.puntoActual = False       
            # Actualizar posición del agente
            self.posicion_x = coordCost.x
            self.posicion_y = coordCost.y

            # Obtener la nueva coordenada y actualizar
            coordenadaNueva = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
            self.coste += coordCost.costo
            coordenadaNueva.visitado = True
            coordenadaNueva.puntoActual = True
            self.listaOpcionesMovimiento.clear()
            self.actualizarVision()
        else:
            messagebox.showinfo("Error", f"Movimiento no válido, estas fuera del mapa o en una barrera")

    def actualizarVision(self):
        coordenadaActual: Coordenada = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
        xActual = self.posicion_x
        yActual = self.posicion_y

        coordenadasIzquierda = (xActual - 1, yActual)
        coordenadasDerecha = (xActual + 1, yActual)
        coordenadasFrente = (xActual, yActual - 1)
        coordenadasAtras = (xActual, yActual + 1)

        for coord in [coordenadasIzquierda, coordenadasDerecha, coordenadasFrente, coordenadasAtras]:
            x, y = coord
            if (x<0) or (y<0) or (x>=self.mapa.ancho) or (y>=self.mapa.alto):
                casillaCostoNueva = casillaCosto(x,y, np.inf, False)
                self.listaOpcionesMovimiento.append(casillaCostoNueva)
            else:
                coordenada: Coordenada = self.mapa.obtenerCoordenada(x,y)
                if coordenada.visible == False:
                    coordenada.visible = True
                    coordenada.costoViaje = self.calcularCosto(coordenada.valor, self.tipo)
                    casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable)
                    self.listaOpcionesMovimiento.append(casillaCostoNueva)
        if len(self.listaOpcionesMovimiento) > 1:
            coordenadaActual.puntoDecision = True