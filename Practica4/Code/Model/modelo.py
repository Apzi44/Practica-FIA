from Utilities.dato import Dato

class Modelo:
    def __init__(self):
        self.datos = list(list())
        self.datos_actuales = list(list())
        # [0] = datos originales, [1] = datos actuales
        self.no_columnas = [0, 0]
        self.no_filas = [0, 0]
        self.separador = None

    def cargar_datos(self, ruta_archivo, separador):
        try:
            matriz_de_datos_auxiliar = list()
            no_columnas_auxiliar = 0
            no_filas_auxiliar = 0
            separador_auxiliar = separador
            with open(ruta_archivo, 'r', encoding="utf-8-sig") as archivo:
                for iteracion, linea in enumerate(archivo):
                    linea_procesada = self._procesar_linea(linea, separador_auxiliar)
                    if no_columnas_auxiliar < len(linea_procesada):
                        no_columnas_auxiliar = len(linea_procesada)
                    no_filas_auxiliar += 1
                    matriz_de_datos_auxiliar.append(linea_procesada)
            
            self.datos = matriz_de_datos_auxiliar
            self.no_columnas[0] = no_columnas_auxiliar
            self.no_filas[0] = no_filas_auxiliar
            self.no_columnas[1] = no_columnas_auxiliar
            self.no_filas[1] = no_filas_auxiliar
            self.separador = separador_auxiliar
            self.datos_actuales = [fila[:] for fila in self.datos]
        except Exception as e:
            return ("Error al cargar el archivo", False)
        return ("Datos cargados exitosamente", True)

    def obtener_datos_valores(self):
        matriz_de_datos_valores = list()
        datos_valores = list()
        for fila, linea in enumerate(self.datos_actuales):
            for columna, elemento in enumerate(linea):
                datos_valores.append(elemento.valor)
            matriz_de_datos_valores.append(datos_valores)
            datos_valores = list()

        return matriz_de_datos_valores

    def _procesar_linea(self, linea, separador):
        linea_procesada = linea.split(separador)
        lineaNueva = list()
        for no_elemento in range(len(linea_procesada)):
            dato = linea_procesada[no_elemento]
            #Se checa si es un dato quantitativo
            try:
                dato= float(dato)
                lineaNueva.append(Dato(dato, "cuantitativo"))
                continue
            except ValueError:
                pass
            #Se checa si el dato es cualitativo
            if dato != "":
                dato = dato.strip()

                lineaNueva.append(Dato(dato, "cualitativo"))
                continue
            else: 
                lineaNueva.append(Dato(dato, "nulo"))
                continue
        return lineaNueva

    def obtener_datos_cualitativos(self):
        datos_cualitativos = list()
        for linea in self.datos_actuales:
            for elemento in linea:
                if elemento.tipo == "cualitativo":
                    datos_cualitativos.append(elemento.valor)
        return datos_cualitativos, len(datos_cualitativos)

    def obtener_datos_cuantitativos(self):
        datos_quantitativos = list()
        for linea in self.datos_actuales:
            for elemento in linea:
                if elemento.tipo == "cuantitativo":
                    datos_quantitativos.append(elemento.valor)
        return datos_quantitativos, len(datos_quantitativos)
    
    def obtener_numero_datos_nulos(self):
        datos_nulos = list()
        for linea in self.datos_actuales:
            for elemento in linea:
                if elemento.tipo == "nulo":
                    datos_nulos.append(elemento)
        return datos_nulos, len(datos_nulos)

    def reiniciar_datos(self):
        self.datos_actuales = [fila[:] for fila in self.datos]
        self.no_columnas[1] = self.no_columnas[0]
        self.no_filas[1] = self.no_filas[0]

    def borrar_datos(self):
        self.datos_actuales = list(list())
        self.no_columnas[0] = 0
        self.no_filas[0] = 0
        self.no_columnas[1] = 0
        self.no_filas[1] = 0
        self.separador = None
        self.datos_actuales = list(list())

    def subconjunto_uno_por_uno(self, filas):
        matriz_de_datos_auxiliar = list()
        for fila in filas:
            fila= fila-1
            matriz_de_datos_auxiliar.append(self.datos_actuales[fila])
        self.datos_actuales = matriz_de_datos_auxiliar
        self.no_filas[1] = len(self.datos_actuales)
        self.no_columnas[1] = len(self.datos_actuales[0])

    def subconjunto_por_intervalo(self, intervalo):
        matriz_de_datos_auxiliar = list()
        #Se resta 1 para que el intervalo sea correcto
        intervalo[0] = intervalo[0]-1

        for fila in range(intervalo[0], intervalo[1]):
            matriz_de_datos_auxiliar.append(self.datos_actuales[fila])
        self.datos_actuales = matriz_de_datos_auxiliar
        self.no_filas[1] = len(self.datos_actuales)
        self.no_columnas[1] = len(self.datos_actuales[0])
        
    def chequeo_atributo(self, atributos):
        atributos_encontrados = set()
        atributos_no_encontrados = set()
        atributos_no_encontrados = set(atributos)

        for fila in self.datos_actuales:
            for columna in fila:
                if columna.tipo in atributos_no_encontrados:
                    atributos_encontrados.add(columna.tipo)
                    atributos_no_encontrados.remove(columna.tipo)
                    break

        if atributos_no_encontrados:
            return False
        return True
