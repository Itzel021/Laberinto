import pygame
import sys
import time
import random
pygame.mixer.init()

RANGO_PERCEPCION = 30
DURACION_MEJORA = 3  # Duración de la mejora en segundos
VELOCIDAD_NORMAL = 1  # Velocidad normal
VELOCIDAD_MEJORADA = 2  # Velocidad mejorada

# Ruta del sonido de derrota
SONIDO_DERROTA = './Sonidos/perder.mp3'
SONIDO_MONEDA = './Sonidos/moneda.mp3'

def colocar_monedas(laberinto, recompensas):
    posiciones_disponibles = [(i, j) for i in range(len(laberinto)) for j in range(len(laberinto[0])) if laberinto[i][j] == 0]
    posiciones_monedas = random.sample(posiciones_disponibles, recompensas)
    return posiciones_monedas

def colocar_mejoras(laberinto, cantidad_mejoras):
    posiciones_disponibles = [(i, j) for i in range(len(laberinto)) for j in range(len(laberinto[0])) if laberinto[i][j] == 0]
    cantidad_mejoras = min(cantidad_mejoras, len(posiciones_disponibles))
    posiciones_mejoras = random.sample(posiciones_disponibles, cantidad_mejoras)
    return posiciones_mejoras

def colocar_enemigos(laberinto, cantidad_enemigos):
    posiciones_disponibles = [(i, j) for i in range(len(laberinto)) for j in range(len(laberinto[0])) if laberinto[i][j] == 0]
    cantidad_enemigos = min(cantidad_enemigos, len(posiciones_disponibles))
    posiciones_iniciales = random.sample(posiciones_disponibles, cantidad_enemigos)
    posiciones_enemigos = [{"pos_actual": pos, "pos_inicial": pos} for pos in posiciones_iniciales]
    return posiciones_enemigos

def mover_enemigos(posiciones_enemigos, jugador_pos, rango_percepcion, laberinto):
    for enemigo in posiciones_enemigos:
        enemigo_x, enemigo_y = enemigo["pos_actual"]
        dist_x = jugador_pos[0] - enemigo_x
        dist_y = jugador_pos[1] - enemigo_y

        # Calcular la distancia euclidiana
        distancia = (dist_x ** 2 + dist_y ** 2) ** 0.5

        # Si el enemigo está dentro del rango de percepción, moverlo hacia el jugador
        if distancia < rango_percepcion:
            # Decidir la dirección a mover
            if abs(dist_x) > abs(dist_y):  # Mover en la dirección horizontal primero
                if dist_x > 0 and laberinto[enemigo_x + 1][enemigo_y] == 0:  # Abajo
                    enemigo_x += 1
                elif dist_x < 0 and laberinto[enemigo_x - 1][enemigo_y] == 0:  # Arriba
                    enemigo_x -= 1
            else:  # Mover en la dirección vertical primero
                if dist_y > 0 and laberinto[enemigo_x][enemigo_y + 1] == 0:  # Derecha
                    enemigo_y += 1
                elif dist_y < 0 and laberinto[enemigo_x][enemigo_y - 1] == 0:  # Izquierda
                    enemigo_y -= 1

            enemigo["pos_actual"] = (enemigo_x, enemigo_y)

