import random

import pygame
from sys import exit
import os
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_surf_walk1 = pygame.image.load(os.path.join('graphics/player', 'player_walk_1.png')).convert_alpha()
        player_surf_walk2 = pygame.image.load(os.path.join('graphics/player', 'player_walk_2.png')).convert_alpha()
        self.player_walk_list = [player_surf_walk1, player_surf_walk2]
        self.player_index = 0
        self.player_surf_pulo = pygame.image.load(os.path.join('graphics/player', 'jump.png')).convert_alpha()
        self.image = self.player_walk_list[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100, 300))
        self.gravidade = 20

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravidade = -20
            self.jump_sound.play()

    def aplicar_gravidade(self):
        self.gravidade += 1
        self.rect.y += self.gravidade
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.aplicar_gravidade()
        self.player_animacao()

    def player_animacao(self):
        if self.rect.bottom < 300:
            # pular
            self.image = self.player_surf_pulo
        else:
            # andar
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk_list):
                self.player_index = 0
            self.image = self.player_walk_list[int(self.player_index)]


class Obstaculos (pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_surf1 = pygame.image.load(os.path.join('graphics/Fly', 'Fly1.png')).convert_alpha()
            fly_surf2 = pygame.image.load(os.path.join('graphics/Fly', 'Fly2.png')).convert_alpha()
            self.frames = [fly_surf1, fly_surf2]
            y_pos = 210
        else:
            snail_surf1 = pygame.image.load(os.path.join('graphics/snail', 'snail1.png')).convert_alpha()
            snail_surf2 = pygame.image.load(os.path.join('graphics/snail', 'snail2.png')).convert_alpha()
            self.frames = [snail_surf1, snail_surf2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))


    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]


    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def verificar_tempo():
    tempo = int(pygame.time.get_ticks() / 1000) - tempo_inicial
    score_surface = fonte_teste.render(f'Score: {tempo}', False, (64, 64, 64))
    score_retangulo = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_retangulo)
    return tempo

def colisao_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstaculo_group,False):
        obstaculo_group.empty()
        return False
    else:
        return True

tempo_inicial = 0
pygame.init()
screen = pygame.display.set_mode((800, 400))
#pygame.display.set_caption('Corredor')
clock = pygame.time.Clock()
fonte_teste = pygame.font.Font(os.path.join('font', 'Pixeltype.ttf'), 50)
snail_pos_x = 600
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops=-1)
jogo_ativo = False


#Fundo e chão
sky_surface = pygame.image.load(os.path.join('graphics', 'Sky.png')).convert()
ground_surface = pygame.image.load(os.path.join('graphics', 'ground.png')).convert()

#Tela inicial
player_parado = pygame.transform.scale2x(pygame.image.load(os.path.join('graphics/Player', 'player_stand.png')).convert_alpha())
player_parado_retangulo = player_parado.get_rect(center=(400, 400))
reiniciar_surface = fonte_teste.render('Pressione espaco para comecar!', False, (111, 196, 169))
reiniciar_retangulo = reiniciar_surface.get_rect(center=(400, 340))

#Texto
text_surface = fonte_teste.render('Pixel-Jump', False, (111, 196, 169))
text_retangulo = text_surface.get_rect(center=(400, 90))


timer_evento = pygame.USEREVENT + 1
pygame.time.set_timer(timer_evento, 1400)

timer_snail = pygame.USEREVENT + 2
pygame.time.set_timer(timer_snail, 500)

timer_fly = pygame.USEREVENT +3
pygame.time.set_timer(timer_fly, 200)


player = pygame.sprite.GroupSingle()
player.add(Player())

obstaculo_group = pygame.sprite.Group()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if jogo_ativo:
            if event.type == timer_evento:
                obstaculo_group.add(Obstaculos(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jogo_ativo = True
    if jogo_ativo:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, sky_surface.get_height())) #Ou (0, 300)
        screen.blit(text_surface, (40, 25))
        score = verificar_tempo()


        #Jogador
        player.draw(screen)
        player.update()
        obstaculo_group.draw(screen)
        obstaculo_group.update()

        #Colisão:
        jogo_ativo = colisao_sprite()

    else:
        screen.fill((94, 129, 162))
        player_parado_retangulo.midbottom = (400, 300)
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


    pygame.display.update()
    clock.tick(60)