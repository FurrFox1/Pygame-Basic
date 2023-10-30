import pygame
import sys
import random
from config import *
from funciones import *
pygame.init()

# Sonido
anillo_sonido = pygame.mixer.Sound("./Sonidos/ring.mp3")
meteoro_sonido = pygame.mixer.Sound("./Sonidos/damage.mp3")
powerup_sonido = pygame.mixer.Sound("./Sonidos/powerup.mp3")
salto_sonido = pygame.mixer.Sound("./Sonidos/jump.mp3")


for i in range(5):
    crear_obstaculo()

for i in range(5):
    crear_anillos()

for i in range(1):
    crear_powerup()


# Fondo y escalamiento
fondo = pygame.image.load("./Imagenes/fondo.png")
fondo = pygame.transform.scale(fondo, SIZE)
fondo_x = 0
fondo_velocidad = 20

# Texto Vida
fuente = pygame.font.SysFont(None, 48)
texto = fuente.render(f"Salud: {Vida}", True, BLANCO)
rect_texto = texto.get_rect()
rect_texto.midtop = (80, 30)

# Evento personalizados
EVENT_NUEVO_ANILLO = pygame.USEREVENT + 1
pygame.time.set_timer(EVENT_NUEVO_ANILLO, 5000)

EVENT_NUEVO_OBSTACULO = pygame.USEREVENT + 2
pygame.time.set_timer(EVENT_NUEVO_OBSTACULO, 2000)

EVENT_NUEVO_POWERUP = pygame.USEREVENT + 1
pygame.time.set_timer(EVENT_NUEVO_POWERUP, 30000)

# Cronometro
tiempo_inicial = pygame.time.get_ticks()
fuente_cronometro = pygame.font.SysFont(None, 48)

VENTANA.fill(NEGRO)
fuente_grande = pygame.font.Font(None, 64)
fuente_pequeña = pygame.font.Font(None, 36)

# Texto "Super Sonic Survival"
texto_super_sonic = fuente_grande.render(
    "Super Sonic Survival", True, AMARILLO)
