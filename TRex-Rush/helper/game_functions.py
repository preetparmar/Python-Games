# Importing Libraries
import pygame
import helper.game_variables as gv
from random import randrange
import sys
from random import choice

def exit_game():
    pygame.quit()
    sys.exit()

def initalize_game():
    pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
    pygame.mixer.init()
    pygame.init()
    screen = pygame.display.set_mode((gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT))
    pygame.display.set_caption('T-Rex Rush')
    pygame.display.set_icon(pygame.image.load('Assets/Images/logo.png'))
    clock = pygame.time.Clock()
    intro_screen(screen, clock)
    return screen, clock

def load_image(file_name:str, size_x=-1, size_y=-1, colorkey=None):
    """
    Loads Images and returns a surface object
    """
    image_file_ = f'Assets/Images/{file_name}.png'
    image_ = pygame.image.load(image_file_).convert_alpha()
    image_rect_ = image_.get_rect()

    if size_x != -1 or size_y != -1:
        image_ = pygame.transform.scale(image_, (size_x, size_y))
    
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image_.get_at((0, 0))
        image_.set_colorkey(colorkey, pygame.RLEACCEL)
    return image_, image_rect_

def intro_screen(screen, clock):
    game_start_ = False
    
    temp_dino = Dino(screen, 44, 47)
    
    callout, callout_rect = load_image('written_by', 196, 45, -1)
    callout_rect.left = gv.SCREEN_WIDTH*0.05
    callout_rect.top = gv.SCREEN_HEIGHT*0.5

    temp_ground, temp_ground_rect = load_image('ground')
    temp_ground_rect.left = 0
    temp_ground_rect.bottom = gv.SCREEN_HEIGHT*0.99

    logo, logo_rect = load_image('start_logo', 500, 100, -1)
    logo_rect.centerx = gv.SCREEN_WIDTH*0.6
    logo_rect.centery = gv.SCREEN_HEIGHT*0.6

    while not game_start_:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        exit_game()
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    game_start_ = True
        
        screen.fill(gv.BG_COLOR)
        screen.blit(temp_ground, temp_ground_rect)
        screen.blit(logo, logo_rect)
        screen.blit(callout, callout_rect)
        temp_dino.draw()
        
        pygame.display.update()
        clock.tick(gv.FPS)

def game_over_screen(screen, highscore):

    game_over, game_over_rect = load_image('game_over')
    game_over_rect.centerx = gv.SCREEN_WIDTH/2
    game_over_rect.centery = gv.SCREEN_HEIGHT/2
    
    replay_font = GameFont(screen, font_size=10)
    replay_font.draw('Press SPACE to Restart', x=500, y=130, score=False)

    
    highscore_font = GameFont(screen, font_size=gv.SCORE_FONT_SIZE)
    highscore_font.draw(highscore, x=gv.HIGHSCORE_X, y=gv.HIGHSCORE_Y)
    highscore_font.draw('HI', x=gv.HIGHSCORE_X-45, y=gv.HIGHSCORE_Y, score=False)

    screen.blit(game_over, game_over_rect)

def load_sprite_sheet(file_name, n_x, n_y, scale_x=-1, scale_y=-1, colorkey=None):
    sheet_, sheet_rect_ = load_image(file_name)
    # sheet_rect_ = sheet_.get_rect()

    sprites = []

    size_x = sheet_rect_.width/n_x
    size_y = sheet_rect_.height/n_y

    for y in range(0, n_y):
        for x in range(0, n_x):
            rect_ = pygame.Rect((x*size_x, y*size_y, size_x, size_y))
            image_ = pygame.Surface(rect_.size).convert()
            image_.blit(sheet_, (0, 0), rect_)

            if scale_x != -1 or scale_y != -1:
                image_ = pygame.transform.scale(image_, (scale_x, scale_y))
            
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image_.get_at((0, 0))
                image_.set_colorkey(colorkey, pygame.RLEACCEL)

            sprites.append(image_)
        
    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect

def load_sound(file_name:str, extension='wav') -> object:
    file_name_ = f'Assets/Sounds/{file_name}.{extension}'
    return pygame.mixer.Sound(file_name_)

def load_sounds():
    return {
        'checkPoint': load_sound('checkPoint'),
        'die': load_sound('die'),
        'jump': load_sound('jump'),
    }

