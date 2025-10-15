import numpy as np
from numpy import isinf
from abc import ABC, abstractmethod
from Coordenada import Coordenada
from tkinter import messagebox
from arbol import Arbol as arbol, Nodo as nodo

class Agente(ABC):
    def __init__(self, tipo, mapa, pos_x=0, pos_y=0):
        self.tipo = tipo
        self.posicion_x = pos_x
        self.posicion_y = pos_y
        self.mapa = mapa
        self.direccion = 1
        self.coste = 0
        self.listaOpcionesMovimiento = list()
        self.noMovimientos= 0

    def inicializarPosicion(self):
        coordenadaInicial: Coordenada = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
        coordenadaInicial.visitado = True
        coordenadaInicial.puntoActual = True
        coordenadaInicial.visible = True
        coordenadaInicial.costoViaje = self.calcularCosto(coordenadaInicial.valor, self.tipo)
        self.coste += 0
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
        conteo = 0
        conexiones = 0
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # derecha, izquierda, abajo, arriba
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.mapa.ancho and 0 <= ny < self.mapa.alto:
                coord = self.mapa.obtenerCoordenada(nx, ny)
                if coord.visible:
                    if coord.avanzable:
                        conexiones += 1
                        if not isinf(coord.costoViaje):
                            conteo += 1
        if conteo > 2 and conexiones > 2:
            return 1
        return 0

    @abstractmethod
    def actualizarVision(self):
        pass

