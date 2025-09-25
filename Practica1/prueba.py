import ttkbootstrap as tb
from tkinter import Toplevel, Label

def abrir_ventana():
    # Crea la ventana secundaria
    top = Toplevel(root)
    top.title("Ventana secundaria")
    top.geometry("300x200")

    # Se le pueden aplicar estilos de ttkbootstrap también
    lbl = tb.Label(top, text="Hola! Soy una ventana toplevel", bootstyle="success")
    lbl.pack(pady=20)

# Ventana principal
root = tb.Window(themename="superhero")
root.title("Ventana principal")
root.geometry("400x300")

btn = tb.Button(root, text="Abrir ventana", bootstyle="info", command=abrir_ventana)
btn.pack(pady=50)

root.mainloop()
