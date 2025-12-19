from Utilities.dato import VectorDato
from math import sqrt
import copy



class Modelo:
    def __init__(self):
        self.datos_originales = list()
        self.datos_actuales = list()

        self.no_columnas = [0,0]
        self.no_filas = [0,0]

        self.nombre_atributos = list()
        self.nombre_atributos_actuales = list()

    def cargar_datos(self, ruta_archivo, separador, modalidad= "inicial"):
        matriz_de_datos, matriz_de_datos_auxiliar = list(), list()
        no_columnas_auxiliar, no_filas_auxiliar = 0, 0
        separador_auxiliar = separador
        indice = 0
        try:
            with open(ruta_archivo, 'r', encoding="utf-8") as archivo:
                for no_linea, linea in enumerate(archivo):
                    linea_limpia = linea.strip()
                    linea_separada, no_columnas_actual = self._fragmentar_linea_por_separador(linea_limpia,separador)


                    if modalidad == "inicial":
                        if no_linea == 0:
                            no_columnas_auxiliar = no_columnas_actual
                        elif no_columnas_auxiliar != no_columnas_actual:
                            return ("Linea de diferentes tamaños",False)
                        indice = no_linea + 1
                    else:
                        if no_columnas_actual != self.no_columnas[1]:
                            return ("Linea de diferentes tamaños",False)
                        indice = self.no_filas[0] + no_linea + 1

                    vector_de_datos, vector_de_datos_copia = self._procesar_linea(indice, linea_separada)

                    matriz_de_datos.append(vector_de_datos), matriz_de_datos_auxiliar.append(vector_de_datos_copia)

                    no_filas_auxiliar+=1
        except Exception as e:
            return ("Error al cargar el archivo " + str(e), False)

        if modalidad == "inicial":
            for i in range(2):
                self.no_columnas[i], self.no_filas[i] = no_columnas_auxiliar, no_filas_auxiliar
            self.datos_originales = matriz_de_datos
            self.datos_actuales = matriz_de_datos_auxiliar
            for i in range(self.no_columnas[0]-1):
                self.nombre_atributos.append("Atributo " + str(i+1))
                self.nombre_atributos_actuales.append("Atributo " + str(i+1))
        else:
            self.datos_actuales.extend(matriz_de_datos_auxiliar)
            self.no_filas[1]+= no_filas_auxiliar
        return ("Datos cargados exitosamente", True)

    def _fragmentar_linea_por_separador(self, linea, separador):
        linea_separada = linea.split(separador)
        return linea_separada,len(linea_separada)

    def _procesar_linea(self, indice, linea_separada):
        lista_datos_cuantitativos = list()
        dato_cualitativo = ""

        for dato in linea_separada:
            try:
                dato= float(dato)
                lista_datos_cuantitativos.append(dato)
                continue
            except ValueError:
                pass

            if dato != "":
                dato = dato.strip()
                dato_cualitativo = dato
                break

        return VectorDato(indice, dato_cualitativo, lista_datos_cuantitativos), VectorDato(indice, dato_cualitativo, lista_datos_cuantitativos)


    def obtener_datos_valores(self):
        matriz_de_datos_valores = list()
        for vector_dato in self.datos_actuales:

            lista_de_datos = list()

            lista_de_datos.append(vector_dato.indice)
            lista_de_datos.extend(vector_dato.valores_cuantitativos)
            lista_de_datos.append(vector_dato.valor_cualitativo)

            matriz_de_datos_valores.append(lista_de_datos)
        return matriz_de_datos_valores

    def obtener_datos_cualitativos(self):
        lista_datos_cualitativos = list()

        for vector_datos in self.datos_actuales:

            dato_cualitativo = vector_datos.valor_cualitativo

            if dato_cualitativo not in lista_datos_cualitativos:
                lista_datos_cualitativos.append(dato_cualitativo)

        return lista_datos_cualitativos

    def obtener_datos_cuantitativos(self):
        matriz_lista_valores = list()

        for columna in range(self.no_columnas[1]-1):
            lista_valores_columnas = list()

            for vector in self.datos_actuales:
                lista_valores_columnas.append(vector.valores_cuantitativos[columna])


            minimo = min(lista_valores_columnas)
            maximo = max(lista_valores_columnas)
            media = round(sum(lista_valores_columnas) / len(lista_valores_columnas), 2)
            if len(lista_valores_columnas) == 1:
                desviacion_estandar = 0
            else:
                desviacion_estandar = round(sqrt(sum((x - media) ** 2 for x in lista_valores_columnas) / (len(lista_valores_columnas)-1)), 2)
            matriz_lista_valores.append(f'Minimo: {minimo}, Maximo: {maximo}, Media: {media}, Desviacion estandar: {desviacion_estandar}')

        return matriz_lista_valores

    def obtener_indice_menor_y_mayor(self):
        lista_indices_disponibles = list()
        for vector in self.datos_actuales:
            lista_indices_disponibles.append(vector.indice)
        return min(lista_indices_disponibles), max(lista_indices_disponibles)

    def verificar_atributos(self, atributos):
        atributos_encontrados = set()
        atributos_no_encontrados = set(atributos)

        for atributo in self.nombre_atributos_actuales:
            if atributo.lower() in atributos_no_encontrados:
                atributos_encontrados.add(atributo)
                atributos_no_encontrados.remove(atributo.lower())

        if len(atributos_no_encontrados) == 0:
            return True, None
        else:
            return False, ",".join(atributos_no_encontrados)

    def verificar_atributo_o_clase(self, valor):
        valor_normalizado = valor.strip().lower()
        for atributo in self.nombre_atributos_actuales:
            if atributo.lower() == valor_normalizado:
                return True

        if valor_normalizado == "clase":
            return True

        return False


    def verificar_existencia(self):
        if self.no_filas[0] == 0:
            return False
        else:
            return True

    def reiniciar_datos(self):
        self.datos_actuales = copy.deepcopy(self.datos_originales)
        self.no_columnas[1] = self.no_columnas[0]
        self.no_filas[1] = self.no_filas[0]
        self.nombre_atributos_actuales = copy.deepcopy(self.nombre_atributos)

    def borrar_datos(self):
        self.datos_originales, self.datos_actuales = list(), list()
        self.no_filas[0], self.no_filas[1] = 0, 0
        self.no_columnas[0], self.no_columnas[1] = 0, 0
        self.nombre_atributos_actuales = list()
        self.nombre_atributos = list()

    def subconjunto_uno_por_uno(self, filas):
        matriz_de_datos_auxiliar = list()
        for indice_fila in filas:

            for vector in self.datos_actuales:
                if vector.indice == indice_fila:
                    matriz_de_datos_auxiliar.append(vector)
                    break

        self.datos_actuales = matriz_de_datos_auxiliar
        self.no_filas[1] = len(self.datos_actuales)

    def subconjunto_por_intervalo(self, intervalo):
        matriz_de_datos_auxiliar = list()

        for vector in self.datos_actuales:
            if vector.indice >= intervalo[0] and vector.indice <= intervalo[1]:
                matriz_de_datos_auxiliar.append(vector)

        self.datos_actuales = matriz_de_datos_auxiliar

        self.no_filas[1] = len(self.datos_actuales)

    def subconjunto_por_atributos(self,atributos):
        matriz_de_datos_auxiliar = list()
        lista_atributos_actuales_normalizada = [atributo.lower() for atributo in self.nombre_atributos_actuales]

        for vector in self.datos_actuales:
            lista_nueva_valores_cuantitativos = list()
            for atributo in atributos:
                atributo_index = lista_atributos_actuales_normalizada.index(atributo)
                lista_nueva_valores_cuantitativos.append(vector.valores_cuantitativos[atributo_index])
            vector.valores_cuantitativos = lista_nueva_valores_cuantitativos

        self.nombre_atributos_actuales = [atributo.lower() for atributo in atributos]
        self.no_columnas[1] = len(self.nombre_atributos_actuales)+1

    def subconjunto_valor_de_atributo(self, atributo, valor):
        matriz_de_datos_auxiliar = list()
        lista_atributos_actuales_normalizada = [atributo.lower() for atributo in self.nombre_atributos_actuales]
        try:
            atributo_index = lista_atributos_actuales_normalizada.index(atributo)
        except ValueError:
            atributo_index = None

        if atributo_index != None:
            try:
                valor = float(valor)
            except ValueError:
                return "Valor ingresado invalido se requiere un numero, no se hacen cambios en la tabla"
        else:
            try:
                valor = float(valor)
                return "Valor ingresado invalido se requiere texto, no se hacen cambios en la tabla"
            except ValueError:
                valor = valor.strip().lower()

        for vector in self.datos_actuales:
            if atributo_index != None:
                if vector.valores_cuantitativos[atributo_index] == valor:
                    matriz_de_datos_auxiliar.append(vector)
            else:
                if vector.valor_cualitativo.lower() == valor.lower():
                    matriz_de_datos_auxiliar.append(vector)

        if len(matriz_de_datos_auxiliar) == 0:
            return "No se encontro ninguna aparicion del valor buscado, no se hacen cambios en la tabla"
        else:
            self.datos_actuales = matriz_de_datos_auxiliar
            self.no_filas[1] = len(self.datos_actuales)