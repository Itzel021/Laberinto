import pygame
import time
from juego import ejecutar_laberinto

pygame.init()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ANCHO, ALTO = 960, 650
tiempo_inicio = time.time()
fuente = pygame.font.Font(None, 30)
fuenteHorizontal = pygame.font.Font(None, 50)

imagen_pared1 = pygame.image.load('./img/pared1.png')
imagen_pared1 = pygame.transform.scale(imagen_pared1, (15, 15))
imagen_pared2 = pygame.image.load('./img/pared2.png')
imagen_pared2 = pygame.transform.scale(imagen_pared2, (15, 15))
imagen_pared3 = pygame.image.load('./img/pared3.png')
imagen_pared3 = pygame.transform.scale(imagen_pared3, (15, 15))


# Función para dibujar la pantalla del juego
def mostrar_juego(dificultad_seleccionada, enemigos, recompensas, mejoras):

    if dificultad_seleccionada == "Fácil":
        nivel = "Fácil"
        ejecutar_laberinto(nivel, enemigos, recompensas, mejoras, imagen_pared1)
        
    elif dificultad_seleccionada == "Medio":
        nivel = "Medio"
        ejecutar_laberinto(nivel, enemigos, recompensas, mejoras, imagen_pared2)

    elif dificultad_seleccionada == "Difícil":
        nivel = "Difícil"
        ejecutar_laberinto(nivel, enemigos, recompensas, mejoras, imagen_pared3)


