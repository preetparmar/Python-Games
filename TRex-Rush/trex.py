import pygame
import helper.game_variables as gv
import helper.game_functions as gf
import sys
from random import randrange, choice

screen, clock = gf.initalize_game()
dino = gf.Dino(screen, 44, 47)
ground = gf.Ground(screen, -1*gv.gamespeed)
score = gf.GameFont(screen, font_size=gv.SCORE_FONT_SIZE)
game_sounds = gf.load_sounds()

clouds_group = pygame.sprite.Group()
cacti_group = pygame.sprite.Group()
ptera_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
# play_ = True

while not gv.game_quit:

    while not gv.game_over:
        for obstacle_ in obstacle_group:
            if pygame.sprite.collide_mask(dino, obstacle_):
                dino.isDead = True
                gv.game_over = True
                gv.game_quit = False
                game_sounds['die'].play()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gf.exit_game()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    gf.exit_game()
                
                if event.key == pygame.K_SPACE:
                    if not dino.isJumping:
                        dino.isJumping = True
                        dino.movement[1] = -1*dino.jumpSpeed
                        game_sounds['jump'].play()
                    
                if event.key == pygame.K_DOWN:
                    if not dino.isJumping:
                        dino.isDucking = True
                    else:
                        dino.movement[1] = 0
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.isDucking = False

        if len(obstacle_group) < 4:
            if len(cacti_group) == 0 or len(obstacle_group) == 0:
                cacti_group.add(gf.Cactus(screen, gv.gamespeed, 40, 40))
                obstacle_group.add(gf.Cactus(screen, gv.gamespeed, 40, 40))
            else:
                obstacle_len = len(obstacle_group)
                if obstacle_group.sprites()[obstacle_len-1].rect.right < gv.SCREEN_WIDTH*0.8 and randrange(0, 50) == 10:
                    object_ = choice([1, 2, 3])
                    if object_ == 1:
                        obstacle_group.add(gf.Ptera(screen, gv.gamespeed, 46, 40))
                    else:
                        obstacle_group.add(gf.Cactus(screen, gv.gamespeed, 40, 40))

        if len(clouds_group) < 5 and randrange(0, 300) == 10:
            cloud = gf.Cloud(screen)
            clouds_group.add(cloud)
        
        dino.update()
        ground.update()
        
        screen.fill(gv.BG_COLOR)
        ground.draw()
        for cloud_ in clouds_group:
            cloud_.update()
            cloud_.draw()
        for obstacle_ in obstacle_group:
            obstacle_.update()
            obstacle_.draw()
        dino.draw()
        score.draw(gv.score, font_color=gv.SCORE_COLOR, x=gv.SCORE_X, y=gv.SCORE_Y)
        pygame.display.update()
        clock.tick(gv.FPS)
        gv.counter += 1
        gv.score += 1 if gv.counter % 5 == 0 else 0
        if gv.score % 100 == 0 and gv.score != 0:
            if gv.play_counter == 4:
                game_sounds['checkPoint'].play()
                gv.play_counter = 0
            else:
                gv.play_counter += 1     

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gf.exit_game()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    gf.exit_game()
                
                if event.key == pygame.K_SPACE:
                    gv.game_over = False
                    dino.isDead = False
                    clouds_group.empty()
                    cacti_group.empty()
                    obstacle_group.empty()
                    gv.score = 0

    gv.highscore = gv.score if gv.highscore < gv.score else gv.highscore
    gf.game_over_screen(screen, gv.highscore)
    pygame.display.update()

pygame.quit()
sys.exit()
