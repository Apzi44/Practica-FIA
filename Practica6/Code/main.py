from View.mainWindow import MainWindow
from Model.modelo import Modelo
from Controller.controlador import Controlador
#Martinez Alor Zaddkiel de Jesus

def main():
    vista = MainWindow()
    modelo = Modelo()
    controlador = Controlador(modelo, vista)
    vista.mainloop()

if __name__ == "__main__":
    main()