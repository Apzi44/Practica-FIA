import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *

def mostrar_info():
    Messagebox.show_info("Información xdddd", "Este es un mensaje informativo.")

def mostrar_pregunta():
    respuesta = Messagebox.yesno("Confirmación", "¿Quieres continuar?")
    if respuesta == "Yes":
        Messagebox.show_info("Respuesta", "Elegiste Sí")
    else:
        Messagebox.show_warning("Respuesta", "Elegiste No")

root = ttk.Window(themename="cosmo")

ttk.Button(root, text="Info", bootstyle=INFO, command=mostrar_info).pack(pady=10)
ttk.Button(root, text="Pregunta", bootstyle=SUCCESS, command=mostrar_pregunta).pack(pady=10)

root.mainloop()
