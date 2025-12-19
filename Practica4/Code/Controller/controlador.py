
class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.vista.boton_cargar_datos.configure(command= lambda: self._cargar_datos("inicial"))
        self.vista.boton_reiniciar_datos.configure(command=self._reiniciar_datos)
        self.vista.boton_borrar_datos.configure(command=self._borrar_datos)
        self.vista.boton_anadir_datos.configure(command= lambda: self._cargar_datos("anadir"))
        self.vista.boton_eleccion_subconjunto_uno_por_uno.configure(command= self._subconjunto_uno_por_uno)
        self.vista.boton_eleccion_subconjunto_por_rango.configure(command= self._subconjunto_por_intervalo)
        self.vista.boton_eleccion_subconjunto_por_atributo.configure(command= self._subconjunto_por_atributos)
        self.vista.boton_eleccion_subconjunto_por_valor_de_atributo.configure(command= self._subconjunto_por_valor_de_atributo)

    def _cargar_datos(self, modalidad= "inicial"):
        if  modalidad != "inicial":
            if not self.modelo.verificar_existencia():
                self.vista.mostrar_mensaje("No se han cargado datos", "warning")
                return

        archivo = self.vista.preguntar_archivo()
        if archivo:
            separador = self.vista.preguntar_separador()
            if separador:
                mensaje, exito = self.modelo.cargar_datos(archivo, separador, modalidad)
                if exito == True:
                    self._actualizar_tabla()
                    self.vista.mostrar_mensaje(mensaje, "info")
                    if modalidad == "inicial":
                        self.vista.boton_cargar_datos.state(['disabled'])
                else:
                    self.vista.mostrar_mensaje(mensaje, "warning")
            else:
                self.vista.mostrar_mensaje("No se ingreso ningun separador valido", "warning")
        else:
            self.vista.mostrar_mensaje("No se selecciono ningun archivo", "warning")

    def _actualizar_tabla(self):
        datos_cualitativos = self.modelo.obtener_datos_cualitativos()
        datos_cuantitativos = self.modelo.obtener_datos_cuantitativos()
        self.vista.mostrar_datos_tabla(datos_cualitativos, datos_cuantitativos, self.modelo.nombre_atributos_actuales)

        datos= self.modelo.obtener_datos_valores()
        self.vista.crear_tabla(datos, self.modelo.nombre_atributos_actuales)

    def _reiniciar_datos(self):
        if self.modelo.verificar_existencia():
            self.modelo.reiniciar_datos()
            self._actualizar_tabla()
            self.vista.mostrar_mensaje("Datos reiniciados exitosamente", "info")
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")

    def _borrar_datos(self):
        if self.modelo.verificar_existencia():
            self.modelo.borrar_datos()
            self.vista.destruir_tabla()
            self.vista.boton_cargar_datos.state(['!disabled'])
            self.vista.mostrar_mensaje("Datos borrados exitosamente", "info")
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")

    def _subconjunto_uno_por_uno(self):
        if self.modelo.verificar_existencia():
            filas = self.vista.pedir_filas(*self.modelo.obtener_indice_menor_y_mayor())
            if filas:
                self.modelo.subconjunto_uno_por_uno(filas)
                try:
                    self._actualizar_tabla()
                except Exception:
                    pass

                self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")

    def _subconjunto_por_intervalo(self):
        if self.modelo.verificar_existencia():
            intervalo = self.vista.pedir_intervalo(*self.modelo.obtener_indice_menor_y_mayor())
            if intervalo:
                self.modelo.subconjunto_por_intervalo(intervalo)
                self._actualizar_tabla()

                self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
                self._actualizar_tabla()
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")

    def _subconjunto_por_atributos(self):
        if self.modelo.verificar_existencia():
            atributos = self.vista.pedir_atributos()
            if atributos:
                resultado, atributos_pendientes = self.modelo.verificar_atributos(atributos)
                if resultado:
                    self.modelo.subconjunto_por_atributos(atributos)
                    self._actualizar_tabla()

                    self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
                else:
                    self.vista.mostrar_mensaje("El atributo " + atributos_pendientes + " no se encuentra en el archivo", "warning")
            else:
                self.vista.mostrar_mensaje("No se ha seleccionado ningun atributo", "warning")
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")

    def _subconjunto_por_valor_de_atributo(self):
        if self.modelo.verificar_existencia():
            atributo = self.vista.pedir_atributo_o_clase()
            if self.modelo.verificar_atributo_o_clase(atributo):
                valor = self.vista.pedir_valor_atributo(atributo)
                if valor:
                    mensaje = self.modelo.subconjunto_valor_de_atributo(atributo, valor)
                    if mensaje == "Exito":
                        self._actualizar_tabla()
                        self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
                    else:
                        self.vista.mostrar_mensaje(mensaje, "warning")
                else:
                    self.vista.mostrar_mensaje("No se ha seleccionado ningun valor", "warning")
            else:
                self.vista.mostrar_mensaje("El atributo " + atributo + " no se encuentra en el archivo", "warning")
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")