# arbol.py
from agente import casillaCosto

class Nodo:
    def __init__(self, coordenada, padre=None):
        self.coordenada = coordenada
        self.padre = padre
        self.hijos = []

    def __repr__(self):
        return f"Nodo({self.coordenada.x}, {self.coordenada.y})"

class Arbol:
    def __init__(self, raiz):
        self.raiz = raiz
        self.visitados = set()

    def agregar_hijo(self, nodo_padre, coordenada):
        nuevo_nodo = Nodo(coordenada, padre=nodo_padre)
        nodo_padre.hijos.append(nuevo_nodo)
        return nuevo_nodo

    def generar_vecinos(self, mapa, nodo_actual):
        x, y = nodo_actual.coordenada.x, nodo_actual.coordenada.y
        vecinos = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

        for posx, posy in vecinos:
            if 0 <= posx < mapa.ancho and 0 <= posy < mapa.alto:
                coord = mapa.obtenerCoordenada(posx, posy)
                if coord.avanzable and not coord.visitado:
                    hijo = self.agregar_hijo(nodo_actual, coord)
                    yield hijo

    # def dfs(self, mapa, nodo_actual, meta):
    #     coord = nodo_actual.coordenada
    #     if (coord.x, coord.y) in self.visitados:
    #         return None

    #     self.visitados.add((coord.x, coord.y))
    #     coord.visitado = True

    #     if coord == meta:
    #         return nodo_actual

    #     for hijo in self.generar_vecinos(mapa, nodo_actual):
    #         resultado = self.dfs(mapa, hijo, meta)
    #         if resultado:
    #             return resultado
    #     return None

    # def obtener_camino(self, nodo_final):
    #     camino = []
    #     actual = nodo_final
    #     while actual:
    #         camino.append((actual.coordenada.x, actual.coordenada.y))
    #         actual = actual.padre
    #     return list(reversed(camino))
