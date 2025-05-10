import pygame, sys
from pygame.math import Vector2 as vector

#НАСТРОЙКИ ГРИ
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6

#Кольора
BLACK = (0, 0, 0)
DARK_BROWN = (45, 30, 20)
GOLD = (212, 175, 55)
LIGHT_GOLD = (230, 210, 150)
RED_BROWN = (80, 30, 20)
PARCHMENT = (240, 230, 200)

#слої
Z_LAYERS = {
	'bg': 0,
	'clouds': 1,
	'bg tiles': 2,
	'path': 3,
	'bg details': 4,
	'main': 5,
	'water': 6,
	'fg': 7
}
