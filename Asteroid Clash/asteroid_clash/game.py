# Importing Libraries
import pygame
from utils import load_sprite, get_random_position, print_text
from models import Spaceship, Asteroid

# Defining SpaceRocks Class
class AsteroidClash:

    MIN_ASTEROID_DISTANCE = 250

    # Initializing
    def __init__(self) -> None:
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite(name='space', with_alpha=False)
        self.bullets = []
        self.asteroids = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE
                    ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ''

    
    # Defining Main Loop for the game
    def main_loop(self) -> None:
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
    
    # Initializing Pygame
    def _init_pygame(self) -> None:
        pygame.init()
        pygame.display.set_caption('Asteroid Clash')
    
    # Defining function for handling input
    def _handle_input(self) -> None:
        for event in pygame.event.get():

            # Exiting the game
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                quit()
            elif (
                self.spaceship and 
                event.type == pygame.KEYDOWN and
                event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        # Handling Inputs
        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            elif is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()


    # Defining function for getting all game objects
    def _get_game_objects(self):
        game_objects = [*self.asteroids]
        game_objects = [*self.asteroids, *self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    # Defining function for processing game logic
    def _process_game_logic(self) -> None:
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = 'YOU LOST!'
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
        
        if not self.asteroids and self.spaceship:
            self.message = 'YOU WON!'


    # Defining function for drawing elements on screen
    def _draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        if self.message:
            print_text(self.screen, self.message, self.font)
        pygame.display.flip()
        self.clock.tick(60)
