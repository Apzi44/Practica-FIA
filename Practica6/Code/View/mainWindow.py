import time
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from ttkbootstrap.tableview import Tableview
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
import copy
#Martinez Alor Zaddkiel de Jesus

class MainWindow(ttk.Window):
    # FUNCIONES GRAFICAS
    def __init__(self):
        super().__init__(themename="cyborg")
        self.title("Interfaz de usuario")
        self.geometry("1100x700")
        self.state("zoomed")
        self._configurar_frames()

    def _configurar_frames(self):
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1, minsize=150)
        self.rowconfigure(0, weight=1)


        self.marco_frame_tabla = ttk.Frame(self, padding=10)
        self.marco_frame_tabla.grid(row=0, column=0, sticky="nsew")


        self.marco_frames_controles = ttk.Frame(self, padding=10)
        self.marco_frames_controles.grid(row=0, column=1, sticky="nsew")

        self._configurar_frame_tabla()
        self._configurar_frame_controles()

    def _configurar_frame_tabla(self):
        self.marco_frame_tabla.columnconfigure(0, weight=1)
        self.marco_frame_tabla.rowconfigure(0, weight=1)

        self.scrolled_frame_tabla = ScrolledFrame(self.marco_frame_tabla, padding=10)
        self.scrolled_frame_tabla.grid(row=0, column=0, sticky="nsew")
        self.scrolled_frame_tabla.columnconfigure(0, weight=1)
        self.scrolled_frame_tabla.rowconfigure(0, weight=1)

        self.frame_tabla = ttk.Labelframe(self.scrolled_frame_tabla, text="INFORMACION", bootstyle=PRIMARY, padding=15)
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(8, weight=1)
        self.frame_tabla.grid(row=0, column=0, sticky="nsew", padx=(0,15))

        self.label_titulo_frame_tabla = ttk.Label(self.frame_tabla, text="ALGORITMOS DE CLASIFICACION", font=("Segoe UI", 18, "bold"))
        self.label_titulo_frame_tabla.grid(row=0, column=0, pady=(0, 10))

        self.label_subtitulo_tabla_conjunto_datos = ttk.Label(self.frame_tabla, text="Contenido del conjunto de datos", font=("Segoe UI", 16, "bold"))
        self.label_subtitulo_tabla_conjunto_datos.grid(row=1, column=0, pady=(0, 10))

        self.label_preview_tabla_conjunto_datos = ttk.Label(self.frame_tabla, text="Cargue un archivo o ingrese datos manualmente para ver su contenido", font=("Segoe UI", 14), foreground="#e0e0e0")
        self.label_preview_tabla_conjunto_datos.grid(row=2, column=0, pady=(0, 10))

        self.subtitulo_tabla_clasificar = ttk.Label(self.frame_tabla, text="Contenido del conjunto de datos para clasificar", font=("Segoe UI", 16, "bold"))
        self.subtitulo_tabla_clasificar.grid(row=3, column=0, pady=(0, 10))

        self.label_preview_tabla_clasificar = ttk.Label(self.frame_tabla, text="Ingrese datos manualmente para ver su contenido", font=("Segoe UI", 14), foreground="#e0e0e0")
        self.label_preview_tabla_clasificar.grid(row=4, column=0, pady=(0, 10))

        self.frame_resultados = ttk.Frame(self.frame_tabla)
        self.frame_resultados.grid(row=5, column=0, pady=(0, 10))

    def _configurar_frame_controles(self):
        estilo_controles_basicos = SUCCESS
        estilo_controles_entrada = INFO
        estilo_controles_entrada_clasificar = WARNING
        estilo_controles_validacion = DANGER
        estilo_botones_basicos = "SUCCESS-OUTLINE"
        estilo_botones_entrada = "INFO-OUTLINE"
        estilo_botones_entrada_clasificar = "WARNING-OUTLINE"
        estilo_botones_validacion = "DANGER-OUTLINE"

        self.marco_frames_controles.columnconfigure(0, weight=1)

        # Frame controles basicos
        self.frame_controles_basicos = ttk.Labelframe(self.marco_frames_controles, text="Controles básicos", bootstyle=estilo_controles_basicos,padding=10)
        self.frame_controles_basicos.grid(row=0, column=0, sticky="new", pady=5)
        self.frame_controles_basicos.columnconfigure(0, weight=1)
        self.frame_controles_basicos.rowconfigure(1, weight=1)

        self.label_titulo_controles_basicos = ttk.Label(self.frame_controles_basicos, text="Controles básicos", font=("Segoe UI", 16, "bold"))
        self.label_titulo_controles_basicos.grid(row=0, column=0, pady=(0, 5))

        self.boton_borrar_datos_conjunto_datos = ttk.Button(self.frame_controles_basicos, text="Borrar datos del conjunto de datos", bootstyle=estilo_botones_basicos)
        self.boton_borrar_datos_conjunto_datos.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.boton_borrar_datos_clasificar = ttk.Button(self.frame_controles_basicos, text="Borrar datos para clasificar", bootstyle=estilo_botones_basicos)
        self.boton_borrar_datos_clasificar.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # Frame entrada
        self.frame_entrada_datos = ttk.Labelframe(self.marco_frames_controles, text="Entrada de datos", bootstyle=estilo_controles_entrada, padding=10)
        self.frame_entrada_datos.grid(row=1, column=0, sticky="new", pady=5)
        self.frame_entrada_datos.columnconfigure(0, weight=1)
        for i in range(1,5): self.frame_entrada_datos.rowconfigure(i, weight=1)

        self.label_titulo_entrada_datos = ttk.Label(self.frame_entrada_datos, text="Entrada de datos", font=("Segoe UI", 16, "bold"))
        self.label_titulo_entrada_datos.grid(row=0, column=0, pady=(0, 5))

        self.boton_crear_conjunto_datos_manualmente = ttk.Button(self.frame_entrada_datos, text="Crear conjunto de datos manualmente", bootstyle=estilo_botones_entrada)
        self.boton_crear_conjunto_datos_manualmente.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.boton_anadir_vector_a_conjunto_datos_manualmente = ttk.Button(self.frame_entrada_datos, text="Añadir vector de datos al conjunto", bootstyle=estilo_botones_entrada)
        self.boton_anadir_vector_a_conjunto_datos_manualmente.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.boton_crear_conjunto_datos_archivo = ttk.Button(self.frame_entrada_datos, text="Crear conjunto de datos desde archivo", bootstyle=estilo_botones_entrada)
        self.boton_crear_conjunto_datos_archivo.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.boton_anadir_vector_a_conjunto_datos_archivo = ttk.Button(self.frame_entrada_datos, text="Añadir vectores de datos al conjunto desde archivo", bootstyle=estilo_botones_entrada)
        self.boton_anadir_vector_a_conjunto_datos_archivo.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        # Frame entrada de datos para clasificar
        self.frame_entrada_datos_clasificar = ttk.Labelframe(self.marco_frames_controles, text="Entrada de datos para clasificar", bootstyle=estilo_controles_entrada_clasificar, padding=10)
        self.frame_entrada_datos_clasificar.grid(row=2, column=0, sticky="new", pady=5)
        self.frame_entrada_datos_clasificar.columnconfigure(0, weight=1)
        for i in range(1,5): self.frame_entrada_datos_clasificar.rowconfigure(i, weight=1)

        self.label_titulo_entrada_datos_clasificar = ttk.Label(self.frame_entrada_datos_clasificar, text="Entrada de datos para clasificar", font=("Segoe UI", 16, "bold"))
        self.label_titulo_entrada_datos_clasificar.grid(row=0, column=0, pady=(0, 5))

        self.boton_anadir_vector_a_conjunto_datos_clasificar_manualmente = ttk.Button(self.frame_entrada_datos_clasificar, text="Añadir vector de datos al conjunto para clasificar", bootstyle=estilo_botones_entrada_clasificar)
        self.boton_anadir_vector_a_conjunto_datos_clasificar_manualmente.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.boton_clasificar_por_distancia_minima = ttk.Button(self.frame_entrada_datos_clasificar, text="Clasificar por distancia minima", bootstyle=estilo_botones_entrada_clasificar)
        self.boton_clasificar_por_distancia_minima.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.boton_clasificar_por_knn = ttk.Button(self.frame_entrada_datos_clasificar, text="Clasificar por KNN", bootstyle=estilo_botones_entrada_clasificar)
        self.boton_clasificar_por_knn.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        # FRrame de algoritmos de validacion
        self.frame_algoritmos_validacion = ttk.Labelframe(self.marco_frames_controles, text="Algoritmos de validacion", bootstyle=estilo_controles_validacion, padding=10)
        self.frame_algoritmos_validacion.grid(row=3, column=0, sticky="new", pady=5)
        self.frame_algoritmos_validacion.columnconfigure(0, weight=1)
        for i in range(1,4): self.frame_algoritmos_validacion.rowconfigure(i, weight=1)

        self.label_titulo_algoritmos_validacion = ttk.Label(self.frame_algoritmos_validacion, text="Algoritmos de validacion", font=("Segoe UI", 16, "bold"))
        self.label_titulo_algoritmos_validacion.grid(row=0, column=0, pady=(0, 5))

        self.boton_validacion_train_and_test = ttk.Button(self.frame_algoritmos_validacion, text="Validacion por train and test", bootstyle=estilo_botones_validacion)
        self.boton_validacion_train_and_test.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.boton_validacion_k_fold = ttk.Button(self.frame_algoritmos_validacion, text="Validacion por k fold", bootstyle=estilo_botones_validacion)
        self.boton_validacion_k_fold.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.boton_validacion_bootstrap = ttk.Button(self.frame_algoritmos_validacion, text="Validacion por bootstrap", bootstyle=estilo_botones_validacion)
        self.boton_validacion_bootstrap.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    
    def crear_tabla(self, datos, nombre_atributos, modalidad):
        if modalidad == "conjunto":
            if hasattr(self, "label_preview_tabla_conjunto_datos"):
                self.label_preview_tabla_conjunto_datos.destroy()
            if hasattr(self, "tabla_conjunto"):
                self.tabla_conjunto.destroy()
        elif modalidad == "clasificar":
            if hasattr(self, "label_preview_tabla_clasificar"):
                self.label_preview_tabla_clasificar.destroy()
            if hasattr(self, "tabla_clasificar"):
                self.tabla_clasificar.destroy()
        
        titulos_columnas = ("Ind", *nombre_atributos)

        Tabla = ttk.Treeview(self.frame_tabla,
            columns=titulos_columnas,
            show="headings",
            height=min(len(datos), 10))

        for i, col in enumerate(titulos_columnas):
            if i == 0:
                Tabla.column(col, width=50, anchor="center")
            else:
                Tabla.column(col, width=100, anchor="center")
            Tabla.heading(col, text=col)

        for linea in datos:
            Tabla.insert(parent="", index="end", values=linea)

        if modalidad == "conjunto":
            self.tabla_conjunto = Tabla
            Tabla.grid(row=2, column=0, sticky="n", pady=15)
        elif modalidad == "clasificar":
            self.tabla_clasificar = Tabla
            Tabla.grid(row=4, column=0, sticky="n", pady=15)

    def reiniciar_tabla(self, modalidad):
        if modalidad == "conjunto":
            if hasattr(self, "tabla_conjunto"):
                self.tabla_conjunto.destroy()
            self.label_preview_tabla_conjunto_datos = ttk.Label(self.frame_tabla, text="Cargue un archivo o ingrese datos manualmente para ver su contenido", font=("Segoe UI", 14), foreground="#e0e0e0")
            self.label_preview_tabla_conjunto_datos.grid(row=2, column=0, pady=(0, 10))
        elif modalidad == "clasificar":
            if hasattr(self, "tabla_clasificar"):
                self.tabla_clasificar.destroy()
            self.label_preview_tabla_clasificar = ttk.Label(self.frame_tabla, text="Ingrese datos manualmente para ver su contenido", font=("Segoe UI", 14), foreground="#e0e0e0")
            self.label_preview_tabla_clasificar.grid(row=4, column=0, pady=(0, 10))

    # FUNCIONES DE PREGUNTAR DATOS O MOSTRAR MENSAJES
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

    def preguntar_k(self, valor_maximo):
        k = simpledialog.askinteger("K", "Ingrese el valor de K", minvalue=1 , maxvalue=valor_maximo)
        if k:
            return k
        else:
            return None

    def preguntar_usar_manhattan(self):
        usar_manhattan = messagebox.askyesno("Usar Manhattan", "¿Desea usar la distancia Manhattan?")
        if usar_manhattan:
            return True
        else:
            return False

    def preguntar_algoritmo(self):
        algoritmo = messagebox.askyesno("Algoritmo", "¿Desea usar el algoritmo de KNN?")
        if algoritmo:
            return True
        else:
            return False

    def preguntar_porcentaje(self):
        porcentaje = simpledialog.askinteger("Porcentaje", "Ingrese el porcentaje de entrenamiento", minvalue=1 , maxvalue=100)
        if porcentaje:
            return porcentaje
        else:
            return None

    def preguntar_k_divisiones(self, valor_maximo):
        k_divisiones = simpledialog.askinteger("K", "Ingrese el valor de K, es decir, en cuantas divisiones se va a dividir el conjunto de datos", minvalue=2 , maxvalue=valor_maximo)
        if k_divisiones:
            return k_divisiones
        else:
            return None

    def preguntar_cantidad_experimentos(self):
        cantidad_experimentos = simpledialog.askinteger("Cantidad de experimentos", "Ingrese la cantidad de experimentos", minvalue=1, maxvalue=50)
        if cantidad_experimentos:
            return cantidad_experimentos
        else:
            return None

    def preguntar_cantidad_muestras_aprendizaje(self, valor_maximo):
        cantidad_muestras_aprendizaje = simpledialog.askinteger("Cantidad de muestras de aprendizaje", "Ingrese la cantidad de muestras de aprendizaje", minvalue=1, maxvalue=valor_maximo)
        if cantidad_muestras_aprendizaje:
            return cantidad_muestras_aprendizaje
        else:
            return None
    
    def preguntar_cantidad_muestras_clasificacion(self, valor_maximo):
        cantidad_muestras_test = simpledialog.askinteger("Cantidad de muestras de test", "Ingrese la cantidad de muestras de test", minvalue=1, maxvalue=valor_maximo)
        if cantidad_muestras_test:
            return cantidad_muestras_test
        else:
            return None

    def mostrar_mensaje(self, mensaje, tipo_mensaje="info"):
        if tipo_mensaje == "info":
            messagebox.showinfo("Información", mensaje)
        elif tipo_mensaje == "error":
            messagebox.showerror("Error", mensaje)
        elif tipo_mensaje == "warning":
            messagebox.showwarning("Advertencia", mensaje)

    def mostrar_resultados_train_and_test(self, tupla_resultados):
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()
        self.label_aciertos = ttk.Label(self.frame_resultados, text=f"Aciertos: {tupla_resultados[0]}")
        self.label_aciertos.pack(pady=2)

        self.label_errores = ttk.Label(self.frame_resultados, text=f"Errores: {tupla_resultados[1]}")
        self.label_errores.pack(pady=2)

        self.label_porcentaje_eficiencia = ttk.Label(self.frame_resultados, text=f"Porcentaje de eficiencia: {tupla_resultados[2]}%")
        self.label_porcentaje_eficiencia.pack(pady=2)

        self.label_porcentaje_errores = ttk.Label(self.frame_resultados, text=f"Porcentaje de errores: {tupla_resultados[3]}%")
        self.label_porcentaje_errores.pack(pady=2)

    def mostrar_resultados_k_fold_cross_validation(self, lista_resultados):
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()
        lista_resultados_eficiencia_errores = lista_resultados[0]
        desviacion_estandar = lista_resultados[1]
        desviacion_estandar_error = lista_resultados[2]
        for i, resultado in enumerate(lista_resultados_eficiencia_errores):
            if i != len(lista_resultados_eficiencia_errores)-1:
                self.label_aciertos = ttk.Label(self.frame_resultados, text=f"Grupo {i+1}: Aciertos: {resultado['aciertos']}")
                self.label_aciertos.grid(row=i, column=0, pady=2)

                self.label_errores = ttk.Label(self.frame_resultados, text=f"Grupo {i+1}: Errores: {resultado['errores']}")
                self.label_errores.grid(row=i, column=1, pady=2)

                self.label_porcentaje_eficiencia = ttk.Label(self.frame_resultados, text=f"Grupo {i+1}: Porcentaje de eficiencia: {resultado['porcentaje_eficiencia']}%")
                self.label_porcentaje_eficiencia.grid(row=i, column=2, pady=2)

                self.label_porcentaje_errores = ttk.Label(self.frame_resultados, text=f"Grupo {i+1}: Porcentaje de errores: {resultado['porcentaje_errores']}%")
                self.label_porcentaje_errores.grid(row=i, column=3, pady=2)
            else:
                self.label_aciertos_globales = ttk.Label(self.frame_resultados, text=f"Aciertos globales: {resultado['aciertos']}")
                self.label_aciertos_globales.grid(row=i, column=0, pady=2)

                self.label_errores_globales = ttk.Label(self.frame_resultados, text=f"Errores globales: {resultado['errores']}")
                self.label_errores_globales.grid(row=i, column=1, pady=2)

                self.label_porcentaje_eficiencia_global = ttk.Label(self.frame_resultados, text=f"Porcentaje de eficiencia global: {resultado['porcentaje_eficiencia']}%")
                self.label_porcentaje_eficiencia_global.grid(row=i, column=2, pady=2)

                self.label_porcentaje_errores_global = ttk.Label(self.frame_resultados, text=f"Porcentaje de errores global: {resultado['porcentaje_errores']}%")
                self.label_porcentaje_errores_global.grid(row=i, column=3, pady=2)
            
        self.label_desviacion_estandar = ttk.Label(self.frame_resultados, text=f"Desviación estándar: {desviacion_estandar}")
        self.label_desviacion_estandar.grid(row=i+1, column=2, pady=2)

        self.label_desviacion_estandar_error = ttk.Label(self.frame_resultados, text=f"Desviación estándar de errores: {desviacion_estandar_error}")
        self.label_desviacion_estandar_error.grid(row=i+1, column=3, pady=2)

    def mostrar_resultados_bootstrap(self, lista_resultados):
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()
        historial_metricas, resultados_globales, desviacion_eficiencia, desviacion_errores = lista_resultados


    #FUNCIONES DE CREACION DE VENTANAS PARA OBTENCION DE VALORES O DATOS
    def crear_ventana_creacion_conjunto_datos(self):
        if hasattr(self, "ventana_creacion_conjunto_datos") and self.ventana_creacion_conjunto_datos.winfo_exists():
            self.ventana_creacion_conjunto_datos.destroy()

        self.ventana_creacion_conjunto_datos = ttk.Toplevel(self)
        self.ventana_creacion_conjunto_datos.title("Crear conjunto de datos")
        self.ventana_creacion_conjunto_datos.geometry("400x400")
        self.lista_entradas = []

        self.frame_vector_entradas = ttk.Frame(self.ventana_creacion_conjunto_datos)
        self.frame_vector_entradas.pack(pady=10, fill="both", expand=True)

        self.btn_agregar = ttk.Button(self.ventana_creacion_conjunto_datos, text="+ Añadir entrada")
        self.btn_agregar.pack(pady=5)
        self.btn_guardar_conjunto_datos = ttk.Button(self.ventana_creacion_conjunto_datos, text="Guardar vector")
        self.btn_guardar_conjunto_datos.pack(pady=10, side="bottom")
        
    def agregar_input(self):
        if len(self.lista_entradas) == 10:
            self.mostrar_mensaje("Se ha alcanzado el maximo de entradas", "warning")
            return

        numero_actual = len(self.lista_entradas)+1
        
        fila = ttk.Frame(self.frame_vector_entradas)
        fila.pack(pady=2)

        label_nuevo = ttk.Label(fila, text=f"Atributo {numero_actual}:")
        label_nuevo.pack(side="left", padx=5)

        entrada_nueva = ttk.Entry(fila)
        entrada_nueva.pack(side="left", padx=5)
        self.lista_entradas.append(entrada_nueva)

    def obtener_vector_entrada(self):
        if len(self.lista_entradas) == 0:
            return "No se han ingresado entradas"
        if len (self.lista_entradas) < 2:
            return "Se requieren al menos 2 entradas"

        vector_entrada = []
        for entrada in self.lista_entradas:
            valor_campo_entrada = entrada.get().strip()
            if valor_campo_entrada == "":
                return "Se requiere que los campos no esten vacios"
            else:
                vector_entrada.append(valor_campo_entrada)
        return vector_entrada

    def crear_ventana_anadir_vector_a_conjunto_datos(self, tuplaAtributos):
        if hasattr(self, "ventana_anadir_vector_a_conjunto_datos") and self.ventana_anadir_vector_a_conjunto_datos.winfo_exists():
            self.ventana_anadir_vector_a_conjunto_datos.destroy()

        self.ventana_anadir_vector_a_conjunto_datos = ttk.Toplevel(self)
        self.ventana_anadir_vector_a_conjunto_datos.title("Anadir vector a conjunto de datos")
        self.ventana_anadir_vector_a_conjunto_datos.geometry("800x600")
        self.lista_entradas = []

        self.frame_vector_entradas = ScrolledFrame(self.ventana_anadir_vector_a_conjunto_datos)
        self.frame_vector_entradas.pack(pady=10, fill="both", expand=True)

        for i in range(len(tuplaAtributos)):
            fila = ttk.Frame(self.frame_vector_entradas)
            fila.pack(pady=2)

            label_nuevo = ttk.Label(fila, text=f"{tuplaAtributos[i][0]} de tipo {tuplaAtributos[i][1]} :")
            label_nuevo.pack(side="left", padx=5)

            entrada_nueva = ttk.Entry(fila)
            entrada_nueva.pack(side="left", padx=5)
            self.lista_entradas.append(entrada_nueva)

        self.btn_guardar_conjunto_datos = ttk.Button(self.ventana_anadir_vector_a_conjunto_datos, text="Guardar vector")
        self.btn_guardar_conjunto_datos.pack(pady=10, side="bottom")

    def crear_ventana_anadir_vector_a_conjunto_datos_clasificar(self, tupla_atributos):
        if hasattr(self, "ventana_anadir_vector_a_conjunto_datos_clasificar") and self.ventana_anadir_vector_a_conjunto_datos_clasificar.winfo_exists():
            self.ventana_anadir_vector_a_conjunto_datos_clasificar.destroy()

        self.ventana_anadir_vector_a_conjunto_datos_clasificar = ttk.Toplevel(self)
        self.ventana_anadir_vector_a_conjunto_datos_clasificar.title("Anadir vector a conjunto de datos")
        self.ventana_anadir_vector_a_conjunto_datos_clasificar.geometry("800x600")

        self.frame_vector_entradas = ttk.Frame(self.ventana_anadir_vector_a_conjunto_datos_clasificar)
        self.frame_vector_entradas.pack(pady=10, fill="both", expand=True)
        for i in range(3): self.frame_vector_entradas.columnconfigure(i, weight=1)
        self.frame_vector_entradas.rowconfigure(0, weight=1)
        for i in range(len(tupla_atributos)+1): self.frame_vector_entradas.rowconfigure(i+1, weight=1)

        label_titulo = ttk.Label(self.frame_vector_entradas, text="Configure el vector a clasificar:")
        label_titulo.grid(row=0, column=0, columnspan=3, pady=10)

        self.lista_entradas = []
        for i in range(len(tupla_atributos)):
            label_nombre_atributo = ttk.Label(self.frame_vector_entradas, text=f"{tupla_atributos[i][0]} de tipo {tupla_atributos[i][1]}")
            label_nombre_atributo.grid(row=i+1, column=0, pady=2)

            entrada_atributo = ttk.Entry(self.frame_vector_entradas)
            entrada_atributo.grid(row=i+1, column=1, pady=2)

            configuracion_atributo = ttk.Combobox(self.frame_vector_entradas, values=("Entrada", "Salida", "Ningun uso"), state="readonly")
            configuracion_atributo.grid(row=i+1, column=2, pady=2)
            configuracion_atributo.current(0)

            self.lista_entradas.append((entrada_atributo, configuracion_atributo))

        self.btn_guardar_vector = ttk.Button(self.frame_vector_entradas, text="Guardar vector")
        self.btn_guardar_vector.grid(row=len(tupla_atributos)+1, column=0, columnspan=3, pady=10)
        
    def obtener_vector_entrada_clasificar(self):
        vector_entrada_modo_tupla = []
        numero_salidas = 0
        numero_entrada = 0
        for i, entrada in enumerate(self.lista_entradas):
            if entrada[1].get() == "Entrada":
                valor = entrada[0].get().strip()
                if valor == "":
                    return "Se requiere que los campos de tipo entrada no esten vacios"
                else:
                    vector_entrada_modo_tupla.append((valor, entrada[1].get()))
                    numero_entrada+=1
            elif entrada[1].get() == "Salida":
                valor = "Pendiente"
                vector_entrada_modo_tupla.append((valor, entrada[1].get()))
                numero_salidas+=1
            elif entrada[1].get() == "Ningun uso":
                valor = "Sin uso"
                vector_entrada_modo_tupla.append((valor, entrada[1].get()))

        if numero_entrada < 2:
            return "Se requiere al menos 2 atributos de tipo entrada"
        if numero_salidas < 1:
            return "Se requiere al menos 1 atributo de tipo salida"

        return vector_entrada_modo_tupla

    def crear_ventana_seleccionar_atributos(self, tupla_atributos):
        if hasattr(self, "ventana_seleccionar_atributos") and self.ventana_seleccionar_atributos.winfo_exists():
            self.ventana_seleccionar_atributos.destroy()

        self.ventana_seleccionar_atributos = ttk.Toplevel(self)
        self.ventana_seleccionar_atributos.title("Seleccionar atributos")
        self.ventana_seleccionar_atributos.geometry("800x600")

        self.frame_atributos = ttk.Frame(self.ventana_seleccionar_atributos)
        self.frame_atributos.pack(pady=10, fill="both", expand=True)

        self.lista_configuraciones = []
        for i in range(len(tupla_atributos)):
            fila = ttk.Frame(self.frame_atributos)
            fila.pack(pady=2)

            label_nuevo = ttk.Label(fila, text=f"{tupla_atributos[i][0]} de tipo {tupla_atributos[i][1]} :")
            label_nuevo.pack(side="left", padx=5)

            configuracion_atributo = ttk.Combobox(fila, values=("Entrada", "Salida", "Ningun uso"), state="readonly")
            configuracion_atributo.pack(side="left", padx=5)
            configuracion_atributo.current(0)
            self.lista_configuraciones.append(configuracion_atributo)

        self.btn_seleccionar_atributos = ttk.Button(self.frame_atributos, text="Seleccionar atributos")
        self.btn_seleccionar_atributos.pack(pady=10, side="bottom")

    def obtener_atributos(self):
        atributos = []
        numero_entrada = 0
        numero_salidas = 0
        for atributo in self.lista_configuraciones:
            if atributo.get() == "Entrada":
                numero_entrada+=1
            elif atributo.get() == "Salida":
                numero_salidas+=1
            atributos.append(atributo.get())
        if numero_entrada < 2:
            return "Se requiere al menos 2 atributos de tipo entrada"
        if numero_salidas < 1:
            return "Se requiere al menos 1 atributo de tipo salida"
        return atributos


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()