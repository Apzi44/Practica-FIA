class Nodo:
    def __init__(self, coordenada, padre=None):
        self.posicion = (coordenada[0], coordenada[1])
        self.padre = padre
        self.hijos = []
        self.nivel = 0 if padre is None else padre.nivel + 1

class Arbol:
    def __init__(self, nodoInicio):
        self.raiz = nodoInicio

    # def busqueda_anchura_recursiva(self, mapa: Mapa):
    #     visitados = set()
    #     visitados.add((self.raiz.coordenada.coordenadaX, self.raiz.coordenada.coordenadaY))
    #     nivel_actual=[self.raiz]
    #     return self.busqueda_anchura_recursiva_aux(nivel_actual, visitados, mapa)
    
    # def busqueda_anchura_recursiva_aux(self, nivel_actual,visitados, mapa: Mapa):

    #     if not nivel_actual:
    #         return None

    #     siguiente_nivel = []
    #     for nodo in nivel_actual:
    #         if self.comparar_nodos(nodo.coordenada, self.fin):
    #             return self.reconstruir_camino(nodo)
            
    #         x, y = nodo.coordenada.coordenadaX, nodo.coordenada.coordenadaY
    #         posibles_vecinos = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

    #         for vx, vy in posibles_vecinos:
    #             if (0 <= vx < mapa.ancho and 0 <= vy < mapa.alto and
    #                     (vx, vy) not in visitados):
                    
    #                 coordenada_vecina = mapa.obtenerCoordenada(vx, vy)
                    
    #                 if coordenada_vecina.avanzable:
    #                     visitados.add((vx, vy))
    #                     nuevo_nodo = Nodo(coordenada_vecina, padre=nodo)
    #                     siguiente_nivel.append(nuevo_nodo)
    #     return self._busqueda_anchura_recursiva_aux(siguiente_nivel, visitados, mapa)
    # def reconstruir_camino(self, nodo_final):
    #     camino = deque()
    #     nodo_actual = nodo_final
    #     while nodo_actual is not None:
    #         camino.appendleft(nodo_actual.coordenada)
    #         nodo_actual = nodo_actual.padre
    #     return list(camino)

    def agregar_hijo(self, nodo_padre, nuevo_nodo):
        nodo_padre.hijos.append(nuevo_nodo)
    
    def imprimirArbol(self):
        def imprimir_nodo(nodo, nivel):
            print(' ' * nivel * 4 + f'Nivel {nivel}: Posición {nodo.posicion}')
            for hijo in nodo.hijos:
                imprimir_nodo(hijo, nivel + 1)
        imprimir_nodo(self.raiz, 0)