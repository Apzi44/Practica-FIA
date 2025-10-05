class formatoInvalidoArchivo(Exception):
    def __init__(self, codigoError):
        if codigoError == 1:
            mensaje= "El archivo esta vacio, por favor verifique el archivo, no se cargo el mapa."
        elif codigoError == 2:
            mensaje= "El archivo debe contener al menos 4 lineas para ser considerado un mapa valido."
        elif codigoError == 3.1:
            mensaje= "El archivo contiene lineas con formato incorrecto para el mapa base. Cada linea debe contener al menos tres valores alfanumericos separados por comas"
        elif codigoError == 3.2:
            mensaje= "El archivo contiene lineas con formato incorrecto para el mapa adicional. Los valores pueden estar vacios o ser alfanumericos, si hay mas de un valor deben estar entre parentesis y separados por comillas dobles."
        elif codigoError == 4:
            mensaje= "El archivo contiene valores invalidos para un mapa binario o mixto, por favor verifique el formato del archivo, no se cargo el mapa. En un mapa binario los valores permitidos son 0 y 1, en un mapa mixto los valores permitidos son 0, 1, 2, 3 y 4."
        elif codigoError == 5:
            mensaje= "El archivo contiene valores invalidos para crear el mapa. El mapa debe contener un unico punto de inicio (I) y un unico punto final (F)."
        super().__init__(mensaje)

class extensionInvalida(Exception):
    def __init__(self, codigoError):
        if codigoError == 1:
            mensaje= "El archivo contiene lineas con diferente cantidad de valores, por favor verifique el formato del archivo, no se cargo el mapa."
        elif codigoError == 2:
            mensaje= "El archivo contiene lineas con mayor cantidad de valores o más lineas de las que tiene el mapa, por favor verifique el formato del archivo, solo se le mostrara el mapa sin valores adicionales."
        super().__init__(mensaje)
    
class excepcionProcesadoValores(Exception):
    def __init__(self):
        mensaje= "El archivo del mapa base debe cargarse con valores numericos enteros"
        super().__init__(mensaje)