import pygame
import time

# Inicializa Pygame y el mixer
pygame.init()
pygame.mixer.init()

# Cargar y reproducir música de fondo
pygame.mixer.music.load("fondo.mp3")
pygame.mixer.music.play(-1)

# Cargar efecto de sonido
sonido_efecto = pygame.mixer.Sound("efecto.mp3")

# Ajustar volúmenes
pygame.mixer.music.set_volume(0.5)
sonido_efecto.set_volume(0.7)

# Simulación de un juego
try:
    while True:
        # Reproducir efecto al presionar Enter
        input("Presiona Enter para reproducir un efecto...")
        sonido_efecto.play()

except KeyboardInterrupt:
    # Detener música al salir
    pygame.mixer.music.stop()
    pygame.quit()
