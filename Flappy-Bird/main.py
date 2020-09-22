# Importing Libraries
import pygame
import helper.game_variables as gv
import helper.game_functions as gf
import sys


def main():
    # INITIALIZING

    screen = gf.initalize_game()
    clock = pygame.time.Clock()
    game_images = gf.load_images()
    game_sounds = gf.load_sounds()
    game_rect = gf.load_rect()
    large_font_ = gf.get_font('04B_19', 40)
    small_font_ = gf.get_font('04B_19', 20)

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, gv.PIPE_SPAWN_TIME)
    pipe_list = []
    
    BIRD_IMAGES = [game_images['redbird-downflap'], game_images['redbird-midflap'], game_images['redbird-upflap']]
    bird_index_ = 0
    BIRD_RECT = game_rect['redbird-midflap']
    bird_movement_ = 0
    BIRDFLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRDFLAP, 200)

    game_active_ = True
    BASE_X_POS = 0
    score_, high_score_ = 0, 0
    

    while True:

        # HANDLING EVENTS
        for event in pygame.event.get():
            
            # Handling Exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handling Key Presses
            if event.type == pygame.KEYDOWN:

                # Handling "Escape" and "Q"
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                # Handling "Space Bar" and "Mouse Click"
                if event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                    bird_movement_ = 0
                    bird_movement_ -= gv.BIRD_JUMP
                    game_sounds['wing_flap'].play()

                # Handling "R" for Restart
                if event.key == pygame.K_r:
                    game_active_ = True
                    score_ = 0
                    pipe_list.clear()
                    BIRD_RECT.center = (50, 226)
                    bird_movement_ = 0
                
                # Handling "P" for Pause
                # if event.key == pygame.K_p:
                #     pipe_list = gf.pause_game(pipe_list)

        
            # Handling USEREVENTS
            if event.type == SPAWNPIPE:
                pipe_list.extend(gf.create_pipe(game_images['pipe-red']))

            if event.type == BIRDFLAP:
                if bird_index_ < 2:
                    bird_index_ += 1
                else:
                    bird_index_ = 0

        # ADDING ELEMENTS TO SCREEN
        
        # Adding Background
        screen.blit(game_images['background-night'], (0,0))

        if game_active_:

            # Adding Bird
            bird_image = BIRD_IMAGES[bird_index_]
            rotated_bird = gf.rotate_bird(bird_image, bird_movement_)
            screen.blit(rotated_bird, BIRD_RECT)
            bird_movement_ += gv.GRAVITY
            BIRD_RECT.centery += bird_movement_

            # Adding Pipe
            pipe_list = gf.move_pipe(pipe_list)
            gf.draw_pipe(screen, game_images['pipe-red'], pipe_list)

            # Adding Score
            score_ += gv.SCORE_INCREASE
            gf.game_score_display(screen, score_, large_font_)
            
            # COLLISION DETECTION
            game_active_ = gf.check_collision(BIRD_RECT, pipe_list, game_sounds['collision'])

        else:           
            screen.blit(game_images['gameover'], (45, 230))
            if score_ > high_score_:
                high_score_ = score_
            gf.final_score_display(screen, score_, high_score_, large_font_, small_font_)

        # Adding Base
        gf.draw_base(screen, game_images['base'], BASE_X_POS)
        BASE_X_POS -= 1
        if BASE_X_POS <= -gv.SCREEN_WIDTH:
            BASE_X_POS = 0

        pygame.display.update()
        clock.tick(gv.FPS)


if __name__ == '__main__':
    main()

