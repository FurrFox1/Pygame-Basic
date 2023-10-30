import pygame
import sys
import random

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 128, 0)
AMARILLO = (255, 255, 0)
CELESTE = (0, 255, 255)
GRIS = (128, 128, 128)




# Ventana
ancho = 1000
largo = 1000
SIZE = (ancho, largo)
VENTANA = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Super Sonic Survival")

ejecutando = True

# Reloj
clock = pygame.time.Clock()

# Listas
lista_obstaculos = []
lista_anillos = []
lista_powerup = []

# Característica personaje
pos_x = 30
pos_y = 700
personaje_alto = 100
personaje_ancho = 100
personaje_original_alto = 100  # Altura original del personaje
personaje = pygame.image.load("./Imagenes/Fly.png").convert()
personaje = pygame.transform.scale(personaje, (personaje_ancho, personaje_alto))
personaje.set_colorkey([255, 255, 255])

Vida = 50
max_tiempo = 0
efecto_powerup = False
tiempo_inicial = 0  # Inicializa el tiempo al comienzo

# Velocidad
vel_x = 0
vel_y = 0
en_el_aire = False
gravedad = 1
agachado = False
