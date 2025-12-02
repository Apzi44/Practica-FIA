
class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.vista.boton_cargar_datos.configure(command=self._cargar_datos)
        self.vista.boton_reiniciar_datos.configure(command=self._reiniciar_datos)
        self.vista.boton_borrar_datos.configure(command=self._borrar_datos)
        self.vista.boton_eleccion_subconjunto_uno_por_uno.configure(command= lambda: self._subconjunto_uno_por_uno(self.modelo.no_filas[1]))
        self.vista.boton_eleccion_subconjunto_por_rango.configure(command= lambda: self._subconjunto_por_intervalo(self.modelo.no_filas[1]))

    def _cargar_datos(self):
        archivo = self.vista.preguntar_archivo()
        if archivo:
            separador = self.vista.preguntar_separador()
            if separador:
                mensaje, exito = self.modelo.cargar_datos(archivo, separador)
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
        datos = self.modelo.obtener_datos_valores()
        datos_cualitativos = self.modelo.obtener_datos_cualitativos()
        datos_cuantitativos = self.modelo.obtener_datos_cuantitativos()
        self.vista.mostrar_datos_tabla(datos_cualitativos, datos_cuantitativos)
        self.vista.crear_tabla(datos)

    def _reiniciar_datos(self):
        self.modelo.reiniciar_datos()
        self._actualizar_tabla()
        self.vista.mostrar_mensaje("Datos reiniciados exitosamente", "info")

    def _borrar_datos(self):
        self.modelo.borrar_datos()
        self.modelo.borrar_tabla()
        self.vista.mostrar_mensaje("Datos borrados exitosamente", "info")

    def _subconjunto_uno_por_uno(self, no_filas):
        filas = self.vista.pedir_filas(no_filas)
        if filas:
            self.modelo.subconjunto_uno_por_uno(filas)
            self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
            self._actualizar_tabla()
        else:
            self.vista.mostrar_mensaje("No se selecciono ningun archivo", "warning")
    
    def _subconjunto_por_intervalo(self, no_filas):
        intervalo = self.vista.pedir_intervalo(no_filas)
        if intervalo:
            self.modelo.subconjunto_por_intervalo(intervalo)
            self.vista.mostrar_mensaje("Subconjunto creado exitosamente", "info")
            self._actualizar_tabla()
        else:
            self.vista.mostrar_mensaje("No se selecciono ningun archivo", "warning")