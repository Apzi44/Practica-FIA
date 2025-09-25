import re
from tkinter import messagebox
import numpy as np
from excepciones import excepcionProcesadoValores, extensionInvalida, formatoInvalidoArchivo
from Coordenada import Coordenada

class Mapa:
    def __init__(self):
        self.matriz = list()
        self.alto = 0
        self.ancho = 0
        self.tipoMapa = None
    # LECTURA Y PROCESAMIENTO DE ARCHIVO
    def leerArchivo(self, nombreArchivo):
        try:
            matrizAuxiliar = list()
            with open(nombreArchivo, 'r', encoding="utf-8-sig") as archivo:
                for iteracion, linea in enumerate(archivo):
                    lineaProcesada= self.__procesarLinea(linea)
                    self.__validarDimensiones(iteracion, len(lineaProcesada), len(matrizAuxiliar[iteracion-1]) if iteracion>0 else 0)
                    matrizAuxiliar.append(lineaProcesada)
            if len(matrizAuxiliar) ==0:
                raise formatoInvalidoArchivo(1)
            if len(matrizAuxiliar) <4:
                raise formatoInvalidoArchivo(2)
            self.__cargaDatos(matrizAuxiliar)
            self.__determinarTipoMapa()
            self.__configurarBarreras()
            matrizAuxiliar.clear()
    
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo no fue encontrado, por favor verifique la ruta del archivo")
            return False
        except formatoInvalidoArchivo as e:
            messagebox.showerror("Error", str(e))
            return False
        except extensionInvalida as e:
            messagebox.showerror("Error", str(e))
            return False
        except excepcionProcesadoValores as e:
            messagebox.showerror("Error", str(e))
            return False
        except Exception:
            messagebox.showerror("Error", "Algo salio mal al cargar el archivo")
            return False
        else:
            return True

    def __procesarLinea(self, linea):
        # Eliminacion de espacios en blanco y caracteres de la linea
        linea = linea.strip()
        # Se quitan comas al final de la linea si es el caso
        linea = self.__quitarComas(linea)
        # Busqueda el tipo de linea
        tipo = self.__buscartipoCoincidencia(linea)

        if tipo == "ninguno":
            raise formatoInvalidoArchivo(3.1)
        else:
            return linea.split(',')
    
    def __quitarComas(self, linea):
        if linea[-1] == ',':
            linea = linea[:-1]
        if linea[-1:-2] == ',,':
            linea = linea[:-2]
        return linea

    def __buscartipoCoincidencia(self, linea):
        patronBase= r"([a-zA-Z0-9]+(?:,[a-zA-Z0-9]+){2,})"
        if re.fullmatch(patronBase, linea):
            return "base"
        else:
            return "ninguno"

    def __validarDimensiones(self, iteracion, largoLinea, largoLineaAnterior):
        if iteracion > 0 and largoLinea != largoLineaAnterior:
                raise extensionInvalida(1)

    def __cargaDatos(self, matrizAuxiliar):
        for y in range(len(matrizAuxiliar)):
                listaAuxiliar= list()
                for x in range(len(matrizAuxiliar[y])):
                    if matrizAuxiliar[y][x].isdigit(): 
                        listaAuxiliar.append(Coordenada(int(matrizAuxiliar[y][x]), x, y))
                    else: 
                        raise excepcionProcesadoValores()
                self.matriz.append(listaAuxiliar)
        self.alto= len(matrizAuxiliar)
        self.ancho= len(matrizAuxiliar[0])

    def __determinarTipoMapa(self):
        tipos = set()
        for fila in self.matriz:
            for coordenada in fila:
                tipos.add(coordenada.valor)
        if len(tipos) == 2 and tipos.issubset({0, 1}):
            self.tipoMapa = "Binario"
        elif len(tipos) <= 7 and tipos.issubset({0, 1, 2, 3, 4, 5, 6}):
            self.tipoMapa = "Mixto"
        else:
            raise formatoInvalidoArchivo(4)

    def __configurarBarreras(self):
        if self.tipoMapa == "Binario":
            for fila in self.matriz:
                for coordenada in fila:
                    if coordenada.valor == 0:
                        coordenada.avanzable = False
                    else:
                        coordenada.avanzable = True
        else:
            for fila in self.matriz:
                for coordenada in fila:
                    if coordenada.valor == 4:
                        coordenada.avanzable = True

    # FUNCIONES DE CONSULTA DE COORDENADAS
    def obtenerCoordenada(self, x, y):
        if (x<0) or (y<0) or (x>=self.ancho) or (y>=self.alto):
            raise IndexError()
        return self.matriz[y][x]

    # CREACION DE MATRICES PARA ALGORITMOS Y VISUALIZACION
    def crearMatrizTerreno(self):
        return np.array([[coordenada.valor if coordenada.visible else -1 for coordenada in fila] for fila in self.matriz])

    def crearMatrizDatos(self, agente):
        matrizDatos= list()
        for fila in self.matriz:
            listaBase= list()
            for coordenada in fila:
                listaAuxiliar= list()
                textoMatriz= ''
                if coordenada.puntoInicialFinal:
                    listaAuxiliar.append(coordenada.puntoClave)
                if coordenada.visitado:
                    listaAuxiliar.append("V")
                if coordenada.puntoDecision:
                    listaAuxiliar.append("O")
                if coordenada.puntoActual:
                    listaAuxiliar.append("X")
                    if agente:
                        if agente.direccion == 1:
                            listaAuxiliar.append('^')
                        elif agente.direccion == 2:
                            listaAuxiliar.append('>')
                        elif agente.direccion == 3:
                            listaAuxiliar.append('v')
                        elif agente.direccion == 4:
                            listaAuxiliar.append('<')
                                        
                if len(listaAuxiliar)!=0:   textoMatriz= ','.join(listaAuxiliar)
                else : textoMatriz= ''
                listaBase.append(textoMatriz)
            matrizDatos.append(listaBase)
        return np.array(matrizDatos)
    

if __name__ == "__main__":
    documento = Mapa()
