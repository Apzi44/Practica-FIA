from Utilities.dato import VectorDato, VectorClasificar
import copy
import math
from collections import Counter
import difflib
import random

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
                    linea_limpia = linea.strip().lower()
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
                no_filas_auxiliar = no_linea + 1
            
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
                    linea_limpia = linea.strip().lower()
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
            self.entrenar_minima_distancia(indices_entrada, indices_salida, self.datos)
            clase_resultante = self.clasificar_por_distancia_minima(vector_sin_clasificar_valores, usar_manhattan)
            atributos_resultantes = clase_resultante.split("_")
            for i,atributo in enumerate(atributos_resultantes):
                vector_sin_clasificar.valores[indices_salida[i]] = atributo
       
    def aplicar_aprendizaje_por_knn(self, k, usar_manhattan=False):
        for vector_sin_clasificar in self.datos_clasificar:
            indices_entrada = [i for i,funcion in enumerate(vector_sin_clasificar.funcion) if funcion == "Entrada"]
            indices_salida = [i for i,funcion in enumerate(vector_sin_clasificar.funcion) if funcion == "Salida"]
            vector_sin_clasificar_valores = [vector_sin_clasificar.valores[i] for i in indices_entrada]
            self.entrenar_knn(indices_entrada, indices_salida, self.datos)
            clase_resultante = self.clasificar_knn(vector_sin_clasificar_valores, k, usar_manhattan)
            atributos_resultantes = clase_resultante.split("_")
            for i,atributo in enumerate(atributos_resultantes):
                vector_sin_clasificar.valores[indices_salida[i]] = atributo

    # FUNCIONES DE APRENDIZAJE MINIMA DISTANCIA
    def entrenar_minima_distancia(self, indices_entrada, indices_salida, lista_datos_entrenamiento):
        self.memoria_centroides = []
        diccionario_clases = {}

        for vector in lista_datos_entrenamiento:
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
    def entrenar_knn(self, indices_entrada, indices_salida, lista_datos_entrenamiento):
        self.base_conocimiento = []

        for vector in lista_datos_entrenamiento:
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

    def validar_con_train_and_test(self, atributos, porcentaje, usar_knn, k, usar_manhattan):
        self.datos_clasificar = list()
        # Primero formamos el conjunto de entrenamiento y el conjunto de prueba
        numero_grupo_entrenamiento = int((porcentaje/100) * self.no_filas)
        if numero_grupo_entrenamiento == self.no_filas:
            numero_grupo_entrenamiento -= 1
        if numero_grupo_entrenamiento == 0:
            numero_grupo_entrenamiento = 1
        
        numero_grupo_prueba = self.no_filas - numero_grupo_entrenamiento

        # Mezclamos los datos
        lista_datos_mezclados = [copy.deepcopy(vector) for vector in self.datos]

        # Mezclamos los datos
        random.shuffle(lista_datos_mezclados)

        # Obtenemos el conjunto de entrenamiento
        conjunto_entrenamiento = lista_datos_mezclados[:numero_grupo_entrenamiento]
        # Obtenemos el conjunto de prueba
        conjunto_prueba = lista_datos_mezclados[numero_grupo_entrenamiento:]

        # Obtenemos los indices de entrada y salida
        indices_entrada = [i for i,funcion in enumerate(atributos) if funcion == "Entrada"]
        indices_salida = [i for i,funcion in enumerate(atributos) if funcion == "Salida"]
        
        # Entrenamos y clasificamos
        _ = self._entrenar_y_clasificar(atributos, indices_entrada, indices_salida, conjunto_entrenamiento, conjunto_prueba, usar_knn, k, usar_manhattan)

        # Obtenemos resultados
        aciertos = 0
        errores = 0
        for vector in self.datos_clasificar:
            clase_obtenida = "_".join([vector.valores[j] for j in indices_salida])
            clase_real = "_".join([self.datos[vector.indice-1].valores[j] for j in indices_salida])
            if clase_obtenida == clase_real: aciertos += 1
            else: errores += 1
        
        porcentaje_eficiencia = (aciertos / (aciertos + errores)) * 100
        porcentaje_errores = (errores / (aciertos + errores)) * 100
        return aciertos, errores, porcentaje_eficiencia, porcentaje_errores

    def validar_con_k_fold_cross_validation(self, atributos, k_divisiones, usar_knn, k_knn, usar_manhattan):
        lista_datos_clasificar_auxiliar = list()
        # Mezclamos los datos
        lista_datos_mezclados = [copy.deepcopy(vector) for vector in self.datos]
        random.shuffle(lista_datos_mezclados)
        
        # Calculamos el tamaño de cada grupo
        total_datos = len(lista_datos_mezclados)
        tamaño_grupo = int(total_datos / k_divisiones)

        # Obtenemos los indices de entrada y salida
        indices_entrada = [i for i,funcion in enumerate(atributos) if funcion == "Entrada"]
        indices_salida = [i for i,funcion in enumerate(atributos) if funcion == "Salida"]

        resultados_por_grupo = []
        for i in range(k_divisiones):
            self.datos_clasificar = list()
            inicio_grupo = i * tamaño_grupo

            # Si se es el ultimo grupo se toma todos los elementos restantes en caso de impar
            if i == k_divisiones-1: fin_grupo = total_datos
            # Si no, se toma el grupo normal
            else: fin_grupo = (i+1) * tamaño_grupo

            # Obtenemos el grupo de prueba y entrenamiento
            grupo_prueba = lista_datos_mezclados[inicio_grupo:fin_grupo]
            grupo_entrenamiento = lista_datos_mezclados[:inicio_grupo] + lista_datos_mezclados[fin_grupo:]

            # Entrenamos y clasificamos
            lista_vectores_clasificados = self._entrenar_y_clasificar(atributos, indices_entrada, indices_salida, grupo_entrenamiento, grupo_prueba, usar_knn, k_knn, usar_manhattan)
            lista_datos_clasificar_auxiliar.extend(lista_vectores_clasificados)

            #Obtenemos resultados por grupo
            aciertos = 0
            errores = 0
            for vector in self.datos_clasificar:
                # Obtenemos la clase obtenida
                clase_obtenida = "_".join([vector.valores[j] for j in indices_salida])
                # Obtenemos la clase real
                clase_real = "_".join([self.datos[vector.indice-1].valores[j] for j in indices_salida])
                
                if clase_obtenida == clase_real: aciertos += 1
                else: errores += 1
            resultados_por_grupo.append(self._obtener_resultados_por_grupo(aciertos, errores))

        # Obtenemos resultados promedio
        resultados_globales = self._obtener_resultados_globales(resultados_por_grupo)
        resultados_por_grupo.append(resultados_globales)

        self.datos_clasificar = lista_datos_clasificar_auxiliar

        #Calculamos desviacion estandar de eficiencia y error
        eficiencia_promedio = sum([grupo["porcentaje_eficiencia"] for grupo in resultados_por_grupo]) / len(resultados_por_grupo)
        if len(resultados_por_grupo) > 1:
            sumatoria_para_desv = sum([((grupo["porcentaje_eficiencia"] - eficiencia_promedio) ** 2) for grupo in resultados_por_grupo])
            desviacion_eficiencia = math.sqrt(sumatoria_para_desv / (len(resultados_por_grupo)-1))
        else: desviacion_eficiencia = 0

        error_promedio = sum([grupo["porcentaje_errores"] for grupo in resultados_por_grupo]) / len(resultados_por_grupo)
        if len(resultados_por_grupo) > 1:
            sumatoria_para_desv = sum([((grupo["porcentaje_errores"] - error_promedio) ** 2) for grupo in resultados_por_grupo])
            desviacion_error = math.sqrt(sumatoria_para_desv / (len(resultados_por_grupo)-1))
        else: desviacion_error = 0

        return resultados_por_grupo, desviacion_eficiencia, desviacion_error

    def validad_con_bootstrap(self, atributos, iteraciones, n_test, n_entrenamiento, usar_knn, k_knn, usar_manhattan):
        self.datos_clasificar = list()
        numero_total = len(self.datos)
        indices_totales = range(numero_total)

        # Obtenemos los indices de entrada y salida
        indices_entrada = [i for i,funcion in enumerate(atributos) if funcion == "Entrada"]
        indices_salida = [i for i,funcion in enumerate(atributos) if funcion == "Salida"]

        historial_metricas = []
        for i in range(iteraciones):
            # Calculamos indices de entrenamiento
            indices_entrenamiento = random.choices(indices_totales, k=n_entrenamiento)
            set_indices_entrenamiento = set(indices_entrenamiento)
            
            # Calculamos grupos de prueba
            indices_cantidatos_prueba = [i for i in indices_totales if i not in set_indices_entrenamiento]
            indices_prueba = []
            # Si el conjunto de prueba es mayor o igual al tamaño de prueba, se elige aleatoriamente
            if len(indices_cantidatos_prueba) >= n_test:
                indices_prueba = random.choices(indices_cantidatos_prueba, k=n_test)
            # Si no, se toman todos los indices restantes
            else:
                indices_prueba = indices_cantidatos_prueba
            # Si no hay indices de prueba, se salta la iteracion
            if not indices_prueba:
                continue

            # Construccion de los grupos de prueba y entrenamiento
            grupo_prueba = [copy.deepcopy(self.datos[i]) for i in indices_prueba]
            grupo_entrenamiento = [copy.deepcopy(self.datos[i]) for i in indices_entrenamiento]

            # Entrenamos y clasificamos
            lista_vectores_clasificados = self._entrenar_y_clasificar(atributos, indices_entrada, indices_salida, grupo_entrenamiento, grupo_prueba, usar_knn, k, usar_manhattan)
            lista_datos_clasificar_auxiliar.extend(lista_vectores_clasificados)

            # Obtenemos resultados por clase y grupo
            resultados_por_clase = []
            diccionario_clases = {}
            aciertos_grupo = 0
            errores_grupo = 0
            for vector in self.datos_clasificar:
                clase_real = "_".join([vector.valores[j] for j in indices_salida])
                clase_real = clase_real.lower()
                clase_resultante = "_".join([vector.valores[j] for j in indices_salida])
                clase_resultante = clase_resultante.lower()

                if clase_real not in diccionario_clases:
                    diccionario_clases[clase_real] = {"aciertos": 0, "errores": 0}
                if clase_real == clase_resultante:
                    diccionario_clases[clase_real]["aciertos"] += 1
                    aciertos_grupo += 1
                else:
                    diccionario_clases[clase_real]["errores"] += 1
                    errores_grupo += 1

            resultados_por_grupo = self._obtener_resultados_por_grupo(aciertos_grupo, errores_grupo)
            resultados_por_clase = self._obtener_resultados_por_clase(diccionario_clases)
            historial_metricas.append({"resultados_por_grupo": resultados_por_grupo, "resultados_por_clase": resultados_por_clase})

        self.datos_clasificar = lista_datos_clasificar_auxiliar
        resultados_globales = self._obtener_resultados_globales(historial_metricas)

        eficiencia_promedio = sum([grupo["resultados_por_grupo"]["porcentaje_eficiencia"] for grupo in historial_metricas]) / iteraciones
        errores_promedio = sum([grupo["resultados_por_grupo"]["porcentaje_errores"] for grupo in historial_metricas]) / iteraciones
        if iteraciones > 1:
            sumatoria_para_desviacion_eficiencia = sum([((grupo["resultados_por_grupo"]["porcentaje_eficiencia"] - eficiencia_promedio) ** 2) for grupo in historial_metricas])
            sumatoria_para_desviacion_errores = sum([((grupo["resultados_por_grupo"]["porcentaje_errores"] - errores_promedio) ** 2) for grupo in historial_metricas])
            desviacion_eficiencia = math.sqrt(sumatoria_para_desviacion_eficiencia / (iteraciones-1))
            desviacion_errores = math.sqrt(sumatoria_para_desviacion_errores / (iteraciones-1))
        else:
            desviacion_eficiencia = 0
            desviacion_errores = 0
        return historial_metricas, resultados_globales, desviacion_eficiencia, desviacion_errores

    @staticmethod
    def _obtener_resultados_por_grupo(aciertos_grupo, errores_grupo):
        porcentaje_eficiencia_grupo = (aciertos_grupo / (aciertos_grupo + errores_grupo)) * 100
        porcentaje_errores_grupo = (errores_grupo / (aciertos_grupo + errores_grupo)) * 100
        resultados_por_grupo = { "aciertos": aciertos_grupo, "errores": errores_grupo,
                                "porcentaje_eficiencia": porcentaje_eficiencia_grupo,
                                "porcentaje_errores": porcentaje_errores_grupo }
        return resultados_por_grupo

    @staticmethod
    def _obtener_resultados_por_clase(diccionario_clases):
        resultados_por_clase = []

        for clave,valor in diccionario_clases.items():
            porcentaje_eficiencia_clase = (valor["aciertos"] / (valor["aciertos"] + valor["errores"])) * 100
            porcentaje_errores_clase = (valor["errores"] / (valor["aciertos"] + valor["errores"])) * 100
            resultados_por_clase.append({ "clase": clave, "aciertos": valor["aciertos"], "errores": valor["errores"],
                                        "total": valor["aciertos"] + valor["errores"],
                                        "porcentaje_eficiencia": porcentaje_eficiencia_clase,
                                        "porcentaje_errores": porcentaje_errores_clase })
        return resultados_por_clase

    @staticmethod
    def _obtener_resultados_globales(resultados_por_grupo):
        resultados_globales = { "aciertos": sum([grupo["aciertos"] for grupo in resultados_por_grupo]),
                                "errores": sum([grupo["errores"] for grupo in resultados_por_grupo]),
                                "porcentaje_eficiencia": sum([grupo["porcentaje_eficiencia"] for grupo in resultados_por_grupo]) / len(resultados_por_grupo),
                                "porcentaje_errores": sum([grupo["porcentaje_errores"] for grupo in resultados_por_grupo]) / len(resultados_por_grupo) }
        return resultados_globales

    def _entrenar_y_clasificar(self, atributos, indices_entrada, indices_salida, grupo_entrenamiento, grupo_prueba, usar_knn, k, usar_manhattan):
        lista_vectores_auxiliar = []
        if usar_knn:
            self.entrenar_knn(indices_entrada, indices_salida, grupo_entrenamiento)
        else:
            self.entrenar_minima_distancia(indices_entrada, indices_salida, grupo_entrenamiento)

        # Configuramos los datos como para clasificar
        for vector in grupo_prueba:
            vector_para_clasificar = VectorClasificar(vector.indice, valores=vector.valores, funcion=atributos)
            self.datos_clasificar.append(vector_para_clasificar)

        # Probamos los datos
        for vector in self.datos_clasificar:
            vector_valores_entrada = [vector.valores[i] for i in indices_entrada]
            if usar_knn:
                resultado = self.clasificar_knn(vector_valores_entrada, k, usar_manhattan)
            else:
                resultado = self.clasificar_por_distancia_minima(vector_valores_entrada)
            atributos_resultantes = resultado.split("_")
            for i,atributo in enumerate(atributos_resultantes):
                vector.valores[indices_salida[i]] = atributo
            lista_vectores_auxiliar.append(vector)
        
        return lista_vectores_auxiliar