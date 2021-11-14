# Importing Library
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import Color
import random

# Function for loading sprites
def load_sprite(name: str, with_alpha: bool = True) -> object:
    path = f'assets/sprites/{name}.png'
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

# Function for wraping elements on the screen
def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

# Function to generate random position coordinates
def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )

# Function to generate random velocities
def get_random_velocity(min_speed: int, max_speed: int) -> object:
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

# Function to load sounds
def load_sound(name: str) -> object:
    path = f"assets/sounds/{name}.wav"
    return Sound(path)

# Function to print text on the screen
def print_text(surface, text, font, color=Color('tomato')):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)