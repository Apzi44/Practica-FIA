import re
from tkinter import messagebox
import numpy as np
from excepciones import excepcionProcesadoValores, extensionInvalida, formatoInvalidoArchivo

# NOTA: Tienen de chamba adicional ver que atributos volver privados y cuaes publicos

class Coordenada:
    def __init__(self, valor, coordenadaX, coordenadaY):
        self.valor= valor
        self.coordenadaX= coordenadaX
        self.coordenadaY= coordenadaY
        self.visitado= False
        self.puntoDesicion = False
        self.valorAdicional= None
        self.puntoClave = None

    def __str__(self):
        return f"La coordenada [{chr(65+self.coordenadaX)},{self.coordenadaY+1}] tiene el valor de:{self.valor}"

class Mapa:
    def __init__(self):
        self.matriz = list()
        self.alto = 0
        self.ancho = 0
        self.tipoMapa = None

    def leerArchivo(self, nombreArchivo):
        try:
            modo= "xd"
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

    def pedirCoordenada(self, x, y):
        if (x<0) or (y<0) or (x>=self.ancho) or (y>=self.alto):
            raise IndexError()
        return self.matriz[y][x]
    
    def crearMatrizTerreno(self):
        return np.array([[int(coordenada.valor) for coordenada in fila] for fila in self.matriz])

    def crearMatrizVisitados(self):
        return np.array([[coordenada.visitado for coordenada in fila] for fila in self.matriz])


    # QUEDA PENDIENTE DE MODIFICAR
    # def crearMatrizDatos(self):
    #     matrizDatos= list()
    #     for fila in self.matriz:
    #         listaBase= list()
    #         for coordenada in fila:
    #             listaAuxiliar= list()
    #             textoMatriz= ''
    #             if coordenada.puntoClave:
    #                 listaAuxiliar.append(coordenada.puntoClave)
    #             elif coordenada.visitado:
    #                 listaAuxiliar.append("V")
    #             elif coordenada.puntoDesicion:
    #                 listaAuxiliar.append("O")
    #             elif coordenada.valorAdicional:
    #                 listaAuxiliar.append(coordenada.valorAdicional)
    #             if len(listaAuxiliar)!=0:   textoMatriz= ','.join(listaAuxiliar)
    #             else : textoMatriz= ''
    #             listaBase.append(textoMatriz)

    #         matrizDatos.append(listaBase)
    #     return np.array(matrizDatos)

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
        elif len(tipos) <= 5 and tipos.issubset({0, 1, 2, 3, 4}):
            self.tipoMapa = "Mixto"
        else:
            raise formatoInvalidoArchivo(4)


if __name__ == "__main__":
    documento = Mapa()
