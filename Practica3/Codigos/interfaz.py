import time
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap, BoundaryNorm
import mapa as mp
from agente import AgenteP, AgenteAxel, AgenteAbad, Agente
import Coordenada as Coordenada
from math import isinf
import copy

class Interfaz(ttk.Window):
    colorTerrenoBinario = {
        0: "#343434",
        1: "#FFFFFF",
    }
    colorTerrenoBinario.setdefault(-1, "#000000")  # Rojo para valores -1

    colorTerrenoMixto = {
        0: "#515151", #Montaña
        1: "#4682B4", #Agua
        2: "#228B22", #Bosque
        3: "#F8E268", #Arena
        4: "#F5D198", #Tierra
        5: "#74216B", #Pantano
        6: "#BDBBBB", #Nieve
    }
    colorTerrenoMixto.setdefault(-1, "#000000")  # Rojo para valores -1

    # FUNCIONES DE INTERFAZ
    def __init__(self):
        self.mapa = None
        self.agente = None
        self.modoUsuario = None
        self.estiloSeccionConsultar = "SUCCESS"
        self.estiloBotonesControlInterfaz = "PRIMARY"
        self.estiloSeccionModificar = "DANGER"
        self.estiloSeccionControlesAgente = "INFO"
        self.estiloSeccionAlgBusqueda = "WARNING"
        self.configuracionesIniciales()
        self.crear_layout()
        self.mainloop()

    def configuracionesIniciales(self):
        super().__init__(themename="cyborg")
        self.title("Mapa Interactivo")
        self._anchoVentana = 1800
        self._altoVentana = 950
        self.geometry(f"{self._anchoVentana}x{self._altoVentana}")
        self.resizable(True, True)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)
    
    def crear_layout(self):
        self.crearPaneles()
        self.crearBotonesControlInterfaz()
        self.crearSeccionConsultar()
        self.crearSeccionModificar()
        self.crearSeccionControlesAgente()
        self.crearSeccionAlgBusqueda()

    def crearPaneles(self):
        self.panelControl = ttk.Frame(self, padding=10, bootstyle="DARK", width=400)
        self.panelControl.grid_propagate(False)
        self.panelControl.grid(row=0, column=0, sticky="nsew")
        for i in range(5):
            self.panelControl.rowconfigure(i, weight=0)
        self.panelControl.columnconfigure(0, weight=1)
        self.labelTitularControl= ttk.Label(self.panelControl, text="OPCIONES DE INTERFAZ BASE", font=("Arial", 18, "bold"), wraplength=300, anchor="center", justify="center")
        self.labelTitularControl.grid(row=0, column=0, pady=10, ipadx=10, sticky="nsew")

        # Panel derecho (mapa)
        self.panelMapa = ttk.Frame(self, bootstyle=LIGHT)
        self.panelMapa.grid(row=0, column=1, sticky="nsew")
        self.panelMapa.grid_propagate(False)

        # Panel busquedas
        self.panelAgente = ttk.Frame(self, padding=10, bootstyle="DARK", width=400)
        self.panelAgente.grid(row=0, column=2, sticky="nsew")
        self.panelAgente.grid_propagate(False)
        for i in range(3):
            self.panelAgente.rowconfigure(i, weight=0)
        self.panelAgente.columnconfigure(0, weight=1)
        self.labelTitularAgente= ttk.Label(self.panelAgente, text="OPCIONES DE AGENTE", font=("Arial", 18, "bold"), wraplength=300, anchor="center", justify="center")
        self.labelTitularAgente.grid(row=0, column=0, pady=10, ipadx=10, sticky="nsew")
    
    def crearBotonesControlInterfaz(self):
        estiloBotones = self.estiloBotonesControlInterfaz + "-OUTLINE"
        self.marcoBotonesControl = ttk.Labelframe( self.panelControl, text="Controles de interfaz", padding=10, bootstyle=self.estiloBotonesControlInterfaz)
        self.marcoBotonesControl.grid(row=1, column=0, pady=15, sticky="nsew")
        for i in range(5):
            self.marcoBotonesControl.rowconfigure(i, weight=1)
        self.marcoBotonesControl.columnconfigure(0, weight=1)
        
        self.botonCargarMapa = ttk.Button( self.marcoBotonesControl, text="Cargar Mapa", bootstyle=estiloBotones,command=self.cargar_mapa)
        self.botonCrearAgente = ttk.Button( self.marcoBotonesControl, text="Crear Agente", bootstyle=estiloBotones,command=self.cargar_agente)
        self.botonModoDios = ttk.Button( self.marcoBotonesControl, text="Modo Dios", bootstyle=estiloBotones, command= self.activarModoDios)
        self.botonDesModoDios = ttk.Button( self.marcoBotonesControl, text="Desactivar Modo Dios", bootstyle=estiloBotones, command= self.desactivarModoDios)
        self.botonBorrarCompleto = ttk.Button( self.marcoBotonesControl, text="Borrar Mapa y Agente", bootstyle=estiloBotones, command= self.borrarTodo)

        self.botonCargarMapa.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        self.botonCrearAgente.grid(row=1, column=0, pady=10, padx=10,sticky="nsew")
        self.botonModoDios.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
        self.botonDesModoDios.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
        self.botonBorrarCompleto.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")

    def crearSeccionConsultar(self):
        # Creacion del marco para obtener valor
        self.marco = ttk.Labelframe( self.panelControl, text="Consultar coordenada", padding=10, bootstyle=self.estiloSeccionConsultar)
        self.marco.grid(row=2, column=0, pady=15, sticky="nsew")
        for i in range(4):
            self.marco.rowconfigure(i, weight=0)
        self.marco.columnconfigure(0, weight=1)
        # Entradas y etiquetas
        self.x_get = ttk.Entry(self.marco, bootstyle=self.estiloSeccionConsultar)
        self.y_get = ttk.Entry(self.marco, bootstyle=self.estiloSeccionConsultar)
        self.x_get.insert(0, "A")
        self.y_get.insert(0, "1")
        self._labelXget=ttk.Label(self.marco, text="X (letra)")
        self._labelYget=ttk.Label(self.marco, text="Y (número)")
        # Posicionamiento en grid
        self._labelXget.grid(row=0, column=0, pady=5)
        self._labelYget.grid(row=1, column=0, pady=5)
        self.x_get.grid(row=0, column=1, pady=5)
        self.y_get.grid(row=1, column=1, pady=5)
        # Boton obtener valor y resultado
        boton_obtener = ttk.Button( self.marco, text="Obtener valor", bootstyle=self.estiloSeccionConsultar, command= self.obtenerValorCoordenada)
        boton_obtener.grid(row=2, column=0, columnspan=2, pady=5)
        # Etiqueta resultado
        self.labelObtener = ttk.Label(self.marco, text="Valor: -", font=("Segoe UI", 12))
        self.labelObtener.grid(row=3, column=0, columnspan=2, pady=5)

    def crearSeccionModificar(self):
        # Creacion del marco para modificar valor
        marco = ttk.Labelframe( self.panelControl, text="Modificar coordenada", padding=10, bootstyle=self.estiloSeccionModificar)
        marco.grid(row=3, column=0, pady=15, sticky="nsew")
        for i in range(4):
            marco.rowconfigure(i, weight=0)
        marco.columnconfigure(0, weight=1)
        # Entradas y etiquetas
        self.x_mod = ttk.Entry(marco, bootstyle=self.estiloSeccionModificar)
        self.y_mod = ttk.Entry(marco, bootstyle=self.estiloSeccionModificar)
        self.val_mod = ttk.Entry(marco, bootstyle=self.estiloSeccionModificar)
        self.x_mod.insert(0, "A")
        self.y_mod.insert(0, "1")
        self.val_mod.insert(0, "0")
        self._labelXmod=ttk.Label(marco, text="X (letra)")
        self._labelYmod=ttk.Label(marco, text="Y (número)")
        self._labelValmod=ttk.Label(marco, text="Nuevo valor")
        # Posicionamiento en grid
        self._labelXmod.grid(row=0, column=0, pady=5)
        self._labelYmod.grid(row=1, column=0, pady=5)
        self._labelValmod.grid(row=2, column=0, pady=5)
        self.x_mod.grid(row=0, column=1, pady=5)
        self.y_mod.grid(row=1, column=1, pady=5)
        self.val_mod.grid(row=2, column=1, pady=5)
        # Boton modificar valor
        boton_modificar = ttk.Button( marco, text="Modificar valor", bootstyle=self.estiloSeccionModificar, command=self.modificarValorCoordenada)
        boton_modificar.grid(row=3, column=0, columnspan=2, pady=5)

    def crearSeccionControlesAgente(self):
        self.marcoControles = ttk.Labelframe( self.panelAgente, text="Controles del agente", padding=10, bootstyle=self.estiloSeccionControlesAgente)
        self.marcoControles.grid(row=1, column=0, pady=8, sticky="nsew")
        for i in range(4): self.marcoControles.rowconfigure(i, weight=1)
        for i in range(2): self.marcoControles.columnconfigure(i, weight=1)
        self.labelControles = ttk.Label(self.marcoControles, text="Crea un agente para ver los controles", font=("Segoe UI", 10), wraplength=300)
        self.labelControles.grid(row=0, column=0, columnspan=2, pady=10)
        self.labelCosto = ttk.Label(self.marcoControles, text="Costo: 0", font=("Segoe UI", 12))
        self.labelCosto.grid(row = 3, column = 0, columnspan = 2, pady = 5)

    def crearSeccionAlgBusqueda(self):
        self.marcoBusqueda = ttk.Labelframe( self.panelAgente, text="Busqueda de ruta", padding=10, bootstyle=self.estiloSeccionAlgBusqueda)
        self.marcoBusqueda.grid(row=2, column=0, pady=8, sticky="nsew")
        for i in range(9): self.marcoBusqueda.rowconfigure(i, weight=1)
        for i in range(2): self.marcoBusqueda.columnconfigure(i, weight=1)
        self.labelBusqueda = ttk.Label(self.marcoBusqueda, text="Crea un agente para ver las opciones de busqueda, el unico disponible es el Agente Abad", font=("Segoe UI", 10), wraplength=300)
        self.labelBusqueda.grid(row=0, column=0, columnspan=2, pady=10)

    def activarModoDios(self):
        if not self.mapa:
            messagebox.showinfo("Error", "Carga un mapa primero.")
            return
        if self.modoUsuario == None:
            self.modoUsuario = "Dios"
            self.botonCrearAgente.config(state=DISABLED)
            for i in range(self.mapa.alto):
                for j in range(self.mapa.ancho):
                    coord: Coordenada= self.mapa.obtenerCoordenada(j,i)
                    coord.visible= True
            self.dibujar_mapa()
        elif self.modoUsuario == "Dios":
            messagebox.showinfo("Modo dios", "El modo dios ya está activado.")
        elif self.modoUsuario == "Agente":
            messagebox.showinfo("Agente activado", "No puedes activar el modo dios debido a que ya tienes un agente en el mapa, intenta borrar todo o cambiar de mapa.")

    def desactivarModoDios(self):
        if not self.mapa:
            messagebox.showinfo("Error", "Carga un mapa primero.")
            return
        if self.modoUsuario == "Dios":
            self.modoUsuario = None
            self.botonCrearAgente.config(state=NORMAL)
            for i in range(self.mapa.alto):
                for j in range(self.mapa.ancho):
                    coord: Coordenada= self.mapa.obtenerCoordenada(j,i)
                    coord.visible= False
            self.dibujar_mapa()
        elif self.modoUsuario == None:
            messagebox.showinfo("Error", "El modo dios ya está desactivado.")
        elif self.modoUsuario == "Agente":
            messagebox.showinfo("Agente activado", "No puedes desactivar el modo dios debido a que tienes un agente en el mapa y por ende el modo dios está desactivado, intenta borrar todo o cambiar de mapa.")

    def borrarTodo(self):
        if self.mapa:
            self.mapa = None
            for widget in self.panelMapa.winfo_children():
                widget.destroy()
        if self.agente:
            self.agente = None
        for widget in self.marcoControles.winfo_children():
            widget.destroy()
        for widget in self.marcoBusqueda.winfo_children():
            widget.destroy()
            
        self.crearSeccionControlesAgente()
        self.crearSeccionAlgBusqueda()
        self.modoUsuario = None

    # Funcion para obtener y actualizar el costo
    def actualizar_costo(self):
        if self.agente:
            costo_actual = self.agente.coste
            self.labelCosto.config(text=f"Costo: {costo_actual}")

    def analizarFinalizacion(self):
        if self.agente:
            coordenadaAnalizar = self.mapa.obtenerCoordenada(self.agente.posicion_x, self.agente.posicion_y)
            if coordenadaAnalizar.puntoClave == "F":
                messagebox.showinfo("¡Felicidades!", f"El agente ha llegado a la meta con un costo total de {self.agente.coste}.")
                # Deshabilitar los botones de control
                for i in self.listaBotonesAgente:
                    i.config(state=DISABLED)

    # FUNCIONES DE CARGA DE MAPA Y AGENTE
    def cargar_mapa(self): 
        respuesta = messagebox.askyesno("Instrucciones", "Desea cargar un archivo para el mapa base?")
        if respuesta == False:
            return
        else: 
            archivo= filedialog.askopenfilename(title="Seleccione el archivo", filetypes= [
            ("Archivos de texto y csv", "*.txt; *.csv"),
            ("Archivos de texto", "*.txt"),
            ("Archivos CSV", "*.csv")])
            if not archivo: return
            else: 
                self.mapa= mp.Mapa()
                bandera= self.mapa.leerArchivo(archivo)
                if bandera == False: 
                    messagebox.showinfo("Error", "No se pudo cargar el mapa, intente de nuevo. El mapa anterior se mantuvo.")
                    return
                else:
                    if self.agente:
                        for widget in self.marcoControles.winfo_children():
                            widget.destroy()
                        for widget in self.marcoBusqueda.winfo_children():
                            widget.destroy()
                        self.crearSeccionControlesAgente()
                        self.crearSeccionAlgBusqueda()
                        self.agente= None
                    self.modoUsuario= None
                    if self.botonCrearAgente:
                        self.botonCrearAgente.config(state=NORMAL)
        if self.mapa:
            self.dibujar_mapa()
    
    def cargar_agente(self):
        if self.mapa== None:
            messagebox.showinfo("Error", "Carga un mapa primero.")
            return
        ventanaCarga= ttk.Toplevel(self)
        ventanaCarga.title("Cargar Agente")
        ventanaCarga.geometry("400x500")
        ventanaCarga.resizable(False, False)
        for i in range(2): ventanaCarga.columnconfigure(i, weight=1)
        for i in range(6): ventanaCarga.rowconfigure(i, weight=1)
        labelTitulo= ttk.Label(ventanaCarga, text="Creacion de agente", font=("Arial", 14, "bold"))
        labelSubtitulo= ttk.Label(ventanaCarga, text="Ingrese los datos del agente", font=("Arial", 10))
        labelTipoAgente= ttk.Label(ventanaCarga, text="Tipo de agente:")
        entryTipoAgente= ttk.Combobox(ventanaCarga, values=["Agente p", "Agente Axel", "Agente Abad"], state="readonly")
        labelTipoCriatura= ttk.Label(ventanaCarga, text="Tipo de criatura:")
        entryTipoCriatura= ttk.Combobox(ventanaCarga, values=["Humano", "Mono", "Pulpo", "Pie grande", "SuperSayayin"], state="readonly")
        entryTipoAgente.current(0)
        entryTipoCriatura.current(0)
        labelPosInicial= ttk.Label(ventanaCarga, text="Posicion inicial (X,Y):")
        entryPosX= ttk.Entry(ventanaCarga)
        entryPosY= ttk.Entry(ventanaCarga)
        labelPosFinal= ttk.Label(ventanaCarga, text="Punto de meta (X,Y):")
        entryPosEndX = ttk.Entry(ventanaCarga)
        entryPosEndY = ttk.Entry(ventanaCarga)
        botonCrearAgente = ttk.Button(ventanaCarga, text="Crear Agente", bootstyle="INFO-OUTLINE", command= lambda: self.crearAgente(ventanaCarga,entryTipoAgente.get(), entryTipoCriatura.get(), entryPosX.get(), entryPosY.get(), entryPosEndX.get(), entryPosEndY.get()))
        labelTitulo.grid(row=0, column=0, columnspan=2, pady=10)
        labelSubtitulo.grid(row=1, column=0, columnspan=2, pady=5)
        labelTipoAgente.grid(row=2, column=0, pady=5)
        entryTipoAgente.grid(row=2, column=1, pady=5)
        labelTipoCriatura.grid(row=3, column=0, pady=5)
        entryTipoCriatura.grid(row=3, column=1, pady=5)
        labelPosInicial.grid(row=4, column=0, pady=5)
        entryPosX.grid(row=4, column=1, pady=5)
        entryPosY.grid(row=5, column=1, pady=5)
        labelPosFinal.grid(row=6, column=0, pady=5)
        entryPosEndX.grid(row=6, column=1, pady=5)
        entryPosEndY.grid(row=7, column=1, pady=5)
        botonCrearAgente.grid(row=8, column=0, columnspan=2, pady=10)

    # FUNCIONES DE CREACION DE AGENTE
    def analizarCasilla(self, x, y, tipoCriatura):
        CoordenadaAnalizar: Coordenada= self.mapa.obtenerCoordenada(x,y)
        calculoCosto = Agente.calcularCosto(self, CoordenadaAnalizar.valor, tipoCriatura, self.mapa.tipoMapa)
        if isinf(calculoCosto):
            return False
        return True

    def crearAgente(self, ventana, tipo, criatura, posX= "A", posY="0", posXEnd="A",posYEnd="0"  ):
        try:
            if not self.mapa:
                raise ValueError("Error: Carga un mapa primero.")
            
            x,y, _, = self.cambioTipoValoresEntrada(posX, posY)
            xEnd,yEnd, _= self.cambioTipoValoresEntrada(posXEnd, posYEnd)
            if self.mapa.alto <= y or self.mapa.ancho <= x or x < 0 or y < 0:
                raise IndexError("Coordenadas de inicio fuera de los límites del mapa.")
            if self.mapa.alto <= yEnd or self.mapa.ancho <= xEnd or xEnd<0 or yEnd<0:
                raise IndexError("Coordenadas de final fuera de los límites del mapa.")
            if x == xEnd and y == yEnd:
                raise ValueError("Las coordenadas de inicio y final deben ser diferentes.")
            
            CoordenadaInicio = self.mapa.obtenerCoordenada(x, y)
            CoordenadaFinal: Coordenada= self.mapa.obtenerCoordenada(xEnd, yEnd)
            
            if CoordenadaInicio.avanzable == False:
                raise ValueError("La coordenada inicial no es avanzable por tanto el agente no puede iniciar ahí.")
            
            if CoordenadaFinal.avanzable == False:
                raise ValueError("La coordenada final no es avanzable por tanto el agente no puede finalizar ahí.")

            if self.analizarCasilla(x, y, criatura) == False:
                raise ValueError("La coordenada inicial no es seleccionable por el tipo de criatura seleccionada.")
            if self.analizarCasilla(xEnd, yEnd, criatura) == False:
                raise ValueError("La coordenada final no es seleccionable por el tipo de criatura seleccionada.")
            if self.agente:
                self.agente = None
                for widget in self.marcoControles.winfo_children():
                    widget.destroy()
                for i in range(self.mapa.alto):
                    for j in range(self.mapa.ancho):
                        coord: Coordenada= self.mapa.obtenerCoordenada(j,i)
                        coord.puntoClave= None
                        coord.visitado= False
                        coord.visible= False
                        coord.costoViaje= None
                        coord.puntoActual= False
                        coord.puntoDecision= False
            
            if self.modoUsuario == "Dios":
                for i in range(self.mapa.alto):
                    for j in range(self.mapa.ancho):
                        coord: Coordenada= self.mapa.obtenerCoordenada(j,i)
                        coord.visible= False
                    self.botonCrearAgente.config(state=NORMAL)

            if tipo == "Agente p":
                self.agente= AgenteP(criatura, self.mapa, x, y, xEnd, yEnd)
            elif tipo == "Agente Axel":
                self.agente= AgenteAxel(criatura, self.mapa, x, y, xEnd, yEnd)
            elif tipo == "Agente Abad":
                self.agente= AgenteAbad(criatura, self.mapa, x, y, xEnd, yEnd)

            self.modoUsuario= "Agente"
            CoordenadaInicio.puntoClave = "I"
            CoordenadaFinal.puntoClave = "F"
            ventana.destroy()
            self.crearSeccionControles()
            self.actualizarSeccionBusqueda(tipo)
            self.dibujar_mapa()
        except Exception as e:
            messagebox.showinfo("Error", f"{e}")

    def crearSeccionControles(self):
        if self.marcoControles:
            for widget in self.marcoControles.winfo_children():
                widget.destroy()
        self.labelControles = ttk.Label(self.marcoControles, text="Controles del agente:")
        self.labelControles.grid(row=0, column=0, columnspan=2, pady=10)
        if type(self.agente) == AgenteP:
            self.botonAvanzar = ttk.Button( self.marcoControles, text="Avanzar", bootstyle="INFO-OUTLINE", 
                command=lambda:(self.agente.moverUbicacion(), self.dibujar_mapa(), self.actualizar_costo(), self.analizarFinalizacion()))
            self.botonGirarDerecha = ttk.Button( self.marcoControles, text="Girar Derecha", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.rotarDerecha(), self.dibujar_mapa(), self.actualizar_costo()))
            self.botonAvanzar.grid(row=1, column=0, pady=10, padx=10, sticky="nsew", columnspan=2)
            self.botonGirarDerecha.grid(row=2, column=0, pady=10, padx=10, sticky="nsew", columnspan=2)
            self.listaBotonesAgente= [self.botonAvanzar, self.botonGirarDerecha]
        elif type(self.agente) == AgenteAxel:
            self.botonAvanzar = ttk.Button( self.marcoControles, text="Avanzar", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion(), self.dibujar_mapa(), self.actualizar_costo(), self.analizarFinalizacion()))
            self.botonGirarDerecha = ttk.Button( self.marcoControles, text="Girar Derecha", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.rotarDerecha(), self.dibujar_mapa(), self.actualizar_costo()))
            self.botonGirarIzquierda = ttk.Button( self.marcoControles, text="Girar Izquierda", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.rotarIzquierda(), self.dibujar_mapa(), self.actualizar_costo()))
            self.botonAvanzar.grid(row=1, column=0, pady=10, padx=10, sticky="nsew", columnspan=2)
            self.botonGirarDerecha.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
            self.botonGirarIzquierda.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
            self.listaBotonesAgente= [self.botonAvanzar, self.botonGirarDerecha, self.botonGirarIzquierda]
        elif type(self.agente) == AgenteAbad:
            self.avanzarEnfrente = ttk.Button( self.marcoControles, text="Avanzar Frente", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion("frente"), self.dibujar_mapa(), self.actualizar_costo(), self.analizarFinalizacion()))
            self.avanzarDerecha = ttk.Button( self.marcoControles, text="Avanzar Derecha", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion("derecha"), self.dibujar_mapa(), self.actualizar_costo(), self.analizarFinalizacion()))
            self.avanzarIzquierda = ttk.Button( self.marcoControles, text="Avanzar Izquierda", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion("izquierda"), self.dibujar_mapa(), self.actualizar_costo(), self.analizarFinalizacion()))
            self.avanzarAtras = ttk.Button( self.marcoControles, text="Avanzar Atrás", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion("atras"), self.dibujar_mapa(), self.actualizar_costo(), self.analizarFinalizacion()))
            self.avanzarEnfrente.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
            self.avanzarDerecha.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")
            self.avanzarIzquierda.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
            self.avanzarAtras.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
            self.listaBotonesAgente= [self.avanzarEnfrente, self.avanzarDerecha, self.avanzarIzquierda, self.avanzarAtras]

        self.labelCosto = ttk.Label(self.marcoControles, text="Costo: 0", font=("Segoe UI", 12))
        self.labelCosto.grid(row=3, column=0, columnspan=2, pady=5)
        self.actualizar_costo()

    def reiniciarMapaParaBusqueda(self):
        for i in range(self.mapa.alto):
            for j in range(self.mapa.ancho):
                    coord: Coordenada= self.mapa.obtenerCoordenada(j,i)
                    coord.visitado= False
                    coord.visible= False
                    coord.puntoDecision= False
                    coord.puntoActual= False
                    coord.puntoClave= None
                    coord.costoViaje= 0
                    coord.puntoCamino= False

        coordenadaFinal: Coordenada= self.mapa.obtenerCoordenada(self.agente.posicion_x_final, self.agente.posicion_y_final)
        coordenadaInicio: Coordenada= self.mapa.obtenerCoordenada(self.agente.posicion_x_inicial, self.agente.posicion_y_inicial)
        coordenadaInicio.puntoClave= "I"
        coordenadaFinal.puntoClave= "F"
        self.agente.inicializarPosicion()
        self.agente.actualizarVision()
        self.dibujar_mapa()

    def mostrarResultado(self, ruta):
        rutaAux = list(copy.deepcopy(ruta))
        if ruta == None:
            messagebox.showinfo("Resultado de la busqueda", "No se encontró una ruta")
        else: 
            for i in self.listaBotonesAgente:
                    i.config(state=DISABLED)
            messagebox.showinfo("Resultado de la busqueda", "Ruta encontrada")    
            while ruta:
                nodoActual = ruta.pop(0)
                self.agente.retroceder(nodoActual)
                CoordenadaActual: Coordenada= self.mapa.obtenerCoordenada(self.agente.posicion_x, self.agente.posicion_y)
                CoordenadaActual.puntoCamino = True
            self.mostrarResultadoBusqueda(rutaAux)
            self.dibujar_mapa()

    def mostrarResultadoBusqueda(self, ruta):
        self.marcoResultado = ttk.Labelframe( self.panelAgente, text="Resultado de la busqueda", padding=3, bootstyle="LIGHT")
        self.marcoResultado.grid(row=3, column=0, pady=2, sticky="nsew")
        
        self.labelResultadoBusqueda = ttk.Label(self.marcoResultado, text=f"Ruta encontrada:")
        self.labelResultadoBusqueda.grid(row=0, column=0, pady=2)
        text = ""
        for paso in ruta:
            text += f"{chr(65 + paso.posicion[0])},{paso.posicion[1]+1} -> "
        self.labelCamino = ttk.Label(self.marcoResultado, text=text, wraplength=350, anchor="center")
        self.labelCamino.grid(row=1, column=0, pady=1)

    def actualizarSeccionBusqueda(self, tipoAgente):
        if tipoAgente == "Agente p" or tipoAgente == "Agente Axel":
            if hasattr(self, 'marcoResultado'):
                self.marcoResultado.destroy()
            self.marcoBusqueda.destroy()
            self.crearSeccionAlgBusqueda()
            return
        else:
            CoordenadaFinal = (self.agente.posicion_x_final, self.agente.posicion_y_final)
            self.labelBusqueda.config(text="Opciones de busqueda:")
            self.tituloLabelBusquProfundidad = ttk.Label(self.marcoBusqueda, text="Busqueda en Profundidad:")
            self.tituloLabelBusquAnchura = ttk.Label(self.marcoBusqueda, text="Busqueda en Anchura:")
            self.tituloLabelEstrella = ttk.Label(self.marcoBusqueda, text="Busqueda A*:")

            self.botonBusquedaProfundidad = ttk.Button(self.marcoBusqueda, text="Paso a paso", bootstyle="INFO-OUTLINE", command= lambda: (self.reiniciarMapaParaBusqueda(), self.mostrarResultado(self.agente.busquedaProfundidadPaso(prioridad=self.comboPrioridad.get()))))

            self.botonBusquedaProfundidadDesicion = ttk.Button(self.marcoBusqueda, text="Por desicion", bootstyle="INFO-OUTLINE", command= lambda: (self.reiniciarMapaParaBusqueda(), self.mostrarResultado(self.agente.busquedaProfundidadDecision(self.comboPrioridad.get()))))
            self.labelPrioridad= ttk.Label(self.marcoBusqueda, text="Seleccione la prioridad que se usara:")
            
            self.comboPrioridad= ttk.Combobox(self.marcoBusqueda, values=["Arriba, Abajo, Izquierda, Derecha", "Abajo, Arriba, Izquierda, Derecha", "Izquierda, Derecha, Arriba, Abajo", "Derecha, Izquierda, Arriba, Abajo","Derecha, Abajo, Arriba, Izquierda"], state="readonly", width=200)
            self.comboPrioridad.current(0)

            self.botonBusquedaAnchura = ttk.Button(self.marcoBusqueda, text="Paso a paso", bootstyle="INFO-OUTLINE", command= lambda: (self.reiniciarMapaParaBusqueda(), self.mostrarResultado(self.agente.busquedaAnchuraPaso(CoordenadaFinal[0], CoordenadaFinal[1]))))
            self.botonBusquedaAnchuraDesicion = ttk.Button(self.marcoBusqueda, text="Por desicion", bootstyle="INFO-OUTLINE", command= lambda: (self.reiniciarMapaParaBusqueda(), self.mostrarResultado(self.agente.busquedaAnchuraDecision(CoordenadaFinal[0], CoordenadaFinal[1]))))

            self.botonBusquedaEstrella = ttk.Button(self.marcoBusqueda, text="Paso a paso", bootstyle="INFO-OUTLINE", command= lambda: (self.reiniciarMapaParaBusqueda(), self.mostrarResultado(self.agente.busquedaA(CoordenadaFinal[0], CoordenadaFinal[1]))))

            self.tituloLabelBusquProfundidad.grid(row=1, column=0, columnspan=2, pady=5)
            self.botonBusquedaProfundidad.grid(row=2, column=0, pady=5)
            self.botonBusquedaProfundidadDesicion.grid(row=2, column=1, pady= 5)
            self.labelPrioridad.grid(row=3, column=0, columnspan=2, pady=5)
            self.comboPrioridad.grid(row=4, column=0, columnspan=2, pady=5)
            self.tituloLabelBusquAnchura.grid(row=5, column=0, columnspan=2, pady=5)
            self.botonBusquedaAnchura.grid(row=6, column=0, pady=5)
            self.botonBusquedaAnchuraDesicion.grid(row=6, column=1, pady=5)
            self.tituloLabelEstrella.grid(row=7, column=0, columnspan=2, pady=5)
            self.botonBusquedaEstrella.grid(row=8, column=0, columnspan=2, pady=5)

    # FUNCIONES DE OBTENER Y MODIFICAR VALORES
    def obtenerValorCoordenada(self):
        if not self.mapa:
            messagebox.showinfo("Error", "Carga un mapa primero.")
            return
        if self.modoUsuario == "Agente" or self.modoUsuario == None:
            messagebox.showinfo("Error", "No puedes obtener el valor de una coordenada si no estás en modo dios.")
            return
        try:
            x, y = self.x_get.get().upper(), self.y_get.get()
            x, y,_ = self.cambioTipoValoresEntrada(x, y)
            labelResultado= self.labelObtener
            if self.mapa.alto <= y or self.mapa.ancho <= x or x < 0 or y < 0:
                raise IndexError("Coordenadas fuera de los límites del mapa.")
            coordenadaBuscada= self.mapa.obtenerCoordenada(x, y)
            labelResultado.config(text=coordenadaBuscada)
        except Exception as e:
            messagebox.showinfo("Error", f"{e}")

    def modificarValorCoordenada(self):
        if not self.mapa:
            messagebox.showinfo("Error", "Carga un mapa primero.")
            return
        if self.modoUsuario == "Agente" or self.modoUsuario == None:
            messagebox.showinfo("Error", "No puedes modificar el valor de una coordenada si no estás en modo dios.")
            return
        try:
            x, y, nuevoValor = self.x_mod.get().upper(), self.y_mod.get(), self.val_mod.get()
            x, y, nuevoValor = self.cambioTipoValoresEntrada(x, y, nuevoValor)

            if self.mapa.tipoMapa == "Binario" and nuevoValor not in [0, 1]:
                raise ValueError("El nuevo valor debe ser 0 o 1 para un mapa binario.")
            elif self.mapa.tipoMapa == "Mixto" and (nuevoValor < 0 or nuevoValor > 4):
                raise ValueError("El nuevo valor debe estar entre 0 y 4 para un mapa mixto.")
            
            coordenadaCambiar = self.mapa.obtenerCoordenada(x, y)
            coordenadaCambiar.valor= nuevoValor
            coordenadaCambiar.avanzable= True if nuevoValor != 0 else False
            messagebox.showinfo("Exito", f"El valor de la coordenada [{x},{y}] ha sido modificado de {self.mapa.obtenerCoordenada(x, y).valor} a {nuevoValor}.")
            self.dibujar_mapa()
        except Exception as e:
            messagebox.showinfo("Error", f"{e}")

    def cambioTipoValoresEntrada(self, x:str, y:str, nuevoValor="0"):
        if x.isalpha() and y.isdigit():
            x= ord(x.upper()) - 65
            y= int(y) - 1
        else: 
            raise ValueError("La coordenada X debe ser una letra y la coordenada Y un número.")
        if not nuevoValor.isdigit():
            raise ValueError("El nuevo valor debe ser un número entero.")
        return x, y, int(nuevoValor)

    # FUNCIONES DE DIBUJO DE MAPA
    def dibujar_mapa(self):
        for widget in self.panelMapa.winfo_children():
            widget.destroy()

        matriz = self.mapa.crearMatrizTerreno()
        matrizTexto = self.mapa.crearMatrizDatos(self.agente)

        w = (1050 - 75) / 100
        h = (900 - 80) / 100
        fig, ax = plt.subplots(figsize=(w, h), dpi=100)
        self.configurarTituloEjes(ax)

        mapaColores, intervaloNormalizado = self.crearMapaColoresLimites()
        ax.pcolormesh(matriz, cmap=mapaColores, norm=intervaloNormalizado, edgecolors='black')
        self.colocadoTextoAdicional(ax, matrizTexto)

        zipLeyenda = self.crearZipLeyenda()
        leyendasColores = [mpatches.Patch(facecolor=color, label=nombre, edgecolor="black") for nombre, color in zipLeyenda]
        ax.legend(handles=leyendasColores, bbox_to_anchor=(1.3, 1))
        fig.subplots_adjust(right=0.75)
        fig.set_facecolor("#737373")

        canvas = FigureCanvasTkAgg(fig, master=self.panelMapa)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="none", expand=False)
        plt.close(fig)

    def configurarTituloEjes(self, ax):
        ax.set_title("Mapa de Terreno", fontsize=16, fontweight='bold')
        ax.set_xlabel("Coordenada X", fontsize=12)
        ax.set_ylabel("Coordenada Y", fontsize=12)
        ax.set_xticks([i+0.5 for i in range(self.mapa.ancho)])
        ax.set_yticks([i+0.5 for i in range(self.mapa.alto)])
        ax.set_xticklabels([chr(65+i) for i in range(self.mapa.ancho)])  # Etiquetas de la A a la letra correspondiente
        ax.set_yticklabels([i+1 for i in range(self.mapa.alto)])  # Etiquetas de 1 a n
        ax.invert_yaxis()  # Invertir el eje Y para que el origen esté en la esquina superior izquierda

    def crearMapaColoresLimites(self):
        if self.mapa.tipoMapa == "Binario": 
            colores_ordenados = []
            valores_ordenados = [-1, 0, 1]
            for valor in valores_ordenados:
                if valor in self.colorTerrenoBinario:
                    colores_ordenados.append(self.colorTerrenoBinario[valor])
            listaValoresColores = colores_ordenados
            
        elif self.mapa.tipoMapa == "Mixto":
            colores_ordenados = []
            valores_ordenados = [-1, 0, 1, 2, 3, 4, 5, 6]
            for valor in valores_ordenados:
                if valor in self.colorTerrenoMixto:
                    colores_ordenados.append(self.colorTerrenoMixto[valor])
            listaValoresColores = colores_ordenados

        mapaColores = ListedColormap(listaValoresColores)
        Limites = [i - 1.5 for i in range(len(listaValoresColores)+1)]
        intervalosNormalizados = BoundaryNorm(Limites, mapaColores.N)
        
        return mapaColores, intervalosNormalizados
    
    def crearZipLeyenda(self):
            if self.mapa.tipoMapa == "Binario":
                zipLeyenda = zip(['0 Valla', '1 Camino'], self.colorTerrenoBinario.values())
            elif self.mapa.tipoMapa == "Mixto":
                zipLeyenda = zip(['0 Montaña', '1 Agua', '2 Bosque', '3 Arena', '4 Tierra', '5 Pantano', '6 Nieve'], self.colorTerrenoMixto.values())
            return zipLeyenda

    def colocadoTextoAdicional(self, ax, matrizTexto):
        for i in range(self.mapa.alto):
            for j in range(self.mapa.ancho):
                if matrizTexto[i][j] != "":
                    color = 'black'
                    texto = matrizTexto[i][j]
                    fontsize = 10
                    fontweight = 'bold'

                    if any(c in texto for c in ['^','>','v','<']):
                        color = 'red'
                        fontsize = 14

                    ax.text(j+0.5, i+0.5, #Alineacion con las coordenadas en el sistema de datos de ax
                            texto, #Texto a mostrar
                            ha='center', #Configuraciones adicionales de estilo
                            va='center', 
                            color=color, 
                            fontsize=fontsize,
                            fontweight=fontweight,
                            fontfamily='Arial')
                else: continue

                CoordenadaActual: Coordenada= self.mapa.obtenerCoordenada(j,i)
                if CoordenadaActual.puntoCamino == True:
                    ax.add_patch(plt.Circle((j+0.5, i+0.5), 0.1, color='yellow'))

if __name__ == "__main__":
    interfaz = Interfaz()