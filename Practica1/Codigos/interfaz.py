from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap, BoundaryNorm
import mapa as mp
from agente import AgenteP, AgenteAxel, AgenteAbad
import Coordenada as Coordenada

class Interfaz(ttk.Window):
    colorTerrenoBinario = {
        0: "#FFFFFF",
        1: "#4B4B4B",
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
        self.configuracionesIniciales()
        self.crear_layout()
        self.mainloop()

    def configuracionesIniciales(self):
        super().__init__(themename="darkly")
        self.title("Mapa Interactivo")
        self._anchoVentana = 1600
        self._altoVentana = 900
        self.geometry(f"{self._anchoVentana}x{self._altoVentana}")
        self.resizable(False, False)
        
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)

    def crear_layout(self):        
        # Panel izquierdo (controles)
        self.panelControl = ttk.Frame(self, padding=10, bootstyle="DARK", width=450)
        self.panelControl.grid(row=0, column=0, sticky="nsew")
        self.panelControl.grid_propagate(False)
        for i in range(14):
            self.panelControl.rowconfigure(i, weight=1)
        self.panelControl.columnconfigure(0, weight=1)
        self.panelControl.columnconfigure(1, weight=1)

        # Panel derecho (mapa)
        self.panelMapa = ttk.Frame(self, bootstyle=LIGHT, width=1150)
        self.panelMapa.grid(row=0, column=1, sticky="nsew")
        self.panelMapa.grid_propagate(False)

        self.labelTitular= ttk.Label(self.panelControl, text="Interfaz de Mapa", font=("Arial", 18, "bold"))
        self.labelTitular.grid(row=0, column=0, columnspan=2, pady=10, ipadx=10, sticky="nsew")
        self.botonCargarMapa = ttk.Button( self.panelControl, text="Cargar Mapa", bootstyle="PRIMARY-OUTLINE",command=self.cargar_mapa)
        self.botonCrearAgente = ttk.Button( self.panelControl, text="Crear Agente", bootstyle="INFO-OUTLINE",command=self.cargar_agente)

        self.labelTitular.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")
        self.botonCargarMapa.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        self.botonCrearAgente.grid(row=1, column=1, pady=10, padx=10,sticky="nsew")

        self.seccion_obtener()
        self.seccion_modificar()
        self.seccionControles()

    def seccion_obtener(self):
        # Creacion del marco para obtener valor
        self.marco = ttk.Labelframe( self.panelControl, text="Consultar coordenada", padding=10, bootstyle="SUCCESS")
        self.marco.grid(row=2, column=0, columnspan=4, rowspan=3,pady=15, sticky="nsew")
        for i in range(4):
            self.marco.rowconfigure(i, weight=1)
        self.marco.columnconfigure(0, weight=1)
        # Entradas y etiquetas
        self.x_get = ttk.Entry(self.marco, bootstyle="SUCCESS")
        self.y_get = ttk.Entry(self.marco, bootstyle="SUCCESS")
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
        boton_obtener = ttk.Button( self.marco, text="Obtener valor", bootstyle="SUCCESS", command= self.obtenerValorCoordenada)
        boton_obtener.grid(row=2, column=0, columnspan=2, pady=5)
        # Etiqueta resultado
        self.labelObtener = ttk.Label(self.marco, text="Valor: -", font=("Segoe UI", 12))
        self.labelObtener.grid(row=3, column=0, columnspan=2, pady=5)

    def seccion_modificar(self):
        # Creacion del marco para modificar valor
        marco = ttk.Labelframe( self.panelControl, text="Modificar coordenada", padding=10, bootstyle=DANGER)
        marco.grid(row=6, column=0, columnspan=2,rowspan=4, pady=15, sticky="nsew")
        for i in range(4):
            marco.rowconfigure(i, weight=1)
        marco.columnconfigure(0, weight=1)

        # Entradas y etiquetas
        self.x_mod = ttk.Entry(marco, bootstyle="DANGER")
        self.y_mod = ttk.Entry(marco, bootstyle="DANGER")
        self.val_mod = ttk.Entry(marco, bootstyle="DANGER")
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
        boton_modificar = ttk.Button( marco, text="Modificar valor", bootstyle="DANGER", command=self.modificarValorCoordenada)
        boton_modificar.grid(row=3, column=0, columnspan=2, pady=5)

    def seccionControles(self):
        self.marcoControles = ttk.Labelframe( self.panelControl, text="Controles del agente", padding=10, bootstyle="INFO")
        self.marcoControles.grid(row=10, column=0, columnspan=2, rowspan=4, pady=15, sticky="nsew")
        for i in range(4): self.marcoControles.rowconfigure(i, weight=1)
        for i in range(2): self.marcoControles.columnconfigure(i, weight=1)
        self.labelControles = ttk.Label(self.marcoControles, text="Crea un agente para ver los controles", font=("Segoe UI", 10))
        self.labelControles.grid(row=0, column=0, columnspan=3, pady=10)
        self.labelCosto = ttk.Label(self.marcoControles, text="Costo: 0", font=("Segoe UI", 12))
        self.labelCosto.grid(row = 3, column = 0, columnspan = 2, pady = 5)
   
    # Funcion para obtener y actualizar el costo
    def actualizar_costo(self):
        if self.agente:
            costo_actual = self.agente.coste
            self.labelCosto.config(text=f"Costo: {costo_actual}")

    # FUNCIONES DE CARGA DE MAPA Y AGENTE
    def cargar_mapa(self): 
        respuesta = messagebox.askyesno("Instrucciones", "Desea cargar un archivo para el mapa base?")
        if respuesta == False: return
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
                    del self.mapaxdd
                    return
        if hasattr(self,"mapa"):
            self.dibujar_mapa()
    
    def cargar_agente(self):
        if not self.mapa:
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
    def crearAgente(self, ventana, tipo, criatura, posX= "A", posY="0", posXEnd="A",posYEnd="0"  ):
        try:
            x,y, _, = self.cambioTipoValoresEntrada(posX, posY)
            xEnd,yEnd, _= self.cambioTipoValoresEntrada(posXEnd, posYEnd)
            if self.mapa.alto <= y or self.mapa.ancho <= x or x < 0 or y < 0:
                raise IndexError("Coordenadas de inicio fuera de los límites del mapa.")
            if self.mapa.alto <= yEnd or self.mapa.ancho <= xEnd or xEnd<0 or yEnd<0:
                raise IndexError("Coordenadas de final fuera de los límites del mapa.")
            if x == xEnd and y == yEnd:
                raise ValueError("Las coordenadas de inicio y final deben ser diferentes.")
            if tipo == "Agente p":
                self.agente= AgenteP(criatura, self.mapa, x, y)
            elif tipo == "Agente Axel":
                self.agente= AgenteAxel(criatura, self.mapa, x, y)
            elif tipo == "Agente Abad":
                self.agente= AgenteAbad(criatura, self.mapa, x, y)

            CoordenadaInicio = self.mapa.obtenerCoordenada(x, y)
            CoordenadaFinal: Coordenada= self.mapa.obtenerCoordenada(xEnd, yEnd)
            CoordenadaInicio.puntoClave = "I"
            CoordenadaFinal.puntoClave = "F"

            ventana.destroy()
            self.crearSeccionControles()
            self.dibujar_mapa()
        except Exception as e:
            messagebox.showinfo("Error", f"{e}")

    def crearSeccionControles(self):
        for widget in self.marcoControles.winfo_children():
            widget.destroy()
        self.labelControles = ttk.Label(self.marcoControles, text="Controles del agente:")
        self.labelControles.grid(row=0, column=0, columnspan=2, pady=10)
        if type(self.agente) == AgenteP:
            self.botonAvanzar = ttk.Button( self.marcoControles, text="Avanzar", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion(), self.dibujar_mapa(), self.actualizar_costo()))
            self.botonGirarDerecha = ttk.Button( self.marcoControles, text="Girar Derecha", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.rotarDerecha(), self.dibujar_mapa(), self.actualizar_costo()))
            self.botonAvanzar.grid(row=1, column=0, pady=10, padx=10, sticky="nsew", columnspan=2)
            self.botonGirarDerecha.grid(row=2, column=0, pady=10, padx=10, sticky="nsew", columnspan=2)
        elif type(self.agente) == AgenteAxel:
            self.botonAvanzar = ttk.Button( self.marcoControles, text="Avanzar", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion(), self.dibujar_mapa(), self.actualizar_costo()))
            self.botonGirarDerecha = ttk.Button( self.marcoControles, text="Girar Derecha", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.rotarDerecha(), self.dibujar_mapa(), self.actualizar_costo()))
            self.botonGirarIzquierda = ttk.Button( self.marcoControles, text="Girar Izquierda", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.rotarIzquierda(), self.dibujar_mapa(), self.actualizar_costo()))
            self.botonAvanzar.grid(row=1, column=0, pady=10, padx=10, sticky="nsew", columnspan=2)
            self.botonGirarDerecha.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
            self.botonGirarIzquierda.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
        elif type(self.agente) == AgenteAbad:
            self.avanzarEnfrente = ttk.Button( self.marcoControles, text="Avanzar Frente", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion("frente"), self.dibujar_mapa(), self.actualizar_costo()))
            self.avanzarDerecha = ttk.Button( self.marcoControles, text="Avanzar Derecha", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion("derecha"), self.dibujar_mapa(), self.actualizar_costo()))
            self.avanzarIzquierda = ttk.Button( self.marcoControles, text="Avanzar Izquierda", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion("izquierda"), self.dibujar_mapa(), self.actualizar_costo()))
            self.avanzarAtras = ttk.Button( self.marcoControles, text="Avanzar Atrás", bootstyle="INFO-OUTLINE", command=lambda:(self.agente.moverUbicacion("atras"), self.dibujar_mapa(), self.actualizar_costo()))
            self.avanzarEnfrente.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
            self.avanzarDerecha.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")
            self.avanzarIzquierda.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
            self.avanzarAtras.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")

    # FUNCIONES DE OBTENER Y MODIFICAR VALORES
    def obtenerValorCoordenada(self):
        if not self.mapa:
            messagebox.showinfo("Error", "Carga un mapa primero.")
            return
        try:
            x, y = self.x_get.get().upper(), self.y_get.get()
            x, y,_ = self.cambioTipoValoresEntrada(x, y)
            labelResultado= self.labelObtener
            if self.mapa.alto <= y or self.mapa.ancho <= x or x < 0 or y < 0:
                raise IndexError("Coordenadas fuera de los límites del mapa.")
            coordenadaBuscada= self.mapa.obtenerCoordenada(x, y)
            if coordenadaBuscada.visible == False:
                raise ValueError("La coordenada no es visible por tanto no se sabe su valor.")
            labelResultado.config(text=coordenadaBuscada)
        except Exception as e:
            messagebox.showinfo("Error", f"{e}")

    def modificarValorCoordenada(self):
        if not self.mapa:
            messagebox.showinfo("Error", "Carga un mapa primero.")
            return
        try:
            x, y, nuevoValor = self.x_mod.get().upper(), self.y_mod.get(), self.val_mod.get()
            x, y, nuevoValor = self.cambioTipoValoresEntrada(x, y, nuevoValor)

            if self.mapa.tipoMapa == "Binario" and nuevoValor not in [0, 1]:
                raise ValueError("El nuevo valor debe ser 0 o 1 para un mapa binario.")
            elif self.mapa.tipoMapa == "Mixto" and (nuevoValor < 0 or nuevoValor > 4):
                raise ValueError("El nuevo valor debe estar entre 0 y 4 para un mapa mixto.")
            
            coordenadaCambiar = self.mapa.obtenerCoordenada(x, y)
            if coordenadaCambiar.visible == False:
                raise ValueError("La coordenada no es visible por tanto no se puede modificar su valor.")
            else:
                coordenadaCambiar.valor= nuevoValor
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

if __name__ == "__main__":
    Interfaz()