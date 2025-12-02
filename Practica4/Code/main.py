from View.mainWindow import MainWindow
from Model.modelo import Modelo
from Controller.controlador import Controlador


def main():
    vista = MainWindow()
    modelo = Modelo()
    controlador = Controlador(modelo, vista) 
    vista.mainloop()

if __name__ == "__main__":
    main()