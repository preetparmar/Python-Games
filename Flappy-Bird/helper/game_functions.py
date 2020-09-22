# Documentation
__doc__ = 'This file contains all the functions which will be required for the game'
__version__ = 1.0

# Importing Libraries
import pygame
import helper.game_variables as gv
from random import choice
import sys


def initalize_game():
    pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
    pygame.mixer.init()
    pygame.init()
    screen = pygame.display.set_mode((gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    pygame.display.set_icon(pygame.image.load('Assets/Images/icon.ico'))
    return screen

def load_image(file_name:str):
    """
    Loads Images and returns a surface object
    """
    image_file_ = f'Assets/Images/{file_name}.png'
    return pygame.image.load(image_file_).convert_alpha()

def load_images():
    """
    Returns a dictionary of Images which will be useful in the game
    """
    return {
            'background-day': load_image('background-day'),
            'background-night': load_image('background-night'),
            'base': load_image('base'),
            'bluebird-downflap': load_image('bluebird-downflap'),
            'bluebird-midflap': load_image('bluebird-midflap'),
            'bluebird-upflap': load_image('bluebird-upflap'),
            'redbird-downflap': load_image('redbird-downflap'),
            'redbird-midflap': load_image('redbird-midflap'),
            'redbird-upflap': load_image('redbird-upflap'),
            'yellowbird-downflap': load_image('yellowbird-downflap'),
            'yellowbird-midflap': load_image('yellowbird-midflap'),
            'yellowbird-upflap': load_image('yellowbird-upflap'),
            'gameover': load_image('gameover'),
            'pipe-green': load_image('pipe-green'),
            'pipe-red': load_image('pipe-red'),
            # 'bottom-pipe-green': load_image('pipe-green'),
            # 'top-pipe-green': pygame.transform.flip(load_image('pipe-green'), False, True),
            # 'bottom-pipe-red': load_image('pipe-red'),
            # 'top-pipe-red': pygame.transform.flip(load_image('pipe-red'), False, True)
        }

def draw_base(screen, image, x_pos):
    """ Draws Base for the Game """
    screen.blit(image, (x_pos, gv.BASE_TOP))
    screen.blit(image, (x_pos+gv.SCREEN_WIDTH, gv.BASE_TOP))

def load_rect():
    """ Returns a list Rectangles which will be useful in the game """
    game_images_ = load_images()
    return {
        'redbird-midflap': game_images_['redbird-midflap'].get_rect(center=(50, gv.SCREEN_HEIGHT/2)),
    }

def draw_pipe(screen:object, pipe_img:object, pipes:list):
    """ Draws Pipe """
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_img, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flip_pipe, pipe)

def create_pipe(pipe_img:object):
    pipe_x_pos_ = gv.SCREEN_WIDTH + 50
    pipe_height_ = choice(list(range(200, 350, 25)))
    top_pipe_rect = pipe_img.get_rect(midbottom=(pipe_x_pos_, pipe_height_-gv.PIPE_GAP))
    bottom_pipe_rect = pipe_img.get_rect(midtop=(pipe_x_pos_, pipe_height_))
    return top_pipe_rect, bottom_pipe_rect

def move_pipe(pipes:list):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def check_collision(bird_rect:object, pipes:list, collide_sound:object):
    """ Checks for collision with the Pipe and the Base """
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            collide_sound.play()
            return False
    if bird_rect.bottom >= gv.BASE_TOP:
        return False
    return True

def game_score_display(screen:object, score:int, font:object):
    display_font(screen, font, str(int(score)), (130, 20))

def get_font(font_name:str, font_size:int=40):
    return pygame.font.Font(f'Assets/Fonts/{font_name}.ttf', font_size)


def final_score_display(screen:object, score:int, high_score:int, large_font:object, small_font:object):
    score_text_ = f'Score: {int(score)}'
    high_score_ = str(int(high_score))
    restart_text_ = 'Press "R" To Restart'
    quit_text_ = 'Press "Q" to Quit'
    
    display_font(screen, large_font, score_text_, (60, 50))
    display_font(screen, large_font, 'High Score', (40, 120))
    display_font(screen, large_font, high_score_, (130, 165))
    display_font(screen, small_font, restart_text_, (40, 280))
    display_font(screen, small_font, quit_text_, (55, 310))
    
    
def rotate_bird(bird_surface:object, bird_movement):
    return pygame.transform.rotate(bird_surface, -bird_movement*3)

def animate_bird(bird_images:list, bird_index:int, bird_rect):
    new_bird_image = bird_images[bird_index]
    new_bird_rect = new_bird_image.get_rect(center=(50, bird_rect.centery))
    return new_bird_image, new_bird_rect


def display_font(screen:object, font:object, text:str, position:tuple=(0, 0), font_color:tuple=(255, 255, 255)):
    font_surface_ = font.render(text, True, font_color)
    screen.blit(font_surface_, position)

def load_sound(file_name:str, extension='wav') -> object:
    file_name_ = f'Assets/Sounds/{file_name}.{extension}'
    return pygame.mixer.Sound(file_name_)

def load_sounds():
    return {
        'wing_flap': load_sound('sfx_wing'),
        'collision': load_sound('sfx_hit'),
        'point': load_sound('sfx_point'),
    }

def pause_game(pipe_list:list):
    pause_status_ = True
    while pause_status_:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_status_ = False
                
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
    return pipe_list[-2:]
