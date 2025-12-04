
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
        self.vista.boton_eleccion_subconjunto_uno_por_uno.configure(command= lambda: self._subconjunto_uno_por_uno(self.modelo.no_filas[1]))
        self.vista.boton_eleccion_subconjunto_por_rango.configure(command= lambda: self._subconjunto_por_intervalo(self.modelo.no_filas[1]))
        self.vista.boton_eleccion_subconjunto_por_atributo.configure(command= lambda: self._subconjunto_por_atributo())
        self.vista.boton_eleccion_subconjunto_por_varios_atributos.configure(command= lambda: self._subconjunto_por_atributos())

    def _cargar_datos(self, modalidad= "inicial"):
        archivo = self.vista.preguntar_archivo()
        if archivo:
            separador = self.vista.preguntar_separador()
            if separador:
                mensaje, exito = self.modelo.cargar_datos(archivo, separador, modalidad)
                if exito == True:
                    self._actualizar_tabla()
                    self.vista.mostrar_mensaje(mensaje, "info")
                else:
                    self.vista.mostrar_mensaje(mensaje, "warning")
            else:
                self.vista.mostrar_mensaje("No se ingreso ningun separador valido", "warning")
        else:
            self.vista.mostrar_mensaje("No se selecciono ningun archivo", "warning")

    def _actualizar_tabla(self):
        datos_cualitativos, datos_cuantitativos = self.modelo.obtener_datos_cuantitativos_cualitativos()
        self.vista.mostrar_datos_tabla(datos_cualitativos, datos_cuantitativos, len(datos_cualitativos), len(datos_cuantitativos))
        
        datos= self.modelo.obtener_datos_valores()
        self.vista.crear_tabla(datos)

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
            self.vista.mostrar_mensaje("Datos borrados exitosamente", "info")
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")

    def _subconjunto_uno_por_uno(self, no_filas):
        if self.modelo.verificar_existencia():
            filas = self.vista.pedir_filas(no_filas)
            if filas:
                self.modelo.subconjunto_uno_por_uno(filas)
                
                datos_cualitativos, datos_cuantitativos = self.modelo.obtener_datos_cuantitativos_cualitativos()
                self.vista.mostrar_datos_tabla(datos_cualitativos, datos_cuantitativos, len(datos_cualitativos), len(datos_cuantitativos))
                
                self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
                self._actualizar_tabla()
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")

    def _subconjunto_por_intervalo(self, no_filas):
        if self.modelo.verificar_existencia():
            intervalo = self.vista.pedir_intervalo(no_filas)
            if intervalo:
                self.modelo.subconjunto_por_intervalo(intervalo)
                
                datos_cualitativos, datos_cuantitativos = self.modelo.obtener_datos_cuantitativos_cualitativos()
                self.vista.mostrar_datos_tabla(datos_cualitativos, datos_cuantitativos, len(datos_cualitativos), len(datos_cuantitativos))
                
                self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
                self._actualizar_tabla()
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")

    def _subconjunto_por_atributo(self):
        if self.modelo.verificar_existencia():
            atributo = self.vista.pedir_atributo()
            if atributo:
                resultado, atributos_pendientes = self.modelo.verificar_atributo([atributo])
                if resultado:
                    self.modelo.subconjunto_atributo([atributo])
                    
                    datos_cualitativos, datos_cuantitativos = self.modelo.obtener_datos_cuantitativos_cualitativos()
                    self.vista.mostrar_datos_tabla(datos_cualitativos, datos_cuantitativos, len(datos_cualitativos), len(datos_cuantitativos))
                    
                    self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
                    self._actualizar_tabla()
                else:
                    self.vista.mostrar_mensaje("El atributo " + atributos_pendientes + " no se encuentra en el archivo", "warning")
            else:
                self.vista.mostrar_mensaje("No se ha seleccionado ningun atributo", "warning")
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")

    def _subconjunto_por_atributos(self):
        if self.modelo.verificar_existencia():
            atributos = self.vista.pedir_atributos()
            if atributos:
                resultado, atributos_pendientes = self.modelo.verificar_atributo(atributos)
                if resultado:
                    self.modelo.subconjunto_atributo(atributos)
                    
                    datos_cualitativos, datos_cuantitativos = self.modelo.obtener_datos_cuantitativos_cualitativos()
                    self.vista.mostrar_datos_tabla(datos_cualitativos, datos_cuantitativos, len(datos_cualitativos), len(datos_cuantitativos))
                    
                    self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
                    self._actualizar_tabla()
                else:
                    self.vista.mostrar_mensaje("El atributo " + atributos_pendientes + " no se encuentra en el archivo", "warning")
            else:
                self.vista.mostrar_mensaje("No se ha seleccionado ningun atributo", "warning")
        else:
            self.vista.mostrar_mensaje("No se han cargado datos", "warning")