def mostrar_menu_ganador(pantalla, texto, fuente, score, tiempo_transcurrido):
    BLANCO = (255, 255, 255)
    AMARILLO = (255, 183, 3)
    AZUL = (2, 48, 71)
    SKYBLUE = (33, 158, 188)
    NEGRO = (0, 0, 0)

    pantalla.fill(NEGRO)
    texto_ganador = fuente.render(f"¡{texto}!", True, AMARILLO)
    pantalla.blit(texto_ganador, (300, 150)) 
    texto_puntaje = fuente.render(f"Puntaje: {score}", True, BLANCO)
    pantalla.blit(texto_puntaje, (300, 200))  

    minutos = int(tiempo_transcurrido // 60)
    segundos = int(tiempo_transcurrido % 60)
    texto_tiempo = fuente.render(f"Tiempo: {minutos:02}:{segundos:02}", True, BLANCO)
    pantalla.blit(texto_tiempo, (350, 600))

    opciones = ["Reiniciar", "Menú", "Salir"]
    seleccion = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    return opciones[seleccion].lower().replace(" ", "_")

        for i, opcion in enumerate(opciones):
            color = AZUL if i == seleccion else SKYBLUE
            boton_rect = pygame.Rect(350, 300 + i * 100, 200, 50)
            pygame.draw.rect(pantalla, color, boton_rect)
            texto_opcion = fuente.render(opcion, True, BLANCO)
            pantalla.blit(texto_opcion, (boton_rect.x + 50, boton_rect.y + 10))

        pygame.display.flip()

def ejecutar_laberinto(nivel, enemigos, recompensas, mejoras, pared):
    pygame.init()
    pygame.mixer.init()

    musica_niveles = {
        "Fácil": './Sonidos/fon_facil.mp3',
        "Medio": './Sonidos/fondo_medio.mp3',
        "Difícil": './Sonidos/fondo_dificil.mp3'
    }
    
    # Cargar y reproducir la música si no está sonando
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(musica_niveles[nivel])
        pygame.mixer.music.play(-1)  # Reproduce en bucle

    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    ROJO = (255, 0, 0)
    AZUL = (0, 0, 255)

    fuente = pygame.font.Font(None, 30)
    fuenteGanador = pygame.font.Font(None, 45)
    TAMANO_CELDA = 30

    ANCHO, ALTO = 925, 650
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Juego del Laberinto")

    jugador_x, jugador_y = 1, 1
    meta_x, meta_y = len(laberinto[0]) - 2, len(laberinto) - 2

    img_clock = pygame.image.load('./img/clock.png')
    img_clock = pygame.transform.scale(img_clock, (40, 40))
    img_recompensas = pygame.image.load('./img/puntaje.png')
    img_recompensas = pygame.transform.scale(img_recompensas, (40, 40))
    img_moneda = pygame.image.load('./img/moneda.png')
    img_moneda = pygame.transform.scale(img_moneda, (28, 28))
    img_meta = pygame.image.load('./img/meta_castillo.png')
    img_meta = pygame.transform.scale(img_meta, (50, 60))

    img_mejora = pygame.image.load('./img/velocidad.png')
    img_mejora = pygame.transform.scale(img_mejora, (28, 28))
    img_enemigo = pygame.image.load('./img/minitauro.png')
    img_enemigo = pygame.transform.scale(img_enemigo, (28, 28))
    img_jugador = pygame.image.load('./img/player.png')
    img_jugador = pygame.transform.scale(img_jugador, (28, 28))

    img_level = pygame.image.load('./img/level.png')
    img_level = pygame.transform.scale(img_level, (35, 30))

    posiciones_monedas = colocar_monedas(laberinto, recompensas)
    posiciones_enemigos = colocar_enemigos(laberinto, enemigos)
    posiciones_mejoras = colocar_mejoras(laberinto, mejoras)

    score = 0
    tiempo_inicio = time.time()
    velocidad_actual = VELOCIDAD_NORMAL
    tiempo_mejora = 0

    # Cargar la música de derrota
    sonido_derrota = pygame.mixer.Sound(SONIDO_DERROTA)
    sonido_moneda = pygame.mixer.Sound(SONIDO_MONEDA)

    ejecutando = True
    while ejecutando:
        pantalla.fill(NEGRO)  # Limpiar la pantalla al inicio de cada iteración
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                for paso in range(velocidad_actual):
                    if evento.key == pygame.K_LEFT and laberinto[jugador_y][jugador_x - 1] == 0:
                        jugador_x -= 1
                    elif evento.key == pygame.K_RIGHT and laberinto[jugador_y][jugador_x + 1] == 0:
                        jugador_x += 1
                    elif evento.key == pygame.K_UP and laberinto[jugador_y - 1][jugador_x] == 0:
                        jugador_y -= 1
                    elif evento.key == pygame.K_DOWN and laberinto[jugador_y + 1][jugador_x] == 0:
                        jugador_y += 1


    # Verificar si el jugador ha sido alcanzado por un enemigo
        for enemigo in posiciones_enemigos:
            if enemigo["pos_actual"] == (jugador_y, jugador_x):
                # Reproducir sonido de derrota sin bloquear
                sonido_derrota.play()
                # Esperar unos milisegundos para que se reproduzca el sonido sin que el juego se trabe
                pygame.time.delay(500)
                tiempo_transcurrido = time.time() - tiempo_inicio
                texto = "Perdiste. Fin del juego"
                opcion = mostrar_menu_ganador(pantalla, texto, fuenteGanador, score, tiempo_transcurrido)
                return opcion

        # Mover enemigos hacia el jugador
        mover_enemigos(posiciones_enemigos, (jugador_y, jugador_x), RANGO_PERCEPCION, laberinto)

        if jugador_x == meta_x and jugador_y == meta_y:
            tiempo_transcurrido = time.time() - tiempo_inicio
            texto = "Ganaste"
            opcion = mostrar_menu_ganador(pantalla, texto, fuenteGanador, score, tiempo_transcurrido)
            return opcion

        monedas_restantes = []
        for (moneda_x, moneda_y) in posiciones_monedas:
            if jugador_x == moneda_y and jugador_y == moneda_x:
                pygame.mixer.Sound("./Sonidos/moneda.mp3")
                score += 1
                sonido_moneda.play()
            else:
                monedas_restantes.append((moneda_x, moneda_y))
        posiciones_monedas = monedas_restantes

        mejoras_restantes = []
        for (mejora_x, mejora_y) in posiciones_mejoras:
            if jugador_x == mejora_y and jugador_y == mejora_x:
                velocidad_actual = VELOCIDAD_MEJORADA
                tiempo_mejora = time.time()
            else:
                mejoras_restantes.append((mejora_x, mejora_y))
        posiciones_mejoras = mejoras_restantes

        if tiempo_mejora != 0 and time.time() - tiempo_mejora >= DURACION_MEJORA:
            velocidad_actual = VELOCIDAD_NORMAL
            tiempo_mejora = 0

        for fila in range(len(laberinto)):
            for col in range(len(laberinto[fila])):
                if laberinto[fila][col] == 1:
                    pantalla.blit(pared, (col * TAMANO_CELDA, fila * TAMANO_CELDA))
                elif laberinto[fila][col] == 0:
                    pygame.draw.rect(pantalla, BLANCO, (col * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

        for (x, y) in posiciones_monedas:
            pantalla.blit(img_moneda, (y * TAMANO_CELDA, x * TAMANO_CELDA))

        # Dibuja las mejoras
        for (x, y) in posiciones_mejoras:
            pantalla.blit(img_mejora, (y * TAMANO_CELDA, x * TAMANO_CELDA))


        # Dibuja los enemigos
        for enemigo in posiciones_enemigos:
            enemigo_x, enemigo_y = enemigo["pos_actual"]
            pantalla.blit(img_enemigo, (enemigo_y * TAMANO_CELDA, enemigo_x * TAMANO_CELDA))

        pantalla.blit(img_jugador, (jugador_x * TAMANO_CELDA, jugador_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
        pantalla.blit(img_meta, (meta_x * TAMANO_CELDA, meta_y * TAMANO_CELDA))

        tiempo_transcurrido = time.time() - tiempo_inicio
        minutos = int(tiempo_transcurrido // 60)
        segundos = int(tiempo_transcurrido % 60)
        texto_tiempo = fuente.render(f"{minutos:02}:{segundos:02}", True, (255, 255, 0))

        pantalla.blit(texto_tiempo, (50, ALTO - 50))
        pantalla.blit(img_clock, (10, ALTO - 60))
        pantalla.blit(img_level, (130, ALTO - 60))
        pantalla.blit(fuente.render(f"{nivel}", True, BLANCO), (180, ALTO - 50))
        pantalla.blit(img_recompensas, (300, ALTO - 60))
        pantalla.blit(fuente.render(f"{score}", True, BLANCO), (350, ALTO - 50))
        pantalla.blit(img_mejora, (420, ALTO - 60))
        pantalla.blit(fuente.render(f"{mejoras}", True, BLANCO), (460, ALTO - 50))
        pantalla.blit(img_enemigo, (510, ALTO - 60))
        pantalla.blit(fuente.render(f"{enemigos}", True, BLANCO), (550, ALTO - 50))

        pygame.display.flip()

# Definir la matriz del laberinto
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]

]

# Llamar a la función para ejecutar el juego
if __name__ == "__main__":
    ejecutar_laberinto()
