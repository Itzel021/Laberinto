import pygame

pygame.init()
pygame.mixer.init()

# Ruta del archivo de música que quieres probar
pygame.mixer.music.load('./Sonidos/fon_facil.mp3')
pygame.mixer.music.set_volume(1.0)  # Volumen máximo
pygame.mixer.music.play(-1)  # Reproduce en bucle

input("Presiona Enter para detener el programa.")  # Pausa para escuchar la música
pygame.mixer.music.stop()  # Detiene la música cuando presionas Enter
