class Nodo:
    def __init__(self, coordenada, padre=None):
        self.posicion = (coordenada[0], coordenada[1])
        self.padre = padre
        self.hijos = []
        self.nivel = 0 if padre is None else padre.nivel + 1

class Arbol:
    def __init__(self, nodoInicio):
        self.raiz = nodoInicio

    def agregar_hijo(self, nodo_padre, nuevo_nodo):
        nodo_padre.hijos.append(nuevo_nodo)
    
    def imprimirArbol(self):
        def imprimir_nodo(nodo, nivel):
            print(' ' * nivel * 4 + f'Nivel {nivel}: Posición {nodo.posicion}')
            for hijo in nodo.hijos:
                imprimir_nodo(hijo, nivel + 1)
        imprimir_nodo(self.raiz, 0)