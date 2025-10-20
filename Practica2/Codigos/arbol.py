class Nodo:
    def __init__(self, coordenada, padre=None):
        self.posicion = (coordenada[0], coordenada[1])
        self.padre = padre
        self.hijos = []
        self.nivel = 0 if padre is None else padre.nivel + 1
        costo = 0

class Arbol:
    def __init__(self, nodoInicio):
        self.raiz = nodoInicio

    def agregar_hijo(self, nodo_padre, nuevo_nodo):
        nodo_padre.hijos.append(nuevo_nodo)
    
    def imprimir_arbol(self, nodo=None, prefijo="", es_ultimo=True):
        if nodo is None:
            nodo = self.raiz
        print(prefijo, "`- " if es_ultimo else "|- ", nodo.posicion, sep="")
        nuevo_prefijo = prefijo + ("   " if es_ultimo else "|  ")
        hijos_count = len(nodo.hijos)
        for i, hijo in enumerate(nodo.hijos):
            es_ultimo_hijo = (i == hijos_count - 1)
            self.imprimir_arbol(hijo, nuevo_prefijo, es_ultimo_hijo) 