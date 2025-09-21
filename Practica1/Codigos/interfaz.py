import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap, BoundaryNorm
import mapa as mp
import agente as ag


class interfaz(tk.Tk):
    colorTerrenoBinario = {
        0: "#FFFFFF",
        1: "#4B4B4B",
    }

    colorTerrenoMixto = {
        0: "#5E5A59", #Montaña
        1: "#4682B4", #Agua
        2: "#228B22", #Bosque
        3: "#F8E268", #Arena
        4: "#F5D198" #Tierra
    }

    def __init__(self):
        self.agentes = []
        self.configurarBase()
        self.crearLabelsEntradasBotones()
        self.mainloop()

    def configurarBase(self):
        self._columnasGrid=10
        self._filasGrid=14
        #Inicializacion de la ventana
        super().__init__()
        self.title("Practica 1 - Fundamentos de IA")
        self.geometry("1250x600")
        self.resizable(False, False)

        #Configuracion de la cuadrícula
        for i in range(self._columnasGrid):
            self.columnconfigure(i, weight=1)
        for i in range(self._filasGrid):
            self.rowconfigure(i, weight=1)

    def crearLabelsEntradasBotones(self):
        # Creacion etiquetas bases de la interfaz
        self.labelEntradA=tk.Label(self,text="Interfaz de usuario - Mapa", justify="center", font=("Arial", 16, "bold"))
        self.labelEntradA.grid(row=0, column=0, ipadx=5, ipady=5, sticky="nsew", columnspan=2)
        self.labelOpciones= tk.Label(self,text="Funciones disponibles", justify="center", font=("Arial", 14, "bold"))
        self.labelOpciones.grid(row=2, column=0, ipadx=5, ipady=5, sticky="nsew", columnspan=2)

        #Creacion boton de cargar mapa
        self.botonCargaMapa=tk.Button(self, text="Cargar Mapa", command=self.cargarMapa)
        self.botonCargaMapa.grid(row=1, column=0, ipadx=80, ipady=2,sticky="ns")

        self.botonCargaAgente=tk.Button(self, text="Cargar Agente", command=self.cargarAgente)
        self.botonCargaAgente.grid(row=1, column=1, ipadx=80, ipady=2,sticky="ns")

        # Creacion de diferentes secciones de la interfaz
        self.__CoordenadasGUI()
        self.__ModificarGUI()

    def __CoordenadasGUI(self):
        #Creacion de labels
        self.labeltituloF1=tk.Label(self, text="Obtener valor de una coordenada", font=("Arial", 12, "bold"))
        self.labeltituloF1.grid(row=3, column=0, ipadx=5, ipady=5, sticky="nsew", columnspan=2)
        self.labelCoordenadaXF1=tk.Label(self, text="Coordenada X:", font=("Arial", 10))
        self.labelCoordenadaYF1=tk.Label(self, text="Coordenada Y:", font=("Arial", 10))
        self.labelResultadoF1=tk.Label(self, text="Valor:", font=("Arial", 10))

        #Creacion entradas y botones
        self.entradaCoordenadaXF1=tk.Entry(self)
        self.entradaCoordenadaXF1.insert(0, "A")
        self.entradaCoordenadaYF1=tk.Entry(self)
        self.entradaCoordenadaYF1.insert(0, "1")

        self.botonObtenerF1=tk.Button(self, text="Obtener valor", command= self.obtenerValorCoordenada)
        
        #Posicionamiento labels, entradas y botones en la cuadrícula
        self.labelCoordenadaXF1.grid(row=4, column=0, ipadx=5, ipady=5, sticky="nsew")
        self.labelCoordenadaYF1.grid(row=5, column=0, ipadx=5, ipady=5, sticky="nsew")
        self.labelResultadoF1.grid(row=6, column=0, ipadx=5, ipady=5, columnspan=2, sticky="nsew")

        self.entradaCoordenadaXF1.grid(row=4, column=1, ipadx=5, ipady=10, sticky="w")
        self.entradaCoordenadaYF1.grid(row=5, column=1, ipadx=5, ipady=10, sticky="w")
        self.botonObtenerF1.grid(row=7, column=0, columnspan=2, ipadx=120, ipady=2, sticky="ns")

    def __ModificarGUI(self):
        #Creacion de labels
        self.labeltituloF2=tk.Label(self, text="Modificar valor de una coordenada", font=("Arial", 12, "bold"))
        self.labeltituloF2.grid(row=8, column=0, ipadx=5, ipady=5, sticky="nsew", columnspan=2)
        self.labelCoordenadaXF2=tk.Label(self, text="Coordenada X:", font=("Arial", 10))
        self.labelCoordenadaYF2=tk.Label(self, text="Coordenada Y:", font=("Arial", 10))
        self.labelNuevoValorF2=tk.Label(self, text="Nuevo valor:", font=("Arial", 10))

        #Creacion entradas y botones
        self.entradaCoordenadaXF2=tk.Entry(self)
        self.entradaCoordenadaXF2.insert(0, "A")
        self.entradaCoordenadaYF2=tk.Entry(self)
        self.entradaCoordenadaYF2.insert(0, "1")
        self.entradaNuevoValorF2=tk.Entry(self)
        self.entradaNuevoValorF2.insert(0, "0")

        self.botonObtenerF2=tk.Button(self, text="Modificar valor", command= self.modificarValorCoordenada)

        #Posicionamiento labels, entradas y botones en la cuadrícula
        self.labelCoordenadaXF2.grid(row=9, column=0, ipadx=5, ipady=5, sticky="nsew")
        self.labelCoordenadaYF2.grid(row=10, column=0, ipadx=5, ipady=5, sticky="nsew")
        self.labelNuevoValorF2.grid(row=11, column=0, ipadx=5, ipady=5, sticky="nsew")
        self.entradaCoordenadaXF2.grid(row=9, column=1, ipadx=5, ipady=10, sticky="w")
        self.entradaCoordenadaYF2.grid(row=10, column=1, ipadx=5, ipady=10, sticky="w")
        self.entradaNuevoValorF2.grid(row=11, column=1, ipadx=5, ipady=10, sticky="w")
        self.botonObtenerF2.grid(row=12, column=0, columnspan=2, ipadx=120, ipady=4, pady=5, sticky="ns")
    
    def cargarMapa(self):
        respuesta = messagebox.askokcancel("Instrucciones", "Desea cargar un archivo para el mapa base?")
        if respuesta == False: return
        else:
            #Si no se carga el mapa base, no se puede cargar el adicional por lo tanto se rompe el ciclo
            bandera= self.__cargarArchivo()
            if bandera == False: return

        if hasattr(self,"mapa"):
            self.dibujarMapa()

    def cargarAgente(self):
        if hasattr(self, 'mapa'):
            self.ventanaEmergente = tk.Toplevel(self)
            self.ventanaEmergente.title("Crear agente")
            self.ventanaEmergente.geometry("300x100")
            self.ventanaEmergente.resizable(False, False)
            for i in range(3):
                self.ventanaEmergente.columnconfigure(i, weight=1)
            for i in range(4):
                self.ventanaEmergente.rowconfigure(i, weight=1)

            self.labelTituloEmergente = tk.Label(self.ventanaEmergente,text="Crear agente", font=("Arial", 12, "bold"))
            self.labelTituloEmergente.grid(row=0, column=0, ipadx=5, ipady=5, sticky="nsew", columnspan=3)
            self.labelTipoEmergente = tk.Label(self.ventanaEmergente,text="Tipo de agente", font=("Arial", 10))
            self.entradaOpcionesEmergente= ttk.Combobox(self.ventanaEmergente, values=["Agente P", "SuperSayayin", "Robot basico"])
            self.entradaOpcionesEmergente.current(0)
            self.entradaOpcionesEmergente.state(["readonly"])

            self.entradaOpcionesEmergente.grid(row=1, column=1, ipadx=5, ipady=5, sticky="nsew")
            self.labelTipoEmergente.grid(row=1, column=0, ipadx=5, ipady=5, sticky="nsew")

            self.botonCrearAgente = tk.Button(self.ventanaEmergente, text="Crear agente seleccionado", command= lambda:{self.crearAgente(self.entradaOpcionesEmergente.get()), self.ventanaEmergente.destroy()})
            self.botonCrearAgente.grid(row=3, column=0, columnspan=3, ipadx=120, ipady=2, sticky="ns")
        else:
            messagebox.showinfo("Error", "No se ha cargado ningún mapa. Por favor, cargue un mapa primero.")

    def crearAgente(self):
        tipo_agente = self.entradaOpcionesEmergente.get()
        nuevo_agente = ag.agente(tipo=tipo_agente, mapa=self.mapa, pos_x=0, pos_y=0)
        self.agentes.append(nuevo_agente)
        messagebox.showinfo('Exito',f"Agente '{tipo_agente}' colocado en la coordenada (0,0)")
        self.dibujarMapa()

    def __cargarArchivo(self):
        # Carga de archivo mediante un cuadro de dialogo
        archivo= filedialog.askopenfilename(title="Seleccione el archivo", filetypes= [
            ("Archivos de texto y csv", "*.txt; *.csv"),
            ("Archivos de texto", "*.txt"),
            ("Archivos CSV", "*.csv")])
        if not archivo: return False
        else: 
            self.mapa= mp.Mapa()
            bandera= self.mapa.leerArchivo(archivo)
            if bandera == False: del self.mapa
        return bandera
    
    def dibujarMapa(self):
        if hasattr(self.mapa, 'matriz'):
            # Obtencion de las matrices necesarias para la creacion del mapa
            matrizTerreno = self.mapa.crearMatrizTerreno()
            #matrizTexto= self.mapa.crearMatrizDatos()

            # Creacion la figura y el eje para el gráfico
            fig, ax = plt.subplots(figsize=(5, 6))
            self.configurarTituloEjes(ax)

            # Creacion del mapa con los colores y limites adecuados
            mapaColores, intervaloNormalizado = self.crearMapaColoresLimites()
            ax.pcolormesh( matrizTerreno,  cmap=mapaColores, norm=intervaloNormalizado, edgecolors='black')
            # Colocación de texto adicional en el mapa
            #self.colocadoTextoAdicional(ax, matrizTexto)
            
            for agente_actual in self.agentes:
                x = agente_actual._agente__pos_x
                y = agente_actual._agente__pos_y
                
                circulo = mpatches.Circle((x + 0.5, y + 0.5), radius = 0.3, facecolor='red', edgecolor='black', linewidth=1.5)
                ax.add_patch(circulo)
                            
            # Creacion de la leyenda del mapa
            zipLeyenda = self.crearZipLeyenda()
            leyendasColores = [mpatches.Patch(facecolor=color, label=nombre, edgecolor="black") for nombre, color in zipLeyenda]
            ax.legend(handles=leyendasColores, bbox_to_anchor=(1.3, 1))
            fig.subplots_adjust(right=0.75)

            # Integracion de la figura de Matplotlib en la interfaz de Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=2, rowspan=self._filasGrid, columnspan=self._columnasGrid-2, sticky="nsew")

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
        if self.mapa.tipoMapa == "Binario": listaValoresColores= list(self.colorTerrenoBinario.values())
        elif self.mapa.tipoMapa == "Mixto": listaValoresColores= list(self.colorTerrenoMixto.values())

        mapaColores = ListedColormap(listaValoresColores)
        Limites = [i - 0.5 for i in range(len(listaValoresColores)+1)]
        intervalosNormalizados = BoundaryNorm(Limites, mapaColores.N)
        
        return mapaColores, intervalosNormalizados

    def colocadoTextoAdicional(self, ax, matrizTexto):
        for i in range(self.mapa.alto):
            for j in range(self.mapa.ancho):
                if matrizTexto[i][j] != "":
                    ax.text(j+0.5, i+0.5, #Alineacion con las coordenadas en el sistema de datos de ax
                            matrizTexto[i][j], #Texto a mostrar
                            ha='center', #Configuraciones adicionales de estilo
                            va='center', 
                            color="black", 
                            fontsize=10,
                            fontweight='bold',
                            fontfamily='Arial')
                else: continue

    def crearZipLeyenda(self):
        if self.mapa.tipoMapa == "Binario":
            zipLeyenda = zip(['0 Valla', '1 Camino'], self.colorTerrenoBinario.values())
        elif self.mapa.tipoMapa == "Mixto":
            zipLeyenda = zip(['0 Montaña', '1 Agua', '2 Bosque', '3 Arena', '4 Tierra'], self.colorTerrenoMixto.values())
        return zipLeyenda

    def obtenerValorCoordenada(self):
        if hasattr(self, 'mapa'):
            # Obtencion de las coordenadas ingresadas por el usuario
            coordenaaX= self.entradaCoordenadaXF1.get().upper()
            coordenadaY= self.entradaCoordenadaYF1.get()
            # Obtencion de la etiqueta de resultado
            labelResultado= self.labelResultadoF1
            try:
                # Intento de conversion de las coordenadas a enteros y obtencion del valor de la coordenada en el mapa
                x,y, _= self.cambioTipoValoresEntrada(coordenaaX, coordenadaY)
                coordenadaBuscada= self.mapa.pedirCoordenada(x, y)
                # Actualizacion de la etiqueta de resultado
                labelResultado.config(text=coordenadaBuscada)
            except ValueError as e:
                messagebox.showinfo("Error", f"{e}")
            except IndexError:
                messagebox.showinfo("Error", "Las coordenadas están fuera de los límites del mapa.")
            except Exception as e:
                messagebox.showinfo("Error", f"{e}")
        else:
            messagebox.showinfo("Error", "No se ha cargado ningún mapa. Por favor, cargue un mapa primero.")

    def modificarValorCoordenada(self):
        if hasattr(self, 'mapa'):
            coordenadaXmodificar = self.entradaCoordenadaXF2.get().upper()
            coordenadaYmodificar = self.entradaCoordenadaYF2.get()
            nuevoValor= self.entradaNuevoValorF2.get()
            try:
                x, y, nuevoValor = self.cambioTipoValoresEntrada(coordenadaXmodificar, coordenadaYmodificar, nuevoValor)
                valorCoordenada= self.mapa.pedirCoordenada(x, y).valor

                if self.mapa.tipoMapa == "Binario" and nuevoValor not in [0, 1]:
                    raise ValueError("El nuevo valor debe ser 0 o 1 para un mapa binario.")
                elif self.mapa.tipoMapa == "Mixto" and (nuevoValor < 0 or nuevoValor > 4):
                    raise ValueError("El nuevo valor debe estar entre 0 y 4 para un mapa mixto.")
                self.mapa.pedirCoordenada(x, y).valor= nuevoValor
                messagebox.showinfo("Exito", f"El valor de la coordenada [{x},{y}] ha sido modificado de {valorCoordenada} a {nuevoValor}.")
                self.dibujarMapa()
            except ValueError as e:
                messagebox.showinfo("Error", f"{e}")
            except IndexError:
                messagebox.showinfo("Error", "Las coordenadas están fuera de los límites del mapa.")
            except Exception as e:
                messagebox.showinfo("Error", f"{e}")
        else:
            messagebox.showinfo("Error", "No se ha cargado ningún mapa. Por favor, cargue un mapa primero.")

    def cambioTipoValoresEntrada(self, x:str, y:str, nuevoValor="0"):
        if x.isalpha() and y.isdigit():
            x= ord(x.upper()) - 65
            y= int(y) - 1
        else: 
            raise ValueError("La coordenada X debe ser una letra y la coordenada Y un número.")
        if not nuevoValor.isdigit():
            raise ValueError("El nuevo valor debe ser un número entero.")
        return x, y, int(nuevoValor)

if __name__ == "__main__":
    app = interfaz()