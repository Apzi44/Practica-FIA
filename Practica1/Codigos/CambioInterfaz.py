import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk  # 🔥 Tema moderno
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import mapa as mp


class Interfaz(ttk.Window):  # Usamos ttkbootstrap para estilo
    def __init__(self):
        super().__init__(themename="darkly")  # Cambia a "flatly" o "cosmo" si prefieres
        self.title("Mapa Interactivo - IA")
        self.geometry("1300x700")
        self.resizable(False, False)

        self.mapa = None
        self._crear_layout()
        self.mainloop()

    # ==================== DISEÑO BASE ==================== #
    def _crear_layout(self):
        # Panel izquierdo (control)
        self.panel = ttk.Frame(self, padding=15, bootstyle=SECONDARY)
        self.panel.pack(side=LEFT, fill=Y)

        # Panel derecho (mapa)
        self.frame_mapa = ttk.Frame(self, padding=10)
        self.frame_mapa.pack(side=RIGHT, fill=BOTH, expand=True)

        # Título
        ttk.Label(
            self.panel, text="🌎 Interfaz de Mapa", font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # Botones principales
        ttk.Button(
            self.panel, text="📂 Cargar Mapa", bootstyle=SUCCESS, command=self.cargar_mapa
        ).pack(fill=X, pady=8)
        ttk.Button(
            self.panel,
            text="🤖 Crear Agente",
            bootstyle=INFO,
            command=self.cargar_agente,
        ).pack(fill=X, pady=8)

        # Sección obtener valor
        self._seccion_obtener()

        # Sección modificar valor
        self._seccion_modificar()

    def _seccion_obtener(self):
        marco = ttk.Labelframe(
            self.panel, text="Consultar valor", padding=10, bootstyle=PRIMARY
        )
        marco.pack(fill=X, pady=15)

        self.x_get = ttk.Entry(marco, width=5)
        self.y_get = ttk.Entry(marco, width=5)
        self.x_get.insert(0, "A")
        self.y_get.insert(0, "1")

        ttk.Label(marco, text="x").pack()
        self.x_get.pack(pady=5)
        ttk.Label(marco, text="y").pack()
        self.y_get.pack(pady=5)

        ttk.Button(
            marco, text="🔍 Consultar valor", bootstyle=PRIMARY, command=self.obtener_valor
        ).pack(fill=X, pady=5)

        self.resultado = ttk.Label(marco, text="Valor: -", font=("Segoe UI", 12))
        self.resultado.pack(pady=5)

    def _seccion_modificar(self):
        marco = ttk.Labelframe(
            self.panel, text="Modificar valor", padding=10, bootstyle=DANGER
        )
        marco.pack(fill=X, pady=15)

        # Etiqueta "modificar" en letras blancas sobre el fondo rojo
        etiqueta_modificar = ttk.Label(
            marco, 
            text="modificar", 
            font=("Segoe UI", 8, "bold"),
            foreground="white",  # Letras blancas
            background="#dc3545"  # Fondo rojo (color DANGER de ttkbootstrap)
        )
        etiqueta_modificar.pack(pady=(0, 10))

        # Campos de entrada
        self.x_mod = ttk.Entry(marco, width=5)
        self.y_mod = ttk.Entry(marco, width=5)
        self.val_mod = ttk.Entry(marco, width=5)

        for entry, val, lbl in [
            (self.x_mod, "A", "x"),
            (self.y_mod, "1", "y"),
            (self.val_mod, "0", "Nuevo valor"),
        ]:
            entry.insert(0, val)
            ttk.Label(marco, text=lbl).pack()
            entry.pack(pady=5)

        # Botón que realiza los cambios ("Modificar")
        self.btn_modificar = ttk.Button(
            marco,
            text="Modificar",     
            bootstyle=DANGER,
            command=self.modificar_valor,
        )
        self.btn_modificar.pack(fill=X, pady=5)

    # ==================== FUNCIONES ==================== #
    def cargar_mapa(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos TXT/CSV", "*.txt *.csv")],
        )
        if not archivo:
            return

        self.mapa = mp.Mapa()
        if not self.mapa.leerArchivo(archivo):
            messagebox.showerror("Error", "No se pudo cargar el mapa.")
            self.mapa = None
            return

        self._dibujar_mapa()

    def cargar_agente(self):
        if not self.mapa:
            messagebox.showinfo("Aviso", "Primero carga un mapa.")
            return
        messagebox.showinfo("Agente", "Aquí podrías crear tu agente personalizado.")

    def obtener_valor(self):
        if not self.mapa:
            messagebox.showinfo("Error", "Carga un mapa primero.")
            return
        try:
            x, y = self._coords(self.x_get.get(), self.y_get.get())
            valor = self.mapa.pedirCoordenada(x, y)
            self.resultado.config(text=f"Valor: {valor}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def modificar_valor(self):
        if not self.mapa:
            messagebox.showinfo("Error", "Carga un mapa primero.")
            return
        try:
            x, y = self._coords(self.x_mod.get(), self.y_mod.get())
            nuevo = int(self.val_mod.get())
            self.mapa.pedirCoordenada(x, y).valor = nuevo
            messagebox.showinfo(
                "Éxito", f"Coordenada [{x},{y}] modificada a {nuevo}."
            )
            self._dibujar_mapa()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _coords(self, x, y):
        if not x.isalpha() or not y.isdigit():
            raise ValueError("x debe ser letra y y un número.")
        return ord(x.upper()) - 65, int(y) - 1

    def _dibujar_mapa(self):
        for w in self.frame_mapa.winfo_children():
            w.destroy()

        matriz = self.mapa.crearMatrizTerreno()
        colores = ListedColormap(["#1f77b4", "#d62728", "#2ca02c", "#f0ad4e", "#9467bd"])
        limites = [-0.5] + [i + 0.5 for i in range(len(colores.colors))]
        norm = BoundaryNorm(limites, colores.N)

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.set_title("Mapa del Terreno", fontsize=16, fontweight="bold")
        ax.pcolormesh(matriz, cmap=colores, norm=norm, edgecolors="black")
        ax.set_xticks([i + 0.5 for i in range(self.mapa.ancho)])
        ax.set_yticks([i + 0.5 for i in range(self.mapa.alto)])
        ax.set_xticklabels([chr(65 + i) for i in range(self.mapa.ancho)])
        ax.set_yticklabels([i + 1 for i in range(self.mapa.alto)])
        ax.invert_yaxis()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_mapa)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    Interfaz()