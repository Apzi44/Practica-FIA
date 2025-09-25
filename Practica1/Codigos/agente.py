import mapa
import numpy as np
from abc import ABC, abstractmethod
from Coordenada import Coordenada
from tkinter import messagebox

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
    
    def calcularCosto(self, terreno, tipoAgente, tipoMapa="Mixto"):
        if tipoMapa == "Binario":
            if terreno == 0:
                return np.inf
            else:
                return 1

        if tipoMapa == "Mixto":
            if tipoAgente == "Humano":
                if terreno == 0: # Montaña
                    return np.inf
                if terreno == 1: # Agua
                    return 2
                elif terreno == 2: # Bosque
                    return 4
                elif terreno == 3: # Arena
                    return 3
                elif terreno == 4: # Tierra
                    return 1
                elif terreno == 5: # Pantano
                    return 5
                elif terreno == 6: # Nieve
                    return 5
            elif tipoAgente == "Mono":
                if terreno == 0: # Montaña
                    return np.inf
                if terreno == 1: # Agua
                    return 4
                elif terreno == 2: # Bosque
                    return 1
                elif terreno == 3: # Arena
                    return 3
                elif terreno == 4: # Tierra
                    return 2
                elif terreno == 5: # Pantano
                    return 5
                elif terreno == 6: # Nieve
                    return np.inf
            elif tipoAgente == "Pulpo":
                if terreno == 0: # Montaña
                    return np.inf
                if terreno == 1: # Agua
                    return 1
                elif terreno == 2: # Bosque
                    return 3
                elif terreno == 3: # Arena
                    return np.inf
                elif terreno == 4: # Tierra
                    return 2
                elif terreno == 5: # Pantano
                    return 2
                elif terreno == 6: # Nieve
                    return np.inf
            elif tipoAgente == "Pie grande":
                if terreno == 0: # Montaña
                    return 15
                if terreno == 1:  # Agua
                    return np.inf
                elif terreno == 2: # Bosque
                    return 4
                elif terreno == 3: # Arena
                    return np.inf
                elif terreno == 4: # Tierra
                    return 4
                elif terreno == 5: # Pantano
                    return 5
                elif terreno == 6: # Nieve
                    return 3
            elif tipoAgente == "SuperSayayin":
                if terreno == 0 or terreno == 1 or terreno == 2 or terreno == 3 or terreno == 4 or terreno == 5 or terreno == 6:
                    return 1

    def analizarCoordenadasAlrededor(self, x, y):
        if self.direccion == 1 or self.direccion == 3:
            if x+1 < self.mapa.ancho:
                coordenadaAnalizar: Coordenada = self.mapa.obtenerCoordenada(x+1, y)
                if coordenadaAnalizar.visible == True and coordenadaAnalizar.avanzable == True: return 1
            if x-1 >= 0:
                coordenadaAnalizar: Coordenada = self.mapa.obtenerCoordenada(x-1, y)
                if coordenadaAnalizar.visible == True and coordenadaAnalizar.avanzable == True: return 1
        if self.direccion == 2 or self.direccion == 4:
            if y+1 < self.mapa.alto:
                coordenadaAnalizar: Coordenada = self.mapa.obtenerCoordenada(x, y+1)
                if coordenadaAnalizar.visible == True and coordenadaAnalizar.avanzable == True: return 1
            if y-1 >= 0:
                coordenadaAnalizar: Coordenada = self.mapa.obtenerCoordenada(x, y-1)
                if coordenadaAnalizar.visible == True and coordenadaAnalizar.avanzable == True: return 1
        return 0

    @abstractmethod
    def actualizarVision(self):
        pass

class casillaCosto:
    def __init__(self, x, y, costo, avanzable):
        self.x = x
        self.y = y
        self.costo = costo
        self.avanzable = avanzable

class AgenteP(Agente):
    def __init__(self, tipo, mapa, pos_x=0, pos_y=0):
        super().__init__(tipo, mapa, pos_x, pos_y)
        self.inicializarPosicion()

    def moverUbicacion(self):
        if not self.listaOpcionesMovimiento:
            messagebox.showinfo("Error", "No hay opciones de movimiento disponibles")
            return

        coordenadaActual: Coordenada = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
        # Obtener la última opción de movimiento
        opcionMovimiento = self.listaOpcionesMovimiento[-1]
        
        if opcionMovimiento.costo != np.inf:
            # Se cambia el punto actual de la coordenada anterior a falso
            coordenadaActual.puntoActual = False
            # Actualizar posición del agente
            self.posicion_x = opcionMovimiento.x
            self.posicion_y = opcionMovimiento.y
            # Obtener la nueva coordenada y actualizar
            coordenadaNueva = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
            self.coste += opcionMovimiento.costo
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
        # Si hay mas de una coordenada visible alrededor se marca como punto de decision
        if self.analizarCoordenadasAlrededor(self.posicion_x, self.posicion_y) == 1:
            coordenadaActual.puntoDecision = True
        # Obtener la casilla de vision segun la direccion
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

        # Si la casilla de vision esta dentro del mapa 
        coordenada: Coordenada = self.mapa.obtenerCoordenada(x,y)
        if coordenada.visible == True: 
            casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable)
            self.listaOpcionesMovimiento.append(casillaCostoNueva)
        else:
            coordenada.visible = True
            coordenada.costoViaje = self.calcularCosto(coordenada.valor, self.tipo, self.mapa.tipoMapa)
            casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable)
            self.listaOpcionesMovimiento.append(casillaCostoNueva)

class AgenteAxel(AgenteP):
    def __init__(self, tipo, mapa, pos_x=0, pos_y=0):
        super().__init__(tipo, mapa, pos_x, pos_y)
        self.inicializarPosicion()

    def rotarIzquierda(self):
        if self.direccion > 1:
            self.direccion -= 1
        else:
            self.direccion = 4
        self.actualizarVision()

class AgenteAbad(Agente):
    def __init__(self, tipo, mapa, pos_x=0, pos_y=0):
        super().__init__(tipo, mapa, pos_x, pos_y)
        self.inicializarPosicion()

    def moverUbicacion(self, direccion):
        print("ando moviendo")
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

        if self.analizarCoordenadasAlrededor(self.posicion_x, self.posicion_y) == 1:
            coordenadaActual.puntoDecision = True

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
                if coordenada.visible == True:
                    casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable)
                    self.listaOpcionesMovimiento.append(casillaCostoNueva)
                else:
                    coordenada.visible = True
                    coordenada.costoViaje = self.calcularCosto(coordenada.valor, self.tipo)
                    casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable)
                    self.listaOpcionesMovimiento.append(casillaCostoNueva)