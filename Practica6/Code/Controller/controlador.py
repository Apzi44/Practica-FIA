#Martinez Alor Zaddkiel de Jesus
class Controlador:
    # FUNCIONES INICIALIZACION Y BASICAS
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.vista.boton_crear_conjunto_datos_manualmente.configure(command=self._crear_conjunto_datos_manualmente)
        self.vista.boton_anadir_vector_a_conjunto_datos_manualmente.configure(command=self._anadir_vector_a_conjunto_datos_manualmente)
        self.vista.boton_crear_conjunto_datos_archivo.configure(command=self._crear_conjunto_datos_archivo)
        self.vista.boton_anadir_vector_a_conjunto_datos_archivo.configure(command=self._anadir_vector_a_conjunto_datos_archivo)
        self.vista.boton_anadir_vector_a_conjunto_datos_clasificar_manualmente.configure(command=self._anadir_vector_a_conjunto_datos_clasificar_manualmente)
        self.vista.boton_clasificar_por_distancia_minima.configure(command=self._clasificar_por_distancia_minima)
        self.vista.boton_clasificar_por_knn.configure(command=self._clasificar_por_knn)
        self.vista.boton_borrar_datos_conjunto_datos.configure(command=self._borrar_datos_conjunto_datos)
        self.vista.boton_borrar_datos_clasificar.configure(command=self._borrar_datos_clasificar)
        self.vista.boton_validacion_train_and_test.configure(command=lambda: self._validacion("train_and_test"))
        self.vista.boton_validacion_k_fold.configure(command=lambda: self._validacion("k_fold"))
        self.vista.boton_validacion_bootstrap.configure(command=lambda: self._validacion("bootstrap"))

    # FUNCIONES BORRAR DATOS
    def _borrar_datos_conjunto_datos(self):
        if not self.modelo.verificar_existencia():
            self.vista.mostrar_mensaje("No se tienen datos previamente ingresados", "warning")
            return
        self.modelo.borrar_datos_conjunto_datos()
        self.vista.reiniciar_tabla("conjunto")
        self.vista.boton_crear_conjunto_datos_manualmente.state(['!disabled'])
        self.vista.boton_crear_conjunto_datos_archivo.state(['!disabled'])
        self.vista.mostrar_mensaje("Datos del conjunto de datos borrados exitosamente", "info")

    def _borrar_datos_clasificar(self):
        if self.modelo.datos_clasificar == []:
            self.vista.mostrar_mensaje("No se tienen datos previamente ingresados", "warning")
            return
        self.modelo.borrar_datos_clasificar()
        self.vista.reiniciar_tabla("clasificar")
        self.vista.boton_crear_conjunto_datos_manualmente.state(['!disabled'])
        self.vista.boton_crear_conjunto_datos_archivo.state(['!disabled'])
        self.vista.mostrar_mensaje("Datos del conjunto de clasificar borrados exitosamente", "info")

    # FUNCIONES INGRESION DE DATOS
    def _crear_conjunto_datos_manualmente(self):
        self.vista.crear_ventana_creacion_conjunto_datos()
        self.vista.btn_agregar.configure(command=self.vista.agregar_input)
        self.vista.btn_guardar_conjunto_datos.configure(command=self._crear_conjunto_datos_manualmente_con_vector_entrada)

    def _crear_conjunto_datos_manualmente_con_vector_entrada(self):
        vector_entrada = self.vista.obtener_vector_entrada()
        if vector_entrada in ["Se requiere que los campos no esten vacios", "No se han ingresado entradas", "Se requieren al menos 2 entradas"]:
            self.vista.mostrar_mensaje(vector_entrada, "warning")
            return
        
        self.modelo.crear_conjunto_de_datos_manualmente(vector_entrada)
        self.vista.mostrar_mensaje("Conjunto de datos creado exitosamente", "info")
        self.vista.boton_crear_conjunto_datos_manualmente.state(['disabled'])
        self.vista.boton_crear_conjunto_datos_archivo.state(['disabled'])
        self.vista.ventana_creacion_conjunto_datos.destroy()
        self._mostrar_conjunto_datos("conjunto")

    def _anadir_vector_a_conjunto_datos_manualmente(self):
        if not self.modelo.verificar_existencia():
            self.vista.mostrar_mensaje("No se tienen datos previamente ingresados", "warning")
            return
        self.vista.crear_ventana_anadir_vector_a_conjunto_datos(self.modelo.crear_tupla_atributos())
        self.vista.btn_guardar_conjunto_datos.configure(command=self._anadir_vector_a_conjunto_datos_con_vector_entrada)

    def _anadir_vector_a_conjunto_datos_con_vector_entrada(self):
        vector_entrada = self.vista.obtener_vector_entrada()
        if vector_entrada in ["Se requiere que los campos no esten vacios", "No se han ingresado entradas", "Se requieren al menos 2 entradas"]:
            self.vista.mostrar_mensaje(vector_entrada, "warning")
            return

        resultado = self.modelo.anadir_vector_a_conjunto_de_datos_manualmente(vector_entrada)
        if resultado == "Exito":
            self.vista.mostrar_mensaje("Vector añadido exitosamente", "info")
            self._mostrar_conjunto_datos("conjunto")
        else:
            self.vista.mostrar_mensaje(resultado, "warning")

    def _crear_conjunto_datos_archivo(self):
        archivo = self.vista.preguntar_archivo()
        if archivo:
            separador = self.vista.preguntar_separador()
            if separador:
                resultado = self.modelo.crear_conjunto_de_datos_por_archivo(archivo, separador)
                if resultado == "Exito":
                    self._mostrar_conjunto_datos("conjunto")
                    self.vista.mostrar_mensaje(resultado, "info")
                    self.vista.boton_crear_conjunto_datos_manualmente.state(['disabled'])
                    self.vista.boton_crear_conjunto_datos_archivo.state(['disabled'])
                else:
                    self.vista.mostrar_mensaje(resultado, "warning")
            else:
                self.vista.mostrar_mensaje("No se ingreso ningun separador valido", "warning")
        else:
            self.vista.mostrar_mensaje("No se selecciono ningun archivo", "warning")

    def _anadir_vector_a_conjunto_datos_archivo(self):
        if not self.modelo.verificar_existencia():
            self.vista.mostrar_mensaje("No se tienen datos previamente ingresados", "warning")
            return
        archivo = self.vista.preguntar_archivo()
        if archivo:
            separador = self.vista.preguntar_separador()
            if separador:
                resultado = self.modelo.anadir_datos_a_conjunto_de_datos_por_archivo(archivo, separador)
                if resultado == "Exito":
                    self._mostrar_conjunto_datos("conjunto")
                    self.vista.mostrar_mensaje(resultado, "info")
                else:
                    self.vista.mostrar_mensaje(resultado, "warning")
            else:
                self.vista.mostrar_mensaje("No se ingreso ningun separador valido", "warning")
        else:
            self.vista.mostrar_mensaje("No se selecciono ningun archivo", "warning")

    # FUNCIONES INGRESION DATOS PARA CLASIFICAR
    def _anadir_vector_a_conjunto_datos_clasificar_manualmente(self):
        if not self.modelo.verificar_existencia():
            self.vista.mostrar_mensaje("No se tienen datos ingresados", "warning")
            return

        self.vista.crear_ventana_anadir_vector_a_conjunto_datos_clasificar(self.modelo.crear_tupla_atributos())
        self.vista.btn_guardar_vector.configure(command=self._anadir_vector_a_conjunto_datos_clasificar_manualmente_con_vector_entrada)

    def _anadir_vector_a_conjunto_datos_clasificar_manualmente_con_vector_entrada(self):
        vector_entrada_clasificar = self.vista.obtener_vector_entrada_clasificar()
        if vector_entrada_clasificar in ["Se requiere que los campos de tipo entrada no esten vacios", "Se requiere al menos 2 atributos de tipo entrada", "Se requiere al menos 1 atributo de tipo salida"]:
            self.vista.mostrar_mensaje(vector_entrada_clasificar, "warning")
            return

        resultado = self.modelo.anadir_vector_a_conjunto_de_datos_clasificar(vector_entrada_clasificar)
        if resultado == "Exito":
            self._mostrar_conjunto_datos("clasificar")
            self.vista.mostrar_mensaje(resultado, "info")
        else:
            self.vista.mostrar_mensaje(resultado, "warning")

    # FUNCIONES MOSTRAR DATOS
    def _mostrar_conjunto_datos(self, modalidad):
        self.vista.crear_tabla(self.modelo.regresar_tabla_datos(modalidad), self.modelo.retornar_nombre_atributos(), modalidad)

    # FUNCIONES CLASIFICACION
    def _clasificar_por_distancia_minima(self):
        if not self.modelo.verificar_existencia():
            self.vista.mostrar_mensaje("No se tienen datos ingresados", "warning")
            return

        if self.modelo.datos_clasificar == []:
            self.vista.mostrar_mensaje("No se tienen datos para clasificar", "warning")
            return

        usar_manhattan = self.vista.preguntar_usar_manhattan()
        if usar_manhattan is None:
            return

        self.modelo.aplicar_aprendizaje_por_distancia_minima(usar_manhattan)
        self._mostrar_conjunto_datos("clasificar")
        self.vista.mostrar_mensaje("Exito", "info")

    def _clasificar_por_knn(self):
        if not self.modelo.verificar_existencia():
            self.vista.mostrar_mensaje("No se tienen datos ingresados", "warning")
            return
        
        if self.modelo.datos_clasificar == []:
            self.vista.mostrar_mensaje("No se tienen datos para clasificar", "warning")
            return

        usar_manhattan = self.vista.preguntar_usar_manhattan()
        if usar_manhattan is None:
            return

        k = self.vista.preguntar_k(self.modelo.no_filas)
        if k is None:
            return

        self.modelo.aplicar_aprendizaje_por_knn(k, usar_manhattan)
        self._mostrar_conjunto_datos("clasificar")
        self.vista.mostrar_mensaje("Exito", "info")

    # FUNCIONES VALIDACION
    def _validacion(self, algoritmo):
        if not self.modelo.verificar_existencia():
            self.vista.mostrar_mensaje("No se tienen datos ingresados", "warning")
            return

        texto = "No se tienen datos suficientes para realizar validacion {algoritmo}"
        if self.modelo.no_filas < 2:
            self.vista.mostrar_mensaje(texto.format(algoritmo=algoritmo), "warning")
            return

        self.vista.crear_ventana_seleccionar_atributos(self.modelo.crear_tupla_atributos())

        if algoritmo == "train_and_test":
            self.vista.btn_seleccionar_atributos.configure(command=lambda: self._validacion_train_and_test())
        elif algoritmo == "k_fold":
            self.vista.btn_seleccionar_atributos.configure(command=lambda: self._validacion_k_fold())
        elif algoritmo == "bootstrap":
            self.vista.btn_seleccionar_atributos.configure(command=lambda: self._validacion_bootstrap())

    def _validacion_train_and_test(self):
        atributos = self.vista.obtener_atributos()
        # Se obtienen los atributos seleccionados
        if atributos in ["Se requiere al menos 2 atributos de tipo entrada", "Se requiere al menos 1 atributo de tipo salida"]:
            self.vista.mostrar_mensaje(atributos, "warning")
            return

        self.vista.ventana_seleccionar_atributos.destroy()

        porcentaje = self.vista.preguntar_porcentaje()
        # Se pregunta el porcentaje de entrenamiento
        if porcentaje is None:
            return

        usar_knn, k, usar_manhattan = self._preguntar_usar_knn_o_manhattan()
        if usar_knn is None:
            return
        
        tupla_resultados=self.modelo.validar_con_train_and_test(atributos, porcentaje, usar_knn, k, usar_manhattan)
        self._mostrar_conjunto_datos("clasificar")
        self.vista.mostrar_resultados_train_and_test(tupla_resultados)
        self.vista.mostrar_mensaje("Exito", "info")
    
    def _validacion_k_fold(self):
        atributos = self.vista.obtener_atributos()
        # Se obtienen los atributos seleccionados
        if atributos in ["Se requiere al menos 2 atributos de tipo entrada", "Se requiere al menos 1 atributo de tipo salida"]:
            self.vista.mostrar_mensaje(atributos, "warning")
            return

        self.vista.ventana_seleccionar_atributos.destroy()

        k_divisiones = self.vista.preguntar_k_divisiones(self.modelo.no_filas)
        # Se pregunta el valor de k
        if k_divisiones is None:
            return

        usar_knn, k, usar_manhattan = self._preguntar_usar_knn_o_manhattan()
        if usar_knn is None:
            return
        
        lista_resultados = self.modelo.validar_con_k_fold_cross_validation(atributos, k_divisiones, usar_knn, k, usar_manhattan)
        self._mostrar_conjunto_datos("clasificar")
        self.vista.mostrar_resultados_k_fold_cross_validation(lista_resultados)
        self.vista.mostrar_mensaje("Exito", "info")
    
    def _validacion_bootstrap(self):
        atributos = self.vista.obtener_atributos()
        # Se obtienen los atributos seleccionados
        if atributos in ["Se requiere al menos 2 atributos de tipo entrada", "Se requiere al menos 1 atributo de tipo salida"]:
            self.vista.mostrar_mensaje(atributos, "warning")
            return

        self.vista.ventana_seleccionar_atributos.destroy()

        cantidad_experimentos = self.vista.preguntar_cantidad_experimentos()
        # Se pregunta el valor de k
        if cantidad_experimentos is None:
            return

        cantidad_muestras_aprendizaje = self.vista.preguntar_cantidad_muestras_aprendizaje(self.modelo.no_filas)
        # Se pregunta el valor de k
        if cantidad_muestras_aprendizaje is None:
            return

        cantidad_muestras_clasificacion = self.vista.preguntar_cantidad_muestras_clasificacion(self.modelo.no_filas)
        # Se pregunta el valor de k
        if cantidad_muestras_clasificacion is None:
            return

        if cantidad_muestras_aprendizaje + cantidad_muestras_clasificacion > self.modelo.no_filas:
            self.vista.mostrar_mensaje("No se pueden seleccionar mas muestras de las disponibles", "warning")
            return

        usar_knn, k, usar_manhattan = self._preguntar_usar_knn_o_manhattan()
        if usar_knn is None:
            return
        
        lista_resultados = self.modelo.validar_con_bootstrap(atributos, cantidad_experimentos, cantidad_muestras_aprendizaje, 
        cantidad_muestras_clasificacion, usar_knn, k, usar_manhattan)
        self._mostrar_conjunto_datos("clasificar")
        self.vista.mostrar_resultados_bootstrap(lista_resultados)
        self.vista.mostrar_mensaje("Exito", "info")

    def _preguntar_usar_knn_o_manhattan(self):
        usar_knn = self.vista.preguntar_algoritmo()
        # Se pregunta si se desea usar KNN
        if usar_knn is None:
            return None, None, None
        
        k = None
        # Se pregunta el valor de k si se usa KNN
        if usar_knn:
            k = self.vista.preguntar_k(self.modelo.no_filas)
            if k is None:
                return None, None, None
        # Se pregunta si se desea usar Manhattan
        usar_manhattan = self.vista.preguntar_usar_manhattan()
        if usar_manhattan is None:
            return None, None, None
        
        return usar_knn, k, usar_manhattan
        