import tkinter as tk
import pygame
from pygame.locals import *
import os

class PygameTk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter con Pygame")
        self.geometry("800x600")

        # Frame donde irá pygame
        self.embed = tk.Frame(self, width=600, height=400)
        self.embed.pack()

        # Iniciar pygame
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())  # "embed" en el frame
        os.environ['SDL_VIDEODRIVER'] = 'windib'  # para Windows (en Linux no se necesita normalmente)

        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.init()
        
        # Llamar al loop
        self.after(10, self.pygame_loop)

    def pygame_loop(self):
        # Rellenar pantalla
        self.screen.fill((30, 30, 30))

        # Dibujar un círculo que se mueve
        pygame.draw.circle(self.screen, (0, 200, 255), (300, 200), 50)

        pygame.display.update()

        # Repetir el loop dentro de Tkinter
        self.after(30, self.pygame_loop)

if __name__ == "__main__":
    app = PygameTk()
    app.mainloop()
