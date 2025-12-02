from ttkbootstrap.dialogs import Querybox


if __name__ == "__main__":
    filas = Querybox.get_integer("Ingrese el número de filas", title="Añadir fila", minvalue=1, maxvalue=10, parent=None)
    print(filas)
