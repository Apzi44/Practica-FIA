class Coordenada:
    def __init__(self, valor, coordenadaX, coordenadaY):
        self.valor= valor
        self.coordenadaX= coordenadaX
        self.coordenadaY= coordenadaY
        self.visitado= False
        self.visible = False
        self.puntoDecision = False
        self.puntoActual = False
        self.puntoInicialFinal = False
        self.puntoClave: str = None
        self.costoViaje: float = None
        self.avanzable: bool = True

    def __str__(self):
        return f"La coordenada [{chr(65+self.coordenadaX)},{self.coordenadaY+1}] tiene el valor de:{self.valor}"