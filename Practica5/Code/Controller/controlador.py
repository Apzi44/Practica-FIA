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