class Coordenada:
    def __init__(self, valor, coordenadaX, coordenadaY):
        self.valor= valor
        self.coordenadaX= coordenadaX
        self.coordenadaY= coordenadaY
        self.visitado= False
        self.visible = False
        self.puntoDesicion = False
        self.puntoClave = None
        self.costoViaje = None

    def __str__(self):
        return f"La coordenada [{chr(65+self.coordenadaX)},{self.coordenadaY+1}] tiene el valor de:{self.valor}"