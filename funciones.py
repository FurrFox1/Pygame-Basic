import pygame
import sys
import random
from config import *

# Colisiones

def detectar_colision(rect, obstaculos):
    for obstaculo in obstaculos:
        obstaculo_rect = pygame.Rect(
            obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])
        if rect.colliderect(obstaculo_rect):
            return True
    return False


# Obstáculos

def crear_obstaculo():
    # Iniciar fuera de la pantalla a la derecha
    x = ancho + random.randint(0, 200)
    y = random.randint(450, largo - 200)
    ancho_obstaculo = 40
    alto_obstaculo = 40
    velocidad_obstaculo = random.randint(2, 8)
    meteoro = pygame.image.load("./Imagenes/Meteor.png").convert()
    meteoro = pygame.transform.scale(
        meteoro, (ancho_obstaculo, alto_obstaculo))
    meteoro.set_colorkey([255, 255, 255])
    lista_obstaculos.append(
        [x, y, ancho_obstaculo, alto_obstaculo, velocidad_obstaculo, meteoro])
    

# Anillos

def crear_anillos():
    # Iniciar fuera de la pantalla a la derecha
    x = ancho + random.randint(0, 200)
    y = random.randint(450, largo - 200)
    ancho_anillo = 40
    alto_anillo = 40
    velocidad_anillo = random.randint(2, 8)
    anillo = pygame.image.load("./Imagenes/anillo.png").convert()
    anillo = pygame.transform.scale(anillo, (ancho_anillo, alto_anillo))
    anillo.set_colorkey([255, 255, 255])
    lista_anillos.append(
        [x, y, ancho_anillo, alto_anillo, velocidad_anillo, anillo])

# Power Up

def crear_powerup():
    # Iniciar fuera de la pantalla a la derecha
    x = ancho + random.randint(0, 200)
    y = random.randint(450, largo - 200)
    ancho_powerup = 40
    alto_powerup = 40
    velocidad_powerup = random.randint(9, 15)
    powerup = pygame.image.load("./Imagenes/powerup.png").convert()
    powerup = pygame.transform.scale(powerup, (ancho_powerup, alto_powerup))
    powerup.set_colorkey([255, 255, 255])
    lista_powerup.append(
        [x, y, ancho_powerup, alto_powerup, velocidad_powerup, powerup])
    


# Funciones de pausado
def pausa():
    pausa = True
    while pausa:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pausa = False
                ejecutando = False
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_c:
                    pausa = False


def mostrar_pausa():
    fuente_pausa = pygame.font.SysFont(None, 64)
    texto_pausa = fuente_pausa.render("PAUSA", True, BLANCO)
    texto_continuar = fuente_pausa.render(
        "Presiona el botón C para reanudar", True, BLANCO)
    rect_texto_pausa = texto_pausa.get_rect()
    rect_texto_pausa.center = (ancho // 2, largo // 2)

    # Calcula las coordenadas para el segundo texto debajo del primero
    rect_texto_continuar = texto_continuar.get_rect()
    rect_texto_continuar.midtop = (ancho // 2, rect_texto_pausa.bottom + 10)

    fondo_negro = pygame.Surface((ancho, largo))
    fondo_negro.fill((0, 0, 0))
    fondo_negro.set_alpha(128)  # Opacidad

    VENTANA.blit(fondo_negro, (0, 0))  
    VENTANA.blit(texto_pausa, rect_texto_pausa)
    VENTANA.blit(texto_continuar, rect_texto_continuar)
    pygame.display.flip()


def quitar_pausa():
    VENTANA.fill((255, 255, 255))  # Restaurar el fondo blanco
    pygame.display.flip()
