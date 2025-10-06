# arbol.py
from agente import casillaCosto
from agente import Agente
from mapa import Coordenada

class Nodo:
    def __init__(self, coordenada, padre=None):
        self.coordenada = coordenada
        self.padre = padre
        self.hijos = []

    def __repr__(self):
        return f"Nodo({self.coordenada.x}, {self.coordenada.y})"

class Arbol:
    def __init__(self, nodoInicio, nodoFinal):
        self.raiz = nodoInicio
        self.fin = nodoFinal
        self.visitados = set()

    def agregar_hijo(self, nodo_padre, coordenada):
        nuevo_nodo = Nodo(coordenada, padre=nodo_padre)
        nodo_padre.hijos.append(nuevo_nodo)
        print("Nodo agregado exitosamente:")
    
    def generar_vecinos(self, agente: Agente):
        vecinos = agente.listaOpcionesMovimiento
        for nodo_hijo in vecinos:
            if nodo_hijo.avanzable and not nodo_hijo.visitado:
                yield nodo_hijo

    def comparar_nodos(self, nodo1, nodo2):
        if nodo1.x == nodo2.x and nodo1.y == nodo2.y:
            return True
        return False

    def busqueda_Profundidad(self):
        listaPrioridad = ["Arriba", "Abajo", "Izquierda", "Derecha"]
        self.visitados= list()
        pilaArbol = [self.raiz]
        while pilaArbol:
            nodo_actual = pilaArbol.pop()
            self.visitados.append(nodo_actual)

            if self.comparar_nodos(nodo_actual, self.fin):
                return listaPrioridad
            for vecino in self.generar_vecinos(nodo_actual):
                if vecino not in self.visitados:             
                    self.visitados.append(vecino)