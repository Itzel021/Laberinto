import pygame
import sys
from pantallaJuego import mostrar_juego

# Inicializar pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 960, 650
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego del laberinto")

# Cargar imagen de fondo
fondo = pygame.image.load("./img/fondoInicio.jpg")  # Reemplaza "fondoInicio.jpg" con la ruta de tu imagen
fondo = pygame.transform.scale(fondo, (800, ALTO))  # Escalar la imagen al tamaño de la ventana

# Cargar imágenes de enemigos, recompensas y mejoras
imagen_enemigo = pygame.image.load("./img/enemigo.jpg")  # Reemplaza con la ruta de la imagen del enemigo
imagen_enemigo = pygame.transform.scale(imagen_enemigo, (160, 160))  # Escalar imagen del enemigo
imagen_recompensa = pygame.image.load("./img/recompensas.jpg")  # Reemplaza con la ruta de la imagen de la recompensa
imagen_recompensa = pygame.transform.scale(imagen_recompensa, (160, 160))  # Escalar imagen de la recompensa
imagen_mejoras = pygame.image.load("./img/mejoras.jpg")  # Reemplaza con la ruta de la imagen de la mejora
imagen_mejoras = pygame.transform.scale(imagen_mejoras, (160, 160))  # Escalar imagen de la mejora

# Cargar imagen del botón "play"
imagen_play = pygame.image.load("./img/game.png")  # Imagen normal del botón play
imagen_play_seleccionado = pygame.image.load("./img/game.png")  # Imagen del botón play seleccionado
imagen_play = pygame.transform.scale(imagen_play, (50, 50))  # Escalar imagen del botón
imagen_play_seleccionado = pygame.transform.scale(imagen_play_seleccionado, (50, 50))  # Escalar imagen seleccionada

# Colores
NEGRO = (0, 0, 0)
GRIS_CLARO = (170, 170, 170)
GRIS_OSCURO = (100, 100, 100)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)

# Fuente
fuente = pygame.font.Font(None, 40)
fuente_grande = pygame.font.Font(None, 50)  # Fuente más grande para los números

# Opciones del menú
opciones = ["Fácil", "Medio", "Difícil"]

# Posiciones de los botones (alineados a la izquierda)
boton_rects = [
    pygame.Rect(50, 200, 160, 40),  # Botón "Fácil"
    pygame.Rect(50, 260, 160, 40),  # Botón "Medio"
    pygame.Rect(50, 320, 160, 40)    # Botón "Difícil"
]
# Variables para el estado del juego
pantalla_juego = False  # Indica si estamos en el menú o en el juego
dificultad_seleccionada = "Fácil"  # Variable para la dificultad seleccionada

# Variables de dificultad
enemigos = 0
recompensas = 0
mejoras = 0

# Función para ajustar la cantidad de enemigos y recompensas según la dificultad
def ajustar_dificultad(dificultad):
    global enemigos, recompensas, mejoras
    if dificultad == "Fácil":
        enemigos = 3
        recompensas = 10
        mejoras = 5
    elif dificultad == "Medio":
        enemigos = 5
        recompensas = 15
        mejoras = 4
    elif dificultad == "Difícil":
        enemigos = 7
        recompensas = 20
        mejoras = 3

# Función para dibujar los botones del menú
def dibujar_menu(seleccionado):
    ventana.blit(fondo, (0, 0))  # Dibujar la imagen de fondo

    for i, opcion in enumerate(opciones):
        # Cambiar color del botón si está seleccionado
        if i == seleccionado:
            pygame.draw.rect(ventana, VERDE, boton_rects[i])  # Color de fondo del botón seleccionado
        else:
            pygame.draw.rect(ventana, GRIS_CLARO, boton_rects[i])  # Color de los botones no seleccionados

        # Dibujar el texto encima del botón
        texto = fuente.render(opcion, True, NEGRO)
        ventana.blit(texto, (boton_rects[i].x + 10, boton_rects[i].y + 5))

    # Dibujar imagen del botón "play" en función de la opción seleccionada
    ventana.blit(imagen_play_seleccionado, (220, 200 + seleccionado * 60))  # Mover la imagen según la selección

# Función para dibujar enemigos y recompensas
def dibujar_enemigos_recompensas():
    # Dibujar enemigo a la derecha
    ventana.blit(imagen_enemigo, (ANCHO - 160, 0))  # Posición del enemigo
    texto_enemigos = fuente_grande.render(f"{enemigos}", True, BLANCO)  # Usar fuente más grande
    ventana.blit(texto_enemigos, (ANCHO - 160, 120))  # Posición del texto de enemigos

    # Dibujar recompensa a la derecha
    ventana.blit(imagen_recompensa, (ANCHO - 160, 200))  # Posición de la recompensa
    texto_recompensas = fuente_grande.render(f"{recompensas}", True, BLANCO)  # Usar fuente más grande
    ventana.blit(texto_recompensas, (ANCHO - 160, 320))  # Posición del texto de recompensas

    # Dibujar mejoras a la derecha
    ventana.blit(imagen_mejoras, (ANCHO - 160, 400))  # Posición de la mejora
    texto_mejoras = fuente_grande.render(f"{mejoras}", True, BLANCO)  # Usar fuente más grande
    ventana.blit(texto_mejoras, (ANCHO - 160, 520))  # Posición del texto de mejoras
    

# Ciclo principal
def main():
    global pantalla_juego, dificultad_seleccionada
    seleccionado = 0
    ajustar_dificultad(dificultad_seleccionada)
    ejecutando = True
    
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccionado = (seleccionado + 1) % len(opciones)
                    dificultad_seleccionada = opciones[seleccionado]
                    ajustar_dificultad(dificultad_seleccionada)
                elif evento.key == pygame.K_UP:
                    seleccionado = (seleccionado - 1) % len(opciones)
                    dificultad_seleccionada = opciones[seleccionado]
                    ajustar_dificultad(dificultad_seleccionada)
                # Cambiar a la pantalla del juego al presionar Enter
                elif evento.key == pygame.K_RETURN:
                    pantalla_juego = True  # Cambiar a la pantalla de juego

        if pantalla_juego:
            mostrar_juego(dificultad_seleccionada, enemigos, recompensas, mejoras)  
        else:
            dibujar_menu(seleccionado)
            dibujar_enemigos_recompensas()

        pygame.display.flip()

# Ejecutar el menú
main()