class casillaCosto:
    def __init__(self, x, y, costo, avanzable, visitado):
        self.x = x
        self.y = y
        self.costo = costo
        self.avanzable = avanzable
        self.visitado = visitado

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
        opcionMovimiento = self.listaOpcionesMovimiento[0]
        
        if opcionMovimiento.costo != np.inf:
            if opcionMovimiento.visitado == True:
                messagebox.showinfo("Error", f"Movimiento no válido, ya has visitado esa casilla")
                return
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
            self.actualizarVision()
            self.noMovimientos += 1
        else:
            messagebox.showinfo("Error", f"Movimiento no válido, estas fuera del mapa o en una barrera")

    def rotarDerecha(self):
        if self.direccion < 4:
            self.direccion += 1
        else:
            self.direccion = 1
        self.actualizarVision()

    def actualizarVision(self):
        self.listaOpcionesMovimiento.clear()
        coordenadaActual: Coordenada = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
        # Obtener la casilla de vision segun la direccion
        if self.direccion == 1 or self.direccion == 3:
            x = self.posicion_x
            y = self.posicion_y - 1 if self.direccion == 1 else self.posicion_y + 1
        if self.direccion == 2 or self.direccion == 4:
            x = self.posicion_x + 1 if self.direccion == 2 else self.posicion_x - 1
            y = self.posicion_y

        # Si la casilla de vision esta fuera se añade a la lista pero se indica que no es avanzable y con coste infinito
        if (x<0) or (y<0) or (x>=self.mapa.ancho) or (y>=self.mapa.alto):
            casillaCostoNueva = casillaCosto(x,y, np.inf, False, False)
            self.listaOpcionesMovimiento.append(casillaCostoNueva)
            return

        # Si la casilla de vision esta dentro del mapa 
        coordenada: Coordenada = self.mapa.obtenerCoordenada(x,y)
        if coordenada.visible == True: 
            casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable, coordenada.visitado)
            self.listaOpcionesMovimiento.append(casillaCostoNueva)
        else:
            coordenada.visible = True
            coordenada.costoViaje = self.calcularCosto(coordenada.valor, self.tipo, self.mapa.tipoMapa)
            casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable, coordenada.visitado)
            self.listaOpcionesMovimiento.append(casillaCostoNueva)
                    # Si hay mas de una coordenada visible alrededor se marca como punto de decision
            if self.analizarCoordenadasAlrededor(self.posicion_x, self.posicion_y) == 1:
                coordenadaActual.puntoDecision = True

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
        
        if coordCost.costo != np.inf:
            if coordCost.visitado == True:
                messagebox.showinfo("Error", f"Movimiento no válido, ya has visitado esa casilla")
                return
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
            self.noMovimientos+=1
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
                casillaCostoNueva = casillaCosto(x,y, np.inf, False, False)
                self.listaOpcionesMovimiento.append(casillaCostoNueva)
            else:
                coordenada: Coordenada = self.mapa.obtenerCoordenada(x,y)
                if coordenada.visible == True:
                    casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable, coordenada.visitado)
                    self.listaOpcionesMovimiento.append(casillaCostoNueva)
                else:
                    coordenada.visible = True
                    coordenada.costoViaje = self.calcularCosto(coordenada.valor, self.tipo)
                    casillaCostoNueva = casillaCosto(x,y, coordenada.costoViaje, coordenada.avanzable, coordenada.visitado)
                    self.listaOpcionesMovimiento.append(casillaCostoNueva)
                    if self.analizarCoordenadasAlrededor(self.posicion_x, self.posicion_y) == 1:
                        coordenadaActual.puntoDecision = True

    def busquedaProfundidadPaso(self, objetivo_x, objetivo_y):
        inicio = nodo((self.posicion_x, self.posicion_y), padre=None)
        self.arbolBusqueda = arbol(inicio)
        resultado = self.dfs(objetivo_x, objetivo_y, inicio)
        if resultado:
            print("Ruta a seguir:")
            print("Objetivo encontrado")
            self.arbolBusqueda.imprimirArbol()
        else:
            print("No se ha encontrado el objetivo")

    def retroceder(self, nodoActual:nodo):
        coordenadaActual = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
        coordenadaActual.puntoActual = False
        self.posicion_x = nodoActual.posicion[0]
        self.posicion_y = nodoActual.posicion[1]
        coordenadaNueva = self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y)
        coordenadaNueva.puntoActual = True
        self.listaOpcionesMovimiento.clear()
        self.actualizarVision()
    
    def dfs(self, objetivo_x, objetivo_y, nodoActual: nodo):
        pilaBusqueda = [nodoActual]
        while pilaBusqueda:
            if nodoActual.posicion[0] == objetivo_x and nodoActual.posicion[1] == objetivo_y:
                return pilaBusqueda

            direccion_map= {0: 'izquierda', 1: 'derecha', 2: 'frente', 3: 'atras'}
            sinSalidas = all(hijo.costo == np.inf or hijo.visitado for hijo in self.listaOpcionesMovimiento)
            #Bloque sin salida
            if sinSalidas:
                # Marcar la casilla como punto clave de bloqueo
                self.mapa.obtenerCoordenada(nodoActual.posicion[0], nodoActual.posicion[1]).puntoClave = 'H'
                # Si no hay mas nodos en la pila de decision se retorna None
                if nodoActual.padre is None: return None
                # Si hay mas nodos en la pila de decision se retrocede al padre
                pilaBusqueda.pop()
                nodoActual = nodoActual.padre
                self.retroceder(nodoActual)
                continue

            # Explorar hijos
            for idx, hijo in enumerate(self.listaOpcionesMovimiento):
                if hijo.avanzable and not hijo.visitado and hijo.costo != np.inf:
                    nodoHijo = nodo((hijo.x, hijo.y), padre=nodoActual)
                    self.arbolBusqueda.agregar_hijo(nodoActual, nodoHijo)
                    direccion = direccion_map[idx]
                    self.moverUbicacion(direccion)
                    pilaBusqueda.append(nodoHijo)
                    nodoActual = nodoHijo
                    break

    def busquedaProfundidadDecision(self, objetivo_x, objetivo_y):
        inicio= nodo((self.posicion_x, self.posicion_y), padre=None)
        self.arbolDecision = arbol(inicio)
        if self.posicion_x == objetivo_x and self.posicion_y == objetivo_y:
            print("Objetivo encontrado")
        else:
            resultado = self.dfs_decision(objetivo_x, objetivo_y, inicio)
            if resultado:
                print("Objetivo encontrado")
            else:
                print("No se ha encontrado el objetivo")

    def movimientoRapido(self, direccion, objetivo_x, objetivo_y, pilaDesicion, nodoPadre):
        self.moverUbicacion(direccion)
        # Si se llega al objetivo se añade a la pila de decision y se retorna exito
        if self.posicion_x == objetivo_x and self.posicion_y == objetivo_y: 
            pilaDesicion.append(nodo((self.posicion_x, self.posicion_y), padre=nodoPadre))
            return ("Exito", nodo((self.posicion_x, self.posicion_y), padre=nodoPadre))
        
        # Si no se llega al objetivo se continua hasta encontrar un punto de decision o sin salidas
        while (self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y).puntoDecision == False):
            sinSalidas = all(hijo.costo == np.inf or hijo.visitado for hijo in self.listaOpcionesMovimiento)
            # Bloque sin salida, ya sea porque no hay movimientos o porque ya se han visitado todos los alrededores
            if sinSalidas:
                self.mapa.obtenerCoordenada(self.posicion_x, self.posicion_y).puntoClave = 'H'
                return "Sin Salidas"
            
            # Si hay movimiento, debido a ser movimiento rapido, se mueve a donde se pueda
            for idx,movimiento in enumerate(self.listaOpcionesMovimiento):
                if movimiento.avanzable and not movimiento.visitado and movimiento.costo != np.inf:
                    direccion_map= {0: 'izquierda', 1: 'derecha', 2: 'frente', 3: 'atras'}
                    direccion = direccion_map[idx]
                    self.moverUbicacion(direccion)
                    if self.posicion_x == objetivo_x and self.posicion_y == objetivo_y: 
                        nodoNuevo= nodo((self.posicion_x, self.posicion_y), padre=nodoPadre)
                        pilaDesicion.append(nodoNuevo)
                        return ("Exito", nodoNuevo)
                    break
        # Si se llega a un punto de decision se retorna el nodo actual
        return ("", nodo((self.posicion_x, self.posicion_y), padre=nodoPadre))

    def dfs_decision(self, objetivo_x, objetivo_y, nodoActual):
        pilaDesicion = [nodoActual]
        while pilaDesicion:
            direccion_map= {0: 'izquierda', 1: 'derecha', 2: 'frente', 3: 'atras'}
            #Bloque sin salida
            sinSalidas = all(hijo.costo == np.inf or hijo.visitado for hijo in self.listaOpcionesMovimiento)
            if sinSalidas:
                # Marcar la casilla como punto clave de bloqueo
                self.mapa.obtenerCoordenada(nodoActual.posicion[0], nodoActual.posicion[1]).puntoClave = 'H'
                # Si no hay mas nodos en la pila de decision se retorna None
                if nodoActual.padre is None: return None
                # Si hay mas nodos en la pila de decision se retrocede al padre
                nodoActual = nodoActual.padre
                self.retroceder(nodoActual)
                pilaDesicion.pop()
                continue

            # Explorar hijos
            for idx, hijo in enumerate(self.listaOpcionesMovimiento):
                if hijo.avanzable and not hijo.visitado and hijo.costo != np.inf:
                    direccion = direccion_map[idx]
                    respuesta= self.movimientoRapido(direccion, objetivo_x, objetivo_y, pilaDesicion, nodoActual)
                    if "Exito" in respuesta:
                        self.arbolDecision.agregar_hijo(nodoActual, respuesta[1])
                        return pilaDesicion
                    elif respuesta == "Sin Salidas":
                        self.retroceder(nodoActual)
                    else:
                        nodoHijo = respuesta[1]
                        pilaDesicion.append(nodoHijo)
                        self.arbolDecision.agregar_hijo(nodoActual, nodoHijo)
                        nodoActual = nodoHijo
                        break