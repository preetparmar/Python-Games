""" Importing Libraries """
import pygame
from time import sleep
from random import randrange

""" Defining Variables """
# Defining Constant Variables
width, height = 500, 500
snake_thickness = 20
apple_thickness = 20
move_speed = 20
fps = 10
flottflott_font = 'fonts/flottflott.ttf'  # Font Path
fira_code_font = 'fonts/fira_code.ttf'  # Font Path

# Defining functional variables
clock = pygame.time.Clock()  # Pygame Clock Object
snake_img = pygame.image.load('images/snakehead.png')  # Loading the Snake Head PNG
apple_img = pygame.image.load('images/apple.png')  # Loading the Apple PNG
icon_img = pygame.image.load('images/icon.png')  # Loading the Icon PNG

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)


""" Defining Functions """

def display_message(message: str, font_color, font_name=flottflott_font, font_size=20, x_displacement=0, y_displacement=0):
    """ 
    Displays the "Message" on the center of the screen.

    Args:
        message (str): Message you want to display -> str
        font_color (Tuple): RGB Color Tuple for the font color
        font_name (str): File Path for the custom font
        font_size (int): Size of the font
        x_displacement (int): x distace from the center of the screen
        y_displacement (int): y distace from the center of the screen
    Yeilds:
        None
    """
    # font = pygame.font.SysFont(None, font_size)  # Initializing system font object
    font = pygame.font.Font(font_name, font_size)  # Initializing custom font object
    message_text = font.render(message, True, font_color)  # Rendering the text
    message_rect = message_text.get_rect()  # Getting the rectangle object from the text
    message_rect.center = width/2 + x_displacement, height/2 + y_displacement  # Centering the rectangle
    game_display.blit(message_text, message_rect)  # Displaying the Text Object and Text Rectangle Object

def snake(snake_list: list, snake_thickness: int):
    """
    Draws the snake.

    Args:
        snake_list (list): List of X and Y positions for Snake
        snake_thickness (int): Snake width and Snake Height
    Yeilds:
        None
    """
    # Handling Direction of the Image
    if direction == 'right':
        snake_head_img = pygame.transform.rotate(snake_img, 270)
    elif direction == 'left':
        snake_head_img = pygame.transform.rotate(snake_img, 90)
    elif direction == 'up':
        snake_head_img = snake_img
    elif direction == 'down':
        snake_head_img = pygame.transform.rotate(snake_img, 180)

    # Drawing Snake Head Image
    game_display.blit(snake_head_img, (snake_list[-1][0], snake_list[-1][1]))

    # Drawaing the body of the snake
    for x_y in snake_list[:-1]:
        game_display.fill(green, [x_y[0], x_y[1], snake_thickness, snake_thickness])

