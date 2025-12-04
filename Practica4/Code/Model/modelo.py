from Utilities.dato import VectorDato
import copy

class Modelo:
    def __init__(self):
        # Matriz de datos
        self.datos = list()
        self.datos_actuales = list()

        # [0] = datos originales, [1] = datos actuales
        self.no_columnas = [0,0]
        self.no_filas = [0,0]
        
        #Separador de la matriz
        self.separador = None

    def cargar_datos(self, ruta_archivo, separador, modalidad= "inicial"):
        try:
            # Valores auxiliares
            matriz_de_datos = list()
            matriz_de_datos_auxiliar = list()
            no_columnas_auxiliar = 0
            no_filas_auxiliar = 0
            separador_auxiliar = separador

            with open(ruta_archivo, 'r', encoding="utf-8") as archivo:
                for no_linea , linea in enumerate(archivo):
                    linea_limpia = linea.strip()
                    linea_separada, no_columnas = self._fragmentar_linea_por_separador(linea_limpia,separador)
                    #Si es primer linea se actualiza el numero de columnas
                    if no_linea == 0:
                        no_columnas_auxiliar = no_columnas
                    #Si no se verifica que mantengan el mismo tamaño de lineas
                    else:
                        if no_columnas_auxiliar != no_columnas:
                            return ("Linea de diferentes tamaños",False)
                    
                    # Se añade a la matriz actual el vector de datos obtenidos
                    vector_de_datos, vector_de_datos_copia = self._procesar_linea(linea_separada)

                    # Se verifica la misma cantidad de datos cuantativos
                    if no_linea != 0:
                        if len(vector_de_datos.valores_cuantitativos) != len(matriz_de_datos[no_linea-1].valores_cuantitativos):
                            return ("Se tiene que tener la misma cantidad de valores cuantitativos en cada vector de datos",False)

                    matriz_de_datos.append(vector_de_datos)
                    matriz_de_datos_auxiliar.append(vector_de_datos_copia)

                    # Se actualiza el valor de filas actual
                    no_filas_auxiliar+=1
            
            # Se actualizan valores de columnas y filas
            for i in range(2):
                self.no_columnas[i], self.no_filas[i] = no_columnas_auxiliar, no_filas_auxiliar
            
            # Se actualiza separador usado
            self.separador = separador_auxiliar
        except Exception as e:
            return ("Error al cargar el archivo " + str(e), False)
        
        if modalidad == "inicial":
            self.datos = matriz_de_datos
            self.datos_actuales = matriz_de_datos_auxiliar
        else:
            self.datos_actuales.extend(matriz_de_datos)
            self.datos_actuales.extend(matriz_de_datos_auxiliar)
            self.no_filas[1] += no_filas_auxiliar

        return ("Datos cargados exitosamente", True)

    def obtener_datos_valores(self):
        # Matriz de datos valores
        matriz_de_datos_valores = list()
        for vectorDato in self.datos_actuales:
            #Se limpia la lista de datos para la siguiente iteracion
            lista_de_datos = list()
            #Se obtiene el valor cualitativo
            dato_cualitativo = vectorDato.valor_cualitativo
            #Se obtiene los valores cuantitativos
            valores_cuantitativos = vectorDato.valores_cuantitativos
            #Se añade el valor a la lista de valores
            lista_de_datos.extend(valores_cuantitativos)
            lista_de_datos.append(dato_cualitativo)

            #Se añade la lista de valores a la matriz de datos
            matriz_de_datos_valores.append(lista_de_datos)

        return matriz_de_datos_valores

    def obtener_datos_cuantitativos_cualitativos(self):
        lista_datos_cuantitativos = list()
        lista_datos_cualitativos = list()

        for vector_datos in self.datos_actuales:
            #Se obtiene el valor cualitativo
            dato_cualitativo = vector_datos.valor_cualitativo
            #Se añade a la lista el valor si no se encuentra en la lista actual
            if dato_cualitativo not in lista_datos_cualitativos:
                lista_datos_cualitativos.append(dato_cualitativo)

            #Se obtiene la lista de datos cuantitativos
            lista_cuantitativos = vector_datos.valores_cuantitativos
            for dato_cuantitativo in lista_cuantitativos:
                #Se itera en la lista y se añade a la lista el valor si no se encuentra en la lista actual
                if dato_cuantitativo not in lista_datos_cuantitativos:
                    lista_datos_cuantitativos.append(dato_cuantitativo)

        return lista_datos_cualitativos, lista_datos_cuantitativos

    def _fragmentar_linea_por_separador(self, linea,separador):
        linea_separada = linea.split(separador)
        return linea_separada,len(linea_separada)

    def _procesar_linea(self, linea_separada):
        lista_datos_cuantativos = list()
        dato_cualitativo = ""

        # Iteramos sobre cada elemento de la fila
        for dato in linea_separada:
            try:
                dato= float(dato)
                lista_datos_cuantativos.append(dato)
                continue
            except ValueError:
                pass

            #Se checa si el dato es cualitativo
            if dato != "":
                dato = dato.strip()
                dato_cualitativo = dato
                continue

        #Se regresa un vector con el dato cualitativo y los datos cuantitativos
        return VectorDato(dato_cualitativo, lista_datos_cuantativos), VectorDato(dato_cualitativo, lista_datos_cuantativos)

    def verificar_existencia(self):
        if self.no_filas[0] == 0:
            return False
        else:
            return True

    def reiniciar_datos(self):
        self.datos_actuales = copy.deepcopy(self.datos)
        self.no_columnas[1] = self.no_columnas[0]
        self.no_filas[1] = self.no_filas[0]

    def borrar_datos(self):
        self.datos = list()
        self.datos_actuales = list()
        self.no_filas[0] = 0
        self.no_columnas[0] = 0
        self.no_filas[1] = 0
        self.no_columnas[1] = 0
        self.separador = None

    def subconjunto_uno_por_uno(self, filas):
        # Se crea una lista auxiliar para la matriz de datos actuales
        matriz_de_datos_auxiliar = list()
        for fila in filas:
            # Se itera en la lista de filas y se resta 1 para que el intervalo sea correcto
            fila= fila-1
            # Se añade la fila a la lista auxiliar
            matriz_de_datos_auxiliar.append(self.datos_actuales[fila])

        # Se actualiza la matriz de datos actuales
        self.datos_actuales = matriz_de_datos_auxiliar
        self.no_filas[1] = len(self.datos_actuales)

    def subconjunto_por_intervalo(self, intervalo):
        # Se crea una lista auxiliar para la matriz de datos actuales
        matriz_de_datos_auxiliar = list()
        #Se resta 1 para que el intervalo sea correcto
        intervalo[0] = intervalo[0]-1

        for fila in range(intervalo[0], intervalo[1]):
            matriz_de_datos_auxiliar.append(self.datos_actuales[fila])
        self.datos_actuales = matriz_de_datos_auxiliar
        self.no_filas[1] = len(self.datos_actuales)
           
    def verificar_atributo(self,atributos):
        # Se crea un conjunto de atributos encontrados y no encontrados
        atributos_encontrados = set()
        atributos_no_encontrados = set(atributos)
        
        # Se itera sobre cada vector de datos
        for vector_dato in self.datos_actuales:
            # Se obtiene el valor cualitativo
            valor_cualitativo = vector_dato.valor_cualitativo.lower()
            # Se checa si el valor cualitativo esta en el conjunto de atributos no encontrados
            if valor_cualitativo in atributos_no_encontrados:
                atributos_encontrados.add(valor_cualitativo)
                atributos_no_encontrados.remove(valor_cualitativo)
        
        # Se regresa un booleano y el conjunto de atributos no encontrados para el caso de que no se encuentre el atributo
        if len(atributos_no_encontrados) > 0:
            return False, ",".join(atributos_no_encontrados)
        else:
        # Si se encuentran todos los atributos se regresa True y None
            return True, None

    def subconjunto_atributo(self, atributos):
        # Se crea una lista auxiliar para la matriz de datos actuales
        matriz_de_datos_auxiliar = list()
        # Se itera sobre cada vector de datos
        for vector_dato in self.datos_actuales:
            # Se checa si el valor cualitativo esta en el conjunto de atributos
            if vector_dato.valor_cualitativo.lower() in atributos:
                matriz_de_datos_auxiliar.append(vector_dato)

        # Se actualiza la matriz de datos actuales
        self.datos_actuales = matriz_de_datos_auxiliar
        self.no_filas[1] = len(self.datos_actuales)
        