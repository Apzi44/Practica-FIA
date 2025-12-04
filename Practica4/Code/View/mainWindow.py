import time
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from ttkbootstrap.tableview import Tableview
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap.constants import *
import copy


class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="cyborg")
        self.title("Interfaz de usuario")
        self.geometry("1100x700")
        self.state("zoomed")
        self._configurar_frames()

    def _configurar_frames(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1, minsize=280)
        self.rowconfigure(0, weight=1)

        # Marco izquierdo (tabla)
        self.marco_frame_tabla = ttk.Frame(self, padding=10)
        self.marco_frame_tabla.grid(row=0, column=0, sticky="nsew")

        # Marco derecho (controles)
        self.marco_frames_controles = ttk.Frame(self, padding=10)
        self.marco_frames_controles.grid(row=0, column=1, sticky="nsew")

        self._configurar_frame_tabla()
        self._configurar_frame_controles()

    def _configurar_frame_tabla(self):
        self.marco_frame_tabla.columnconfigure(0, weight=1)
        self.marco_frame_tabla.rowconfigure(0, weight=1)

        self.frame_tabla = ttk.Labelframe(self.marco_frame_tabla, text="Tabla de datos", bootstyle=PRIMARY, padding=15)
        self.frame_tabla.grid(row=0, column=0, sticky="nsew")
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(8, weight=1)

        self.label_titulo_tabla = ttk.Label(self.frame_tabla, text="Tabla de datos", font=("Segoe UI", 18, "bold"))
        self.label_titulo_tabla.grid(row=0, column=0, pady=(0, 10))

        self.label_subtitulo_tabla = ttk.Label(self.frame_tabla, text="Contenido del archivo", font=("Segoe UI", 16, "bold"))
        self.label_subtitulo_tabla.grid(row=1, column=0, pady=(0, 10))

        self.label_preview_tabla = ttk.Label(self.frame_tabla, text="Cargue un archivo para ver su contenido", font=("Segoe UI", 14), foreground="#e0e0e0")
        self.label_preview_tabla.grid(row=2, column=0, pady=(0, 10))

    def _configurar_frame_controles(self):
        estilo_controles_basicos = SUCCESS
        estilo_controles_eleccion = WARNING
        estilo_botones_basicos = "SUCCESS-OUTLINE"
        estilo_botones_eleccion = "WARNING-OUTLINE"

        self.marco_frames_controles.columnconfigure(0, weight=1)
        self.marco_frames_controles.rowconfigure(0, weight=0)
        self.marco_frames_controles.rowconfigure(1, weight=0)

        self.frame_controles_basicos = ttk.Labelframe(self.marco_frames_controles, text="Controles básicos", bootstyle=estilo_controles_basicos,padding=10)
        self.frame_controles_basicos.grid(row=0, column=0, sticky="new", pady=5)
        self.frame_controles_basicos.columnconfigure(0, weight=1)
        for i in range(1, 4): self.frame_controles_basicos.rowconfigure(i, weight=1)

        self.label_titulo_controles_basicos = ttk.Label(self.frame_controles_basicos, text="Controles básicos", font=("Segoe UI", 16, "bold"))
        self.label_titulo_controles_basicos.grid(row=0, column=0, pady=(0, 5))

        self.boton_cargar_datos = ttk.Button(self.frame_controles_basicos, text="Cargar datos", bootstyle=estilo_botones_basicos)
        self.boton_cargar_datos.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.boton_reiniciar_datos = ttk.Button(self.frame_controles_basicos, text="Reiniciar datos", bootstyle=estilo_botones_basicos)
        self.boton_reiniciar_datos.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.boton_borrar_datos = ttk.Button(self.frame_controles_basicos, text="Borrar datos", bootstyle=estilo_botones_basicos)
        self.boton_borrar_datos.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.boton_anadir_datos = ttk.Button(self.frame_controles_basicos, text="Anadir datos", bootstyle=estilo_botones_basicos)
        self.boton_anadir_datos.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        self.frame_controles_eleccion = ttk.Labelframe(self.marco_frames_controles, text="Elección de subconjunto", bootstyle=estilo_controles_eleccion, padding=10)
        self.frame_controles_eleccion.grid(row=1, column=0, sticky="new", pady=5)
        self.frame_controles_eleccion.columnconfigure(0, weight=1)
        for i in range(1, 4): self.frame_controles_eleccion.rowconfigure(i, weight=1)

        self.label_titulo_controles_eleccion = ttk.Label(self.frame_controles_eleccion, text="Selecciona un método", font=("Segoe UI", 16, "bold"))
        self.label_titulo_controles_eleccion.grid(row=0, column=0, pady=(0, 5))

        self.boton_eleccion_subconjunto_uno_por_uno = ttk.Button(self.frame_controles_eleccion, text="Elección uno por uno", bootstyle=estilo_botones_eleccion)
        self.boton_eleccion_subconjunto_uno_por_uno.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.boton_eleccion_subconjunto_por_rango = ttk.Button(self.frame_controles_eleccion, text="Elección por rango", bootstyle=estilo_botones_eleccion)
        self.boton_eleccion_subconjunto_por_rango.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.boton_eleccion_subconjunto_por_atributo = ttk.Button(self.frame_controles_eleccion, text="Elección por atributo", bootstyle=estilo_botones_eleccion)
        self.boton_eleccion_subconjunto_por_atributo.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.boton_eleccion_subconjunto_por_varios_atributos = ttk.Button(self.frame_controles_eleccion, text="Elección por varios atributos", bootstyle=estilo_botones_eleccion)
        self.boton_eleccion_subconjunto_por_varios_atributos.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

    def preguntar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv"), ("Archivos de texto", "*.txt")])
        if archivo:
            return archivo
        else:
            return None

    def preguntar_separador(self):
        separador = simpledialog.askstring("Separador", "Ingrese el separador del archivo")
        if separador:
            return separador
        else:
            return None

    def aviso_confirmacion(self, mensaje):
        confirmacion = messagebox.askyesno("Confirmación", mensaje)
        if confirmacion:
            return True
        else:
            return False
    
    def mostrar_mensaje(self, mensaje, tipo_mensaje="info"):
        if tipo_mensaje == "info":
            messagebox.showinfo("Información", mensaje)
        elif tipo_mensaje == "error":
            messagebox.showerror("Error", mensaje)
        elif tipo_mensaje == "warning":
            messagebox.showwarning("Advertencia", mensaje)
    
    def crear_tabla(self, datos):
        if hasattr(self, "tabla"):
            self.tabla.destroy()
        
        self.tabla = ttk.Treeview(self.frame_tabla, 
            columns=("No.fila", "Minimo", "Maximo", "Promedio", "Desviacion estandar", "Atributo"), 
            show="headings",
            height=min(len(datos), 10))

        for i, col in enumerate(("No.fila", "Minimo", "Maximo", "Promedio", "Desviacion estandar", "Atributo")):
            if i == 0:
                self.tabla.column(col, width=50, anchor="center")
            else:
                self.tabla.column(col, width=100, anchor="center")
            self.tabla.heading(col, text=col)
        
        for i, linea in enumerate(datos, start=1):
            valores_con_indice = (i, *linea)
            self.tabla.insert(parent="", index="end", values=valores_con_indice)
        self.tabla.grid(row=8, column=0, sticky="n", pady=15)

    def destruir_tabla(self):
        if hasattr(self, "tabla"):
            self.tabla.destroy()
            
        self.label_preview_tabla.grid()
        self.label_titulo_datos_cualitativos.destroy()
        self.label_titulo_datos_cuantitativos.destroy()
        self.label_cantidad_datos_cualitativos.destroy()
        self.label_cantidad_datos_cuantitativos.destroy()
        self.label_datos_cualitativos.destroy()
        self.label_datos_cuantitativos.destroy()

    def mostrar_datos_tabla(self, datos_cualitativos, datos_cuantitativos, largo_datos_cualitativos, largo_datos_cuantitativos):
        self.label_preview_tabla.grid_remove()
        self.label_titulo_datos_cualitativos= ttk.Label(self.frame_tabla, text="Datos cualitativos", font=("Segoe UI", 16, "bold"))
        self.label_titulo_datos_cuantitativos= ttk.Label(self.frame_tabla, text="Datos cuantitativos", font=("Segoe UI", 16, "bold"))
        
        self.label_titulo_datos_cualitativos.grid(row=2, column=0, pady=(0, 5))
        self.label_titulo_datos_cuantitativos.grid(row=5, column=0, pady=(0, 5))

        self.label_cantidad_datos_cualitativos = ttk.Label(self.frame_tabla, text="Cantidad de datos cualitativos: " + str(largo_datos_cualitativos), font=("Segoe UI", 14))
        self.label_cantidad_datos_cuantitativos = ttk.Label(self.frame_tabla, text="Cantidad de datos cuantitativos: " + str(largo_datos_cuantitativos), font=("Segoe UI", 14))

        self.label_cantidad_datos_cualitativos.grid(row=3, column=0, pady=(0, 5))
        self.label_cantidad_datos_cuantitativos.grid(row=6, column=0, pady=(0, 5))

        string_datos_cualitativos = ""
        string_datos_cuantitativos = ""
        for datos in datos_cualitativos:
            string_datos_cualitativos = string_datos_cualitativos + f"{datos}, "

        for datos in datos_cuantitativos:
            string_datos_cuantitativos = string_datos_cuantitativos + f"{datos}, "

        self.label_datos_cualitativos = ttk.Label(self.frame_tabla, text=string_datos_cualitativos, anchor="center", font=("Segoe UI", 12))
        self.label_datos_cualitativos.grid(row=4, column=0, sticky="new")

        self.label_datos_cuantitativos = ttk.Label(self.frame_tabla, text=string_datos_cuantitativos, anchor="center", font=("Segoe UI", 12))
        self.label_datos_cuantitativos.grid(row=7, column=0, sticky="new")

    def pedir_filas(self, valorMaximo):
        lista_actual_filas = set()
        while True: 
            texto= f"Ingrese el número de fila a añadir, lista actual: {lista_actual_filas}. Aprete 'cancelar' para finalizar o salir. En caso de no tener nada en la lista no se realiza ninguna accion"
            fila = Querybox.get_integer(texto, title="Añadir fila", 
            minvalue=1, maxvalue=valorMaximo, parent=self)
            # Si el usuario cancela la accion
            if fila == None:
                break

            if fila in lista_actual_filas:
                self.mostrar_mensaje("La fila ya se encuentra en la lista", "warning")
                continue
            if len(lista_actual_filas) >= valorMaximo:
                self.mostrar_mensaje("Se ha alcanzado el maximo de filas", "warning")
                continue
            else:
                lista_actual_filas.add(fila)

        # Si se cancela y no se añade nada
        if len(lista_actual_filas) == 0:
            return None
        else:
            return lista_actual_filas

    def pedir_intervalo(self, valorMaximo):
        intervalo = []
        # Se pide el inicio del intervalo
        while len(intervalo) < 1:
            texto= "Ingrese el inicio del intervalo"
            inicio = Querybox.get_integer(texto, title="Intervalo", 
            minvalue=1, maxvalue=valorMaximo, parent=self)
            # Si el usuario cancela la accion
            if inicio == None:
                break
            intervalo.append(inicio)
        
        # Se pide el fin del intervalo
        if len(intervalo) == 1:
            while len(intervalo) < 2:
                texto= "Ingrese el fin del intervalo"
                fin = Querybox.get_integer(texto, title="Intervalo", 
                minvalue=intervalo[0], maxvalue=valorMaximo, parent=self)
                # Si el usuario cancela la accion
                if fin == None:
                    break
                intervalo.append(fin)
        else:
            return None
        return intervalo
        
    def pedir_atributo(self):
        atributo = Querybox.get_string("Ingrese el atributo", title="Atributo", parent=self)
        if atributo == None:
            return None
        atributo = atributo.lower()
        return atributo

    def pedir_atributos(self):
        atributos = set()
        while True:
            atributo = self.pedir_atributo()
            if atributo == None:
                break
            if atributo in atributos:
                self.mostrar_mensaje("El atributo ya se encuentra en la lista", "warning")
                continue
            else:
                atributos.add(atributo)
        return atributos

if __name__ == "__main__":
    MainWindow()
