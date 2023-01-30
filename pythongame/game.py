import pygame

image_path = '/data/data/com.andrei.myapp/files/app/'

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Andrey's game")
icon = pygame.image.load(image_path + "other/icon.png").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load(image_path + 'other/fon.png').convert().convert_alpha()
walk_left = [
    pygame.image.load(image_path + 'other/player_left/player1.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_left/player2.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_left/player3.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_left/player4.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_left/player5.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_left/player6.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_left/player7.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_left/player8.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_left/player9.png').convert_alpha(),
]
walk_right = [
    pygame.image.load(image_path + 'other/player_right/player1.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_right/player2.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_right/player3.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_right/player4.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_right/player5.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_right/player6.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_right/player7.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_right/player8.png').convert_alpha(),
    pygame.image.load(image_path + 'other/player_right/player9.png').convert_alpha(),





]

enemy = pygame.image.load(image_path + 'other/enemy.png').convert_alpha()
enemy_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speet = 5
player_x = 150
player_y = 355


is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound(image_path + 'font/bg.mp3')
bg_sound.play()

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2500)

laber = pygame.font.Font(image_path + 'font/Raleway-SemiBold.ttf', 40)
lose_label = laber.render('Вы проиграли!', False, (57, 128, 179))
restart_label = laber.render('Играь занаво!', False, (170, 108, 179))
restart_label_rest = restart_label.get_rect(topleft=(160, 260))

bullet_left = 5
bullet = pygame.image.load(image_path + 'other/free-icon-bullet-2218085.png').convert_alpha()
bullets = []

gameplay = True
running = True
while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 600, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 10

                if el.x < -10:
                    enemy_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speet
        elif keys[pygame.K_d] and player_x < 500:
            player_x += player_speet

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 8:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -600:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 620:
                    bullets.pop(i)

                if enemy_list_in_game:
                    for (index, enemy_el) in enumerate(enemy_list_in_game):
                        if el.colliderect(enemy_el):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (160, 160))
        screen.blit(restart_label, restart_label_rest)

        mouse = pygame.mouse.get_pos()
        if restart_label_rest.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            enemy_list_in_game.clear()
            bullets.clear()
            bullet_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(602, 355)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_w and bullet_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullet_left -= 1

    clock.tick(10)
