import pygame
from sys import exit
import os
from random import randint, choice


def verificar_tempo():
    tempo = int(pygame.time.get_ticks() / 1000) - tempo_inicial
    score_surface = fonte_teste.render(f'Score: {tempo}', False, (64, 64, 64))
    score_retangulo = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_retangulo)
    return tempo

def obstaculo_movimento(lista_obstaculos):
    if lista_obstaculos:
        for obstaculo_retangulo in lista_obstaculos:
            obstaculo_retangulo.x -= 5
            if obstaculo_retangulo.bottom == 300:
                screen.blit(snail_surface, obstaculo_retangulo)
            else:
                screen.blit(fly_surface, obstaculo_retangulo)
        lista_obstaculos = [ obstaculo for obstaculo in lista_obstaculos if obstaculo.x > -50]
        return lista_obstaculos
    else:
        return []


def colisao(jogador, lista_obstaculos):
    if lista_obstaculos:
        for obstaculo_retangulo in lista_obstaculos:
            if jogador.colliderect(obstaculo_retangulo):
                return False
            else: return True
    else:
        return True


def player_animacao():
    #criar a animação de andar qdo tiver no chão e pular qdo tiver no alto
   global player_surface, player_index
   if player_retangulo.bottom < 300:
        #pular
       player_surface = player_surf_pulo
   else:
        #andar
       player_index += 0.1
       if player_index >= len(player_walk_list):
           player_index = 0
       player_surface = player_walk_list[int(player_index)]

tempo_inicial = 0
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Corredor')
clock = pygame.time.Clock()
fonte_teste = pygame.font.Font(os.path.join('font', 'Pixeltype.ttf'), 50)
snail_pos_x = 600
score = 0




#superficie_teste = pygame.Surface((100,200))
#superficie_teste.fill('Red')
sky_surface = pygame.image.load(os.path.join('graphics', 'Sky.png')).convert()
ground_surface = pygame.image.load(os.path.join('graphics', 'ground.png')).convert()

text_surface = fonte_teste.render('Pixel-Jump', False, (111, 196, 169))
text_retangulo = text_surface.get_rect(center=(400, 90))
#score_surface = fonte_teste.render('Score', False, (64, 64, 64))
#score_retangulo = score_surface.get_rect(center=(400, 50))

#Obstáculos
obstaculos_rect_lista = []

#Caracol
snail_surf1 = pygame.image.load(os.path.join('graphics/snail', 'snail1.png')).convert_alpha()
snail_surf2 = pygame.image.load(os.path.join('graphics/snail', 'snail2.png')).convert_alpha()
# snail_retangulo = snail_surface.get_rect(midbottom=(600, sky_surface.get_height()))
snail_frames = [snail_surf1, snail_surf2]
snail_index = 0
snail_surface = snail_frames[snail_index]

#Mosca
fly_surf1 = pygame.image.load(os.path.join('graphics/Fly', 'Fly1.png')).convert_alpha()
fly_surf2 = pygame.image.load(os.path.join('graphics/Fly', 'Fly2.png')).convert_alpha()
fly_frames = [fly_surf1, fly_surf2]
fly_index = 0
fly_surface = fly_frames[fly_index]



player_surf_walk1 = pygame.image.load(os.path.join('graphics/player', 'player_walk_1.png')).convert_alpha()
player_surf_walk2 = pygame.image.load(os.path.join('graphics/player', 'player_walk_2.png')).convert_alpha()
player_walk_list = [player_surf_walk1, player_surf_walk2]
player_index = 0
player_surf_pulo = pygame.image.load(os.path.join('graphics/player', 'jump.png')).convert_alpha()
player_surface = player_walk_list[player_index]
player_retangulo = player_surface.get_rect(midbottom=(80, 300))  #Ou poderia ser sky_surface.get_height() que nem o chão
player_gravidade = 0

#Tela inicial de início de jogo
player_parado = pygame.image.load(os.path.join('graphics/Player', 'player_stand.png')).convert_alpha()
player_parado = pygame.transform.scale2x(player_parado)
player_parado_retangulo = player_parado.get_rect(center=(400, 200))

reiniciar_surface = fonte_teste.render('Pressione espaco para comecar!', False, (111, 196, 169))
reiniciar_retangulo = reiniciar_surface.get_rect(center=(400, 340))

jogo_ativo = False
timer_evento = pygame.USEREVENT + 1
pygame.time.set_timer(timer_evento, 1400)

timer_snail = pygame.USEREVENT + 2
pygame.time.set_timer(timer_snail, 500)

timer_fly = pygame.USEREVENT +3
pygame.time.set_timer(timer_fly, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if jogo_ativo:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_retangulo.collidepoint(event.pos) and player_retangulo.bottom >= 300:
                    player_gravidade = -20
            if event.type == timer_evento:
                if randint(0, 2):
                    obstaculos_rect_lista.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstaculos_rect_lista.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 210)))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_retangulo.bottom >= 300:
                    player_gravidade = - 20
            if event.type == timer_snail:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surface = snail_frames[snail_index]
            if event.type == timer_fly:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_frames[fly_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jogo_ativo = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reiniciar_retangulo.collidepoint(event.pos):
                    jogo_ativo = True
    if jogo_ativo:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, sky_surface.get_height())) #Ou (0, 300)
        #pygame.draw.rect(screen, '#c0e8ec', score_retangulo)
        #pygame.draw.rect(screen, '#c0e8ec', score_retangulo, 15)
        screen.blit(text_surface, (40, 25))
        #screen.blit(score_surface, score_retangulo)
        score = verificar_tempo()


        #Movimento do obstáculo
        obstaculos_rect_lista = obstaculo_movimento(obstaculos_rect_lista)
        #snail_retangulo.x -=5
        #if snail_retangulo.right < 0:
        #    snail_retangulo.left = 810
        #screen.blit(snail_surface, snail_retangulo)

        #Jogador
        player_gravidade += 1
        player_retangulo.y += player_gravidade
        if player_retangulo.bottom >= 300: player_retangulo.bottom = 300
        player_animacao()
        screen.blit(player_surface, player_retangulo)

        #Colisão
        jogo_ativo = colisao(player_retangulo, obstaculos_rect_lista)
        #if player_retangulo.colliderect(snail_retangulo):
        #    jogo_ativo = False
        #    snail_retangulo.x = 810

        #mouse_pos = pygame.mouse.get_pos()
        #if player_retangulo.collidepoint(mouse_pos):
        #    print('colisão')

    else:
        screen.fill((94, 129, 162))
        obstaculos_rect_lista.clear()
        player_retangulo.midbottom = (80, 300)
        screen.blit(player_parado, player_parado_retangulo)
        #pygame.draw.rect(screen, '#c0e8ec', reiniciar_retangulo, 100)
        screen.blit(text_surface, text_retangulo)
        if score == 0:
            screen.blit(reiniciar_surface, reiniciar_retangulo)
        else:
            score_surface = fonte_teste.render(f'Seus pontos: {score}',False, (111, 196, 169))
            score_retangulo = score_surface.get_rect(center=(400, 330))
            screen.blit(score_surface, score_retangulo)
        tempo_inicial = int(pygame.time.get_ticks() / 1000)


    #desenhar os elementos
    #atualizar as informações
    pygame.display.update()
    clock.tick(60)