rect_texto_super_sonic = texto_super_sonic.get_rect()
rect_texto_super_sonic.center = (ancho // 2, largo // 2 - 50)

VENTANA.blit(texto_super_sonic, rect_texto_super_sonic)

# Texto "Presiona una tecla para comenzar"
texto_comenzar = fuente_pequeña.render(
    "Presiona 'C' para comenzar", True, BLANCO)
rect_texto_comenzar = texto_comenzar.get_rect()
rect_texto_comenzar.center = (ancho // 2, largo // 2 + 50)
VENTANA.blit(texto_comenzar, rect_texto_comenzar)

ventana_inicial = True
while ventana_inicial:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ventana_inicial = False
            ejecutando = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            ventana_inicial = False
            tiempo_inicial = pygame.time.get_ticks()  # Inicializa el tiempo al comenzar

    VENTANA.fill((0, 0, 0))  # Fondo negro
    VENTANA.blit(texto_super_sonic, rect_texto_super_sonic)
    VENTANA.blit(texto_comenzar, rect_texto_comenzar)
    pygame.display.flip()


pygame.mixer.music.load("./Sonidos/music.mp3")

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
reproduciendo_musica = True

while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

        if event.type == EVENT_NUEVO_ANILLO:
            crear_anillos()

        if event.type == EVENT_NUEVO_OBSTACULO:
            crear_obstaculo()

        if event.type == EVENT_NUEVO_POWERUP:
            crear_powerup()

    vel_x = 0
    # CONTROLES
    botones = pygame.key.get_pressed()
    if botones[pygame.K_LEFT]:
        vel_x = -7
    if botones[pygame.K_RIGHT]:
        vel_x = 7
    if botones[pygame.K_UP] and not en_el_aire:
        salto_sonido.play()
        vel_y = -20
        en_el_aire = True
    if botones[pygame.K_DOWN]:
        personaje_alto = 50
        agachado = True
        pos_y = 750
    elif en_el_aire == False:
        personaje_alto = personaje_original_alto
        pos_y = 700
        agachado = False

    if botones[pygame.K_m]:
        if reproduciendo_musica:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause
        reproduciendo_musica = not reproduciendo_musica

    # Pausa juego
    if botones[pygame.K_p]:
        if reproduciendo_musica:
            pygame.mixer.music.pause()
        mostrar_pausa()
        pausa()
        if reproduciendo_musica:
            quitar_pausa()
            pygame.mixer.music.unpause()

    # Gravedad
    if en_el_aire:
        pos_y += vel_y
        vel_y += gravedad

        if pos_y >= 700:
            en_el_aire = False
            pos_y = 700

    VENTANA.fill((255, 255, 255))

    # Dibujar fondo
    VENTANA.blit(fondo, (fondo_x, 0))
    VENTANA.blit(fondo, (fondo_x + fondo.get_width(), 0))
    fondo_x -= fondo_velocidad
    if fondo_x <= -fondo.get_width():
        fondo_x = 0

    # Dibujar obstáculos (Meteoros)
    for obstaculo in lista_obstaculos:
        x, y, ancho_obstaculo, alto_obstaculo, velocidad_obstaculo, meteoro = obstaculo
        VENTANA.blit(meteoro, (x, y))
        # Actualiza la posición según la velocidad individual
        x -= velocidad_obstaculo
        if x + ancho_obstaculo < 0:
            x = ancho + random.randint(0, 200)
            y = random.randint(450, largo - 200)
            # Asignamos una nueva velocidad aleatoria
            velocidad_obstaculo = random.randint(2, 8)
        obstaculo[0] = x
        obstaculo[1] = y
        obstaculo[4] = velocidad_obstaculo

    # Dibujar anillos
    for objeto in lista_anillos:
        x, y, ancho_anillo, alto_anillo, velocidad_anillo, anillo = objeto
        VENTANA.blit(anillo, (x, y))
        # Actualiza la posición según la velocidad individual
        x -= velocidad_anillo
        if x + ancho_anillo < 0:
            x = ancho + random.randint(0, 200)
            y = random.randint(450, largo - 200)
            # Asigna una nueva velocidad aleatoria
            velocidad_anillo = random.randint(2, 8)
        lista_anillos[lista_anillos.index(objeto)] = [
            x, y, ancho_anillo, alto_anillo, velocidad_anillo, anillo]

    # Dibujar Powerup

    for power in lista_powerup:
        x, y, ancho_powerup, alto_powerup, velocidad_powerup, powerup = power
        VENTANA.blit(powerup, (x, y))
        # Actualiza la posición según la velocidad individual
        x -= velocidad_powerup
        if x + ancho_powerup < 0:
            # Elimina el power-up que ha salido de la pantalla
            lista_powerup.remove(power)
        power[0] = x
        power[1] = y
        power[4] = velocidad_powerup

    # Limitar la posición horizontal del personaje para que no sobresalga de la ventana
    if pos_x + vel_x < 0:
        pos_x = 0
    elif pos_x + vel_x + personaje_ancho > ancho:
        pos_x = ancho - personaje_ancho
    else:
        pos_x += vel_x

    # Colision

    personaje_rect = pygame.Rect(pos_x, pos_y, personaje_ancho, personaje_alto)
    if detectar_colision(personaje_rect, lista_obstaculos):
        Vida -= 1
        texto = fuente.render(f"Salud: {Vida}", True, BLANCO)
        rect_texto = texto.get_rect()
        rect_texto.midtop = (80, 30)
        meteoro_sonido.play()

    for anillo in lista_anillos:
        if detectar_colision(personaje_rect, [anillo]):
            lista_anillos.remove(anillo)
            Vida += 10
            texto = fuente.render(f"Salud: {Vida}", True, BLANCO)
            rect_texto = texto.get_rect()
            rect_texto.midtop = (80, 30)
            anillo_sonido.play()

    for powerup in lista_powerup:
        if detectar_colision(personaje_rect, [powerup]):
            lista_powerup.remove(powerup)
            lista_obstaculos.clear()
            powerup_sonido.play()
            for i in range(5):
                crear_obstaculo()
            efecto_powerup = True

    # Efecto PowerUp       
    if efecto_powerup:
        VENTANA.fill((255, 255, 255))  
        pygame.display.flip()
        pygame.time.delay(100)  
        efecto_powerup = False  

    # Calcula el tiempo en segundos
    tiempo_actual = pygame.time.get_ticks()
    segundos_transcurridos = (tiempo_actual - tiempo_inicial) // 1000

    # Texto para el cronómetro
    texto_cronometro = fuente_cronometro.render(f"Tiempo: {segundos_transcurridos} s", True, BLANCO)
    rect_texto_cronometro = texto_cronometro.get_rect()
    rect_texto_cronometro.topright = (ancho - 30, 30)

    # Dibuja el cronómetro en la pantalla
    VENTANA.blit(texto_cronometro, rect_texto_cronometro)

    if Vida == 0:
        pygame.mixer.music.stop()
        game_over_texto = fuente.render("Game Over", True, ROJO)
        rect_game_over = game_over_texto.get_rect()
        rect_game_over.center = (ancho // 2, largo // 2)
        VENTANA.blit(game_over_texto, rect_game_over)

        # Muestra el tiempo transcurrido
        tiempo_transcurrido = segundos_transcurridos
        tiempo_transcurrido_texto = fuente_cronometro.render(
            f"Tiempo: {tiempo_transcurrido} s", True, BLANCO)
        rect_tiempo_transcurrido = tiempo_transcurrido_texto.get_rect()
        rect_tiempo_transcurrido.midtop = (
            ancho // 2, rect_game_over.bottom + 10)
        VENTANA.blit(tiempo_transcurrido_texto, rect_tiempo_transcurrido)

        # Actualiza el tiempo máximo si es necesario
        max_tiempo = max(max_tiempo, tiempo_transcurrido)

        # Muestra el mejor tiempo en la misma sesión
        mejor_tiempo_texto = fuente_cronometro.render(f"Mejor tiempo: {max_tiempo} s", True, BLANCO)
        rect_mejor_tiempo = mejor_tiempo_texto.get_rect()
        rect_mejor_tiempo.midtop = (
            ancho // 2, rect_tiempo_transcurrido.bottom + 10)
        VENTANA.blit(mejor_tiempo_texto, rect_mejor_tiempo)

        # Muestra la opción de volver a intentarlo
        reiniciar_texto = fuente.render("Presiona 'R' para jugar nuevamente", True, BLANCO)
        rect_reiniciar = reiniciar_texto.get_rect()
        rect_reiniciar.midtop = (ancho // 2, rect_mejor_tiempo.bottom + 20)
        VENTANA.blit(reiniciar_texto, rect_reiniciar)

        pygame.display.flip()

        # Bucle para esperar a que se presione 'R' para reiniciar
        reiniciar = False
        while not reiniciar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ejecutando = False
                    reiniciar = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.mixer.music.play()
                        reiniciar = True
                        Vida = 50
                        fuente = pygame.font.SysFont(None, 48)
                        texto = fuente.render(
                            f"Salud: {Vida}", True, BLANCO)
                        rect_texto = texto.get_rect()
                        rect_texto.midtop = (80, 30)
                        segundos_transcurridos = 0
                        tiempo_inicial = pygame.time.get_ticks()
                        lista_obstaculos.clear()
                        for i in range(5):
                            crear_obstaculo()
                        lista_anillos.clear()
                        for i in range(5):
                            crear_anillos()
                        lista_powerup.clear()
                        for i in range(1):
                            crear_powerup()
                        ejecutando = True

    # Cuadrado personaje
    pygame.draw.rect(VENTANA, ROJO, (pos_x, pos_y,personaje_ancho, personaje_alto), -1)

    # Actualizamos los elementos en pantalla
    VENTANA.blit(texto, rect_texto)
    VENTANA.blit(personaje, (pos_x, pos_y))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