def start_game():
    """
    This function defines the main functionalities of the game.
    """

    """ Defining Variables """

    # Global Variables
    global direction, snake_length
    direction = 'right'
    snake_length = 1

    # Local Variables
    game_exit = False

    # Derived Local Variables
    snake_x, snake_y = width/2, height/2
    x_change, y_change = move_speed, 0
    snake_list = []
    apple_x, apple_y = randrange(0, width-apple_thickness), randrange(0, height-apple_thickness)
    while apple_x in [x[0] for x in snake_list] or apple_y in [y[1] for y in snake_list]:
        apple_x, apple_y = randrange(0, width-apple_thickness), randrange(0, height-apple_thickness)

    # Game Loop
    while not game_exit:

        """ Boundary Restriction """
        x_boundary = snake_x + snake_thickness > width or snake_x < 0  # X boundary
        y_boundary = snake_y + snake_thickness > height or snake_y < 0  # Y boundary
        if  x_boundary or y_boundary:
            game_over_function()

        """ Apple Crossing """
        x_crossing = snake_x + snake_thickness > apple_x and snake_x <= apple_x + apple_thickness
        y_crossing = snake_y + snake_thickness > apple_y and snake_y <= apple_y + apple_thickness
        if x_crossing and y_crossing:
            apple_x, apple_y = randrange(0, width-apple_thickness), randrange(0, height-apple_thickness)
            while apple_x in [x[0] for x in snake_list] or apple_y in [y[1] for y in snake_list]:
                apple_x, apple_y = randrange(0, width-apple_thickness), randrange(0, height-apple_thickness)
            snake_length += 1

        """ Event Handlers """
        for event in pygame.event.get():

            # Quit Event
            if event.type == pygame.QUIT:
                display_message('Thank you for playing the game', font_color=red)
                sleep(2)
                game_exit = True

            # Movement Events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -move_speed
                    x_change = 0
                    direction = 'up'
            
                elif event.key == pygame.K_DOWN:
                    y_change = move_speed
                    x_change = 0
                    direction = 'down'

                elif event.key == pygame.K_RIGHT:
                    x_change = move_speed
                    y_change = 0
                    direction = 'right'

                elif event.key == pygame.K_LEFT:
                    x_change = -move_speed
                    y_change = 0
                    direction = 'left'
                
                # Pause Event
                elif event.key == pygame.K_p:
                    pause()

        # New Snake Location
        snake_head = []
        snake_x += x_change
        snake_y += y_change
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)

        # Adding in the length everytime
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Clashing into self restriction
        for each_element in snake_list[:-1]:
            if each_element == snake_head:
                game_over_function()
                

        """ Displaying items """
        game_display.fill(white)  # Background
        snake(snake_list, snake_thickness)  # Drawing Snake
        game_display.blit(apple_img, [apple_x, apple_y])  # Drawing Apple Image
        display_message('Score: %s' % (snake_length-1), font_color=black, font_size=20,
                        x_displacement=-width/2 + 35, y_displacement=-height/2 + 20)
        pygame.display.update()  # Updating Display

        # Defining Frames per Second
        clock.tick(fps)

def intro_screen():
    """
    This function defines the starting screen
    """

    play = False
    game_display.fill(white)
    display_message(message='Welcome to My Snake Game!', font_color=green, font_size=45, y_displacement=-20)
    display_message(message='Press "S" to Start, "P" to Pause or "Q" to Quit', font_color=black, 
                    font_name=fira_code_font, font_size=15, y_displacement=15)
    pygame.display.update()
    while not play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    thank_you()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    play = True
                    break
                if event.key == pygame.K_q:
                    thank_you()
            clock.tick(5)

def game_over_function():
    """
    This function handles the Game Over Event
    """
    game_over = False
    game_display.fill(white)
    display_message('GAME OVER!!!', font_color=red, font_size=50)
    display_message('Press "R" to restart or "Q" to Quit', font_color=black, 
                    y_displacement=50, font_name=fira_code_font, font_size=20)
    display_message('Score: %s' % (snake_length-1), font_color=black, font_size=40, y_displacement=width/2 - 40)
    pygame.display.update()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                thank_you()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    thank_you()
                if event.key == pygame.K_r:
                    start_game()

def thank_you():
    """
    Function to display Thank You message
    """
    game_display.fill(white)
    display_message('Thank you for playing the game!', font_color=black, font_size=40)
    display_message('<3', font_color=red, font_size=50, font_name=fira_code_font, y_displacement=50)
    pygame.display.update()
    sleep(1)
    quit()

def pause():
    """
    Function to Pause the game
    """
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_function()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pause = False
                    break
                if event.key == pygame.K_q:
                    game_over_function()
            game_display.fill(white)
            display_message('PAUSED', font_color=red, font_size=40)
            display_message('Press "C" to Continue or "Q" to Quit', font_color=black, 
                            font_name=fira_code_font, font_size=15, y_displacement=50)
            pygame.display.update()
            clock.tick(5)

def main():
    """
    Main function for the Game
    """
    global game_display

    # Initialising PyGame
    pygame.init()

    # Initialising game window
    game_display = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake Game')
    pygame.display.set_icon(icon_img)  # Setting the icon

    # Starting Game
    intro_screen()
    start_game()
    quit()

if __name__ == '__main__':
    main()