class Dino():

    def __init__(self, screen, size_x=1, size_y=1):
        self.screen = screen
        self.images, self.rect = load_sprite_sheet('dino', 5, 1, size_x, size_y, -1)
        self.images1, self.rect1 = load_sprite_sheet('dino_ducking', 2, 1, 59, size_y, -1)  # why scaling?
        self.rect.bottom = gv.BASE_LEVEL
        self.rect.left = gv.SCREEN_WIDTH/15
        self.index = 0
        self.image = self.images[0]
        self.counter = 0
        self.isJumping = False
        self.isBlinking = False
        self.isDucking = False
        self.isDead = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5
        self.score = 0

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width




    def draw(self):
        self.screen.blit(self.image, self.rect)

    def checkbounds(self):
        """ Checks if your Dino is still above the ground """
        if self.rect.bottom > gv.BASE_LEVEL:
            self.rect.bottom = gv.BASE_LEVEL
            self.isJumping = False

    def update(self):
        
        if self.isJumping:
            self.movement[1] = self.movement[1] + gv.GRAVITY
            self.index = 0
            self.image = self.images[self.index]
        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2  # Index = 0 or 1
                self.image = self.images1[(self.index)%2]
                self.rect.width = self.duck_pos_width    
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2  # Index = 2 or 3
                self.image = self.images[self.index]
                self.rect.width = self.stand_pos_width
        if self.isDead:
            self.index = 4
                
        self.rect = self.rect.move(self.movement)
        self.checkbounds()
        
        if not self.isDead and self.counter % 7 == 6:
            self.score += 1

        self.counter += 1


class Ground():

    def __init__(self, screen, speed=-5):
        self.screen = screen
        self.speed = speed
        self.image_1, self.rect_1 = load_image('ground')
        self.image_2, self.rect_2 = load_image('ground')
        self.rect_1.bottom = gv.SCREEN_HEIGHT
        self.rect_2.bottom = gv.SCREEN_HEIGHT
        self.rect_2.left = self.rect_1.right
        
        
    def draw(self):
        self.screen.blit(self.image_1, self.rect_1)
        self.screen.blit(self.image_2, self.rect_2)


    def update(self):
        self.rect_1.left += self.speed
        self.rect_2.left += self.speed

        if self.rect_1.right < 0:
            self.rect_1.left = self.rect_2.right
        
        if self.rect_2.right < 0:
            self.rect_2.left = self.rect_1.right


class Cactus(pygame.sprite.Sprite):
    
    def __init__(self, screen, speed=5, size_x=-1, size_y=-1):
        super().__init__()
        self.screen = screen
        self.imgages, self.rect = load_sprite_sheet('cacti-small', 3, 1, size_x, size_y, -1)
        self.rect.bottom = gv.BASE_LEVEL
        self.rect.left = gv.SCREEN_WIDTH + self.rect.width
        self.image = self.imgages[randrange(0, 3)]
        self.movement = [-1*speed, 0]
    
    def draw(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen       
        self.image, self.rect = load_image('cloud', int(90*30/42), 30, -1)
        self.rect.left = gv.SCREEN_WIDTH
        self.rect.top = randrange(gv.SCREEN_HEIGHT/5, gv.SCREEN_HEIGHT/2)
        self.speed = 1
        self.movement = [-1*self.speed, 0]
    
    def draw(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Ptera(pygame.sprite.Sprite):
    
    def __init__(self, screen, speed=5, size_x=-1, size_y=-1):
        super().__init__()
        self.screen = screen
        self.imgages, self.rect = load_sprite_sheet('ptera', 2, 1, size_x, size_y, -1)
        self.ptera_height = [gv.SCREEN_HEIGHT*0.82, gv.SCREEN_HEIGHT*0.73, gv.SCREEN_HEIGHT*0.60]
        self.rect.centery = self.ptera_height[randrange(0, 3)]
        self.rect.left = gv.SCREEN_WIDTH + self.rect.width
        self.image = self.imgages[0]
        self.movement = [-1*speed, 0]
        self.index = 0
        self.counter = 0
    
    def draw(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 2
        self.image = self.imgages[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter += 1
        if self.rect.right < 0:
            self.kill()


class GameFont():
    
    def __init__(self, screen, font_name='PressStart2P-Regular', font_size=20):
        font_path = f'Assets/Fonts/{font_name}.ttf'
        self.font = pygame.font.Font(font_path, font_size)
        self.screen = screen

    def draw(self, text, font_color=gv.SCORE_COLOR, alpha=10, x=0, y=0, score=True):
        if score:
            font_ = self.font.render(f'{text:>06}', True, font_color)
        else:
            font_ = self.font.render(f'{text}', True, font_color)
        self.screen.blit(font_, (x, y))
        # pygame.display.update()
