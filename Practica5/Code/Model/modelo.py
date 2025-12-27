from Utilities.dato import VectorDato, VectorClasificar
import copy
import math
from collections import Counter
import difflib

class Modelo:
    def __init__(self):
        self.datos = list()
        self.datos_clasificar = list()

        self.no_columnas = 0
        self.no_filas = 0
        self.no_filas_clasificar = 0

    def verificar_existencia(self):
        if self.no_columnas == 0:
            return False
        else:
            return True

    def _es_numero(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False

    def crear_tupla_atributos(self):
        tupla_atributos = list()
        for i,dato in enumerate(self.datos[0].valores):
            nombre_atributo ="Atributo " + str(i+1)
            tipo_dato = "numerico" if self._es_numero(dato) else "texto"
            tupla_atributos.append((nombre_atributo,tipo_dato))
        return tupla_atributos

    def retornar_nombre_atributos(self):
        lista_atributos = list()
        for i in range(self.no_columnas):
            lista_atributos.append("Atributo " + str(i+1))
        return lista_atributos

    #FUNCIONES DE BORRAR DATOS
    def borrar_datos_conjunto_datos(self):
        self.datos = list()
        self.no_columnas = 0
        self.no_filas = 0

    def borrar_datos_clasificar(self):
        self.datos_clasificar = list()
        self.no_filas_clasificar = 0

    #FUNCIONES DE INGRESION DE DATOS POR ARCHIVO
    def crear_conjunto_de_datos_por_archivo(self, ruta_archivo, separador):
        lista_datos_auxiliar = list()
        no_columnas_auxiliar = 0
        no_filas_auxiliar = 0
        indice = 0
        try:
            with open(ruta_archivo, 'r', encoding="utf-8") as archivo:
                for no_linea, linea in enumerate(archivo):
                    linea_limpia = linea.strip()
                    linea_separada, no_columnas_actual = self._fragmentar_linea_por_separador(linea_limpia,separador)
                    # Si es la primer linea, se procesa la linea como la creacion manual
                    if no_linea == 0:
                        no_columnas_auxiliar = no_columnas_actual
                        lista_datos_auxiliar.append(VectorDato(no_linea+1, linea_separada))
                    else:
                        if no_columnas_actual != no_columnas_auxiliar:
                            return "Linea de diferentes tamaños"
                        
                        for i,valor in enumerate(linea_separada):
                            if self._es_numero(valor) != self._es_numero(lista_datos_auxiliar[0].valores[i]):
                                return "Linea de diferentes tipos de datos"
                        
                        lista_datos_auxiliar.append(VectorDato(no_linea+1, linea_separada))
            
            self.no_columnas = no_columnas_auxiliar
            self.no_filas = no_filas_auxiliar
            self.datos = lista_datos_auxiliar
            return "Exito"
        except Exception as e:
            return str(e)

    def anadir_datos_a_conjunto_de_datos_por_archivo(self, ruta_archivo, separador):
        try:
            with open(ruta_archivo, 'r', encoding="utf-8") as archivo:
                for no_linea, linea in enumerate(archivo):
                    linea_limpia = linea.strip()
                    linea_separada, no_columnas_actual = self._fragmentar_linea_por_separador(linea_limpia,separador)
                    if no_columnas_actual != self.no_columnas:
                        return "Linea de diferentes tamaños"
                    
                    for i,valor in enumerate(linea_separada):
                        if self._es_numero(valor) != self._es_numero(self.datos[0].valores[i]):
                            return "Linea de diferentes tipos de datos"
                    
                    self.no_filas+=1
                    self.datos.append(VectorDato(self.no_filas, linea_separada))
            return "Exito"
        except Exception as e:
            return str(e)

    def _fragmentar_linea_por_separador(self, linea, separador):
        linea_separada = linea.split(separador)
        return linea_separada,len(linea_separada)

    # FUNCIONES DE INGRESION DE DATOS MANUALMENTE
    def crear_conjunto_de_datos_manualmente(self,vector_entrada):
        self.no_columnas = len(vector_entrada)
        self.no_filas+=1
        self.datos.append(VectorDato(self.no_filas, vector_entrada))
        return "Exito"

    def anadir_vector_a_conjunto_de_datos_manualmente(self, vector_entrada):
        for i,valor in enumerate(vector_entrada):
            if self._es_numero(valor) != self._es_numero(self.datos[0].valores[i]):
                return "Error: El vector de entrada debe tener el mismo tipo de dato que los datos cargados"
        
        self.no_filas+=1
        self.datos.append(VectorDato(self.no_filas, vector_entrada))
        return "Exito"

    # FUNCIONES MUESTRA DE DATOS
    def regresar_tabla_datos(self, modalidad = "conjunto"):
        if modalidad == "conjunto":
            datos = self.datos
        elif modalidad == "clasificar":
            datos = self.datos_clasificar
        tabla = list()
        for vector in datos:
            lista_valores = list()
            lista_valores.append(vector.indice)
            for valor in vector.valores:
                lista_valores.append(valor)
            tabla.append(lista_valores)
        return tabla

    # FUNCIONES DE INGRESION DE DATOS CLASIFICAR
    def anadir_vector_a_conjunto_de_datos_clasificar(self, vector_entrada_clasificar):
        self.no_filas_clasificar+=1
        lista_valores = list()
        lista_funciones = list()

        for i,valor in enumerate(vector_entrada_clasificar):
            if valor[1] == "Entrada":
                if self._es_numero(valor[0]) != self._es_numero(self.datos[0].valores[i]):
                    return "Error: El vector de entrada debe tener el mismo tipo de dato que los datos clasificados"
            lista_valores.append(valor[0])
            lista_funciones.append(valor[1])
        
        self.datos_clasificar.append(VectorClasificar(self.no_filas_clasificar, lista_valores, lista_funciones))
        return "Exito"

    # FUNCIONES CLASIFICACION
    def aplicar_aprendizaje_por_distancia_minima(self, usar_manhattan = False):
        for vector_sin_clasificar in self.datos_clasificar:
            indices_entrada = [i for i,funcion in enumerate(vector_sin_clasificar.funcion) if funcion == "Entrada"]
            indices_salida = [i for i,funcion in enumerate(vector_sin_clasificar.funcion) if funcion == "Salida"]
            vector_sin_clasificar_valores = [vector_sin_clasificar.valores[i] for i in indices_entrada]
            self.entrenar_minima_distancia(indices_entrada, indices_salida)
            clase_resultante = self.clasificar_por_distancia_minima(vector_sin_clasificar_valores, usar_manhattan)
            atributos_resultantes = clase_resultante.split("_")
            for i,atributo in enumerate(atributos_resultantes):
                vector_sin_clasificar.valores[indices_salida[i]] = atributo
       
    def aplicar_aprendizaje_por_knn(self, k, usar_manhattan=False):
        for vector_sin_clasificar in self.datos_clasificar:
            indices_entrada = [i for i,funcion in enumerate(vector_sin_clasificar.funcion) if funcion == "Entrada"]
            indices_salida = [i for i,funcion in enumerate(vector_sin_clasificar.funcion) if funcion == "Salida"]
            vector_sin_clasificar_valores = [vector_sin_clasificar.valores[i] for i in indices_entrada]
            self.entrenar_knn(indices_entrada, indices_salida)
            clase_resultante = self.clasificar_knn(vector_sin_clasificar_valores, k, usar_manhattan)
            atributos_resultantes = clase_resultante.split("_")
            for i,atributo in enumerate(atributos_resultantes):
                vector_sin_clasificar.valores[indices_salida[i]] = atributo

    # FUNCIONES DE APRENDIZAJE MINIMA DISTANCIA
    def entrenar_minima_distancia(self, indices_entrada, indices_salida):
        self.memoria_centroides = []
        diccionario_clases = {}

        for vector in self.datos:
            # Forma un vector de entrada para cada clase
            vector_entrada = [vector.valores[i] for i in indices_entrada]

            # Forma una etiqueta de clase para cada vector de entrada
            etiqueta_clase = "_".join([str(vector.valores[i]) for i in indices_salida])
            etiqueta_clase = etiqueta_clase.lower()

            # Si la etiqueta de clase no esta en el diccionario, la agrega
            if etiqueta_clase not in diccionario_clases:
                diccionario_clases[etiqueta_clase] = []
            
            # Agrega el vector de entrada a la lista de vectores de la clase
            diccionario_clases[etiqueta_clase].append(vector_entrada)

        # Calcula el centroide de cada clase, items regresa una tupla (clase, lista_vectores)
        for clase, lista_vectores in diccionario_clases.items():
            # Se calcula un vector centroide para cada clase
            centroide = self._calcular_centroide(lista_vectores)
            
            # Agrega el centroide a la memoria de centroides almacenandola como un diccionario donde
            # se tiene la clave y el vector promedio que es una lista
            self.memoria_centroides.append({ "clase": clase, "vector_promedio": centroide })

    def clasificar_por_distancia_minima(self, vector_entrada_usuario, usar_manhattan=False):
        # Inicializa la mejor distancia y la clase ganadora
        mejor_distancia = float('inf')
        clase_ganadora = None

        # Recorre la memoria de los centroides y asi obtenemos la mejor clase
        for centroide_vector in self.memoria_centroides:
            # Obtenemos la clase y el vector promedio
            centroide = centroide_vector['vector_promedio']
            
            # Calculamos la distancia entre el vector nuevo y el centroide de la clase
            if usar_manhattan:
                distancia = self._distancia_manhattan(vector_entrada_usuario, centroide)
            else:
                distancia = self._distancia_euclidiana(vector_entrada_usuario, centroide)

            # Nos quedamos con la distancia más pequeña
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                # Almacenamos la clase que es menor
                clase_ganadora = centroide_vector['clase']

        return clase_ganadora

    def _calcular_centroide(self,lista_vectores):
        numero_columnas = len(lista_vectores[0])
        numero_filas = len(lista_vectores)
        vector_resultante = []

        for columna in range(numero_columnas):
            # Obtenemos todos los valores de la columna
            columna_valores = [vector[columna] for vector in lista_vectores]
            
            # Si la columna es numerica
            if self._es_numero(columna_valores[0]):
                suma = sum(float(v) for v in columna_valores)
                promedio = suma / numero_filas
                vector_resultante.append(promedio)
            else:
            # Si la columna es un string
                conteo = Counter(columna_valores)
                moda = conteo.most_common(1)[0][0]
                vector_resultante.append(moda)
        
        return vector_resultante

    # FUNCIONES DE APRENDIZAJE KNN
    def entrenar_knn(self, indices_entrada, indices_salida):
        self.base_conocimiento = []

        for vector in self.datos:
            # Obtenemos los valores de entrada
            vector_entrada = [vector.valores[i] for i in indices_entrada]
            # Obtenemos la clase de salida
            clase_salida = "_".join([str(vector.valores[i]) for i in indices_salida])
            # Convertimos la clase de salida a minusculas
            clase_salida = clase_salida.lower()
            # Agregamos el vector de entrada y la clase de salida a la base de conocimiento
            self.base_conocimiento.append({"entrada": vector_entrada, "salida": clase_salida})

    def clasificar_knn(self, vector_entrada_usuario, k, usar_manhattan=False):
        lista_distancias = []

        for vector_guardado in self.base_conocimiento:
            # Obtenemos el vector de entrada
            vector_entrada = vector_guardado['entrada']
            # Obtenemos la clase de salida
            clase_salida = vector_guardado['salida']

            if usar_manhattan:
                distancia = self._distancia_manhattan(vector_entrada_usuario, vector_entrada)
            else:
                distancia = self._distancia_euclidiana(vector_entrada_usuario, vector_entrada)
            
            # Agregamos la distancia y la clase de salida a la lista de distancias
            lista_distancias.append((distancia, clase_salida))

        # Ordenamos la lista de distancias
        lista_distancias.sort(key=lambda x: x[0])

        # Obtenemos los k vecinos mas cercanos
        vecinos_cercanos = lista_distancias[:k]
        # Obtenemos la clase de salida
        votos = [vecino[1] for vecino in vecinos_cercanos]
        
        conteo = Counter(votos)
        # Obtenemos la clase ganadora
        clase_ganadora = conteo.most_common(1)[0][0]

        return clase_ganadora

    # FUNCIONES PARA CALCULO DE DISTANCIAS
    def _distancia_euclidiana(self, v1, v2):
        suma = 0
        for i in range(len(v1)):
            diferencia = self._diferencia_mixta(v1[i], v2[i])
            suma += diferencia ** 2
        return math.sqrt(suma)

    def _distancia_manhattan(self, v1, v2):
        suma = 0
        for i in range(len(v1)):
            diferencia = self._diferencia_mixta(v1[i], v2[i])
            suma += abs(diferencia)
        return suma

    def _diferencia_mixta(self, dato1, dato2):
        if self._es_numero(dato1) and self._es_numero(dato2):
            return float(dato1) - float(dato2)
        if str(dato1).lower() == str(dato2).lower():
            return 0.0
        else:
           similitud = difflib.SequenceMatcher(None, str(dato1), str(dato2)).ratio()
           return 1.0 - similitud