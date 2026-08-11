import pygame
from pygame.locals import *
from sys import exit
import os
import random
from database import db, Pontuação

#=====INICIALIZAÇÂO++++
db.connect()
db.create_tables([Pontuação])
pygame.init()
pygame.mixer.init()
#=====VARIAVEIS++++++++
PONTOS = 0
RECORD_TOTAL = 0
RECORD_ATUAL = 0
try:
    record_atual = Pontuação.get()
    RECORD_TOTAL = record_atual.record
except Pontuação.DoesNotExist:
    record_atual = Pontuação.create(record=RECORD_TOTAL)

# Função para atualizar o record
def atualizar_record(PONTOS):
    global RECORD_TOTAL
    RECORD_TOTAL = PONTOS
    record_atual.record = RECORD_TOTAL
    record_atual.save()
ALTURA = 480
LARGURA = 640
BRANCO = (255,255,255)
PRETO = (0,0,0)
RELOGIO = pygame.time.Clock()
Diretorio_Principal = os.path.dirname(__file__)
Diretorio_Imagens = os.path.join(Diretorio_Principal ,'IMAGENS')
Diretorio_Som = os.path.join(Diretorio_Principal, 'Audios')
def database():
    pass
def Exibe_msg(msg,tamanho,cor):
    font = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = font.render(mensagem, True, cor)
    return texto_formatado
def Record(msg,tamanho,cor):
    font = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = font.render(mensagem,True, cor)
    return texto_formatado
#=====TELA+++++++
tela = pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption('DinoGame')
#=====VARIAVEL PYG+++++
velocidade_jogo = 10
sprite_sheet = pygame.image.load(os.path.join(Diretorio_Imagens, 'DINO.png'))
som_morte = pygame.mixer.Sound(os.path.join(Diretorio_Som, 'death_sound.wav'))
som_morte.set_volume(1)
colidiu = False
Som_pontuação = pygame.mixer.Sound(os.path.join(Diretorio_Som, 'score_sound.wav'))
Som_pontuação.set_volume(1)

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(Diretorio_Som, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.image_Dino = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0),(32,32))
            img = pygame.transform.scale(img, (32*3,32*3))
            self.image_Dino.append(img)
        self.index = 0
        self.image = self.image_Dino[self.index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.y_init = (ALTURA - 64 - 92//2)
        self.rect.center = (100, ALTURA - 64) 
        self.velocidade = 0
        self.gravidade = 0.8
        self.força_pulo = -12
        self.sit = False
    def agachar(self):
        if colidiu == True:
            pass
        else:
            self.sit = True
    def jump(self):
        if colidiu == True:
            pass
        else:
            self.velocidade = self.força_pulo
            self.som_pulo.play() 
    def update(self):
        if self.sit == True:
            self.gravidade = 25
            self.sit = False
        else:
            self.gravidade = 0.8
        self.velocidade += self.gravidade
        self.rect.y += self.velocidade
        if self.index > 2:
            self.index = 0
        if self.rect.y >= self.y_init:
            self.rect.y = self.y_init
        self.index += 0.25
        self.image = self.image_Dino[int(self.index)]

class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32,0),(32,32))
        self.image = pygame.transform.scale(self.image, (32*3,32*3))
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(50,200,50)
        self.rect.x = LARGURA - random.randrange(30,200,90)
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.y = random.randrange(50,200,50)
        self.rect.x -= velocidade_jogo

class Chao(pygame.sprite.Sprite):
    def __init__(self,pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32,0),(32,32))
        self.image = pygame.transform.scale(self.image, (32*2,32*2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 64
        self.rect.x = pos_x * 64
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= velocidade_jogo
class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32,0),(32,32))
        self.image= pygame.transform.scale(self.image, (32*2,32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (LARGURA,ALTURA - 64)
        
    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.x = random.randrange(LARGURA,LARGURA*2,250)
        self.rect.x -= velocidade_jogo
class Dino_voador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dino_img = []
        for i in range(2):
            img = sprite_sheet.subsurface(((3+i) * 32,0),(32,32))
            img = pygame.transform.scale(img, (32*3,32*3))
            self.dino_img.append(img)
        self.index = 0
        self.image = self.dino_img[self.index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (LARGURA,ALTURA//2)
    
    def update(self):
        if self.index > 1:
            self.index = 0
        self.index += 0.25
        self.image = self.dino_img[int(self.index)]
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= velocidade_jogo
all_sprite = pygame.sprite.Group()    
dino = Dino() 
all_sprite.add(dino)
for i in range(4):
    nuvens = Nuvem()
    all_sprite.add(nuvens)
for i in range(LARGURA*2//64):
    chao = Chao(i)
    all_sprite.add(chao)


grupo_obstaculos = pygame.sprite.Group()
"""
cacto = Cacto()
all_sprite.add(cacto)
grupo_obstaculos.add(cacto) """
while True:
    RELOGIO.tick(25)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if dino.rect.y != dino.y_init:
                    pass
                else:
                    dino.jump()
            if event.key == pygame.K_UP:
                if dino.rect.y != dino.y_init:
                    pass
                else:
                    dino.jump()
            if event.key == pygame.K_w:
                if dino.rect.y != dino.y_init:
                    pass
                else:
                    dino.jump()
            if event.key == pygame.K_DOWN:
                if dino.rect.y >= dino.y_init:
                    pass
                else:
                    dino.agachar()
            if event.key == pygame.K_s:
                if dino.rect.y >= dino.y_init:
                    pass
                else:
                    dino.agachar()  
    
    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)
    all_sprite.draw(tela)
    if colisoes and colidiu == False:
        som_morte.play()
        colidiu = True
    if PONTOS >= int(RECORD_TOTAL):
        atualizar_record(PONTOS)
    if colidiu == True:
        pass
    else:
        PONTOS += 1
        all_sprite.update()
        texto_pontos = Exibe_msg(PONTOS,40,(0,0,0))
        texto_record = Record(RECORD_TOTAL,40,(0,0,0))
    if PONTOS % 400 <= 0:
        dino_voador = Dino_voador()
        all_sprite.add(dino_voador)
        grupo_obstaculos.add(dino_voador)
    for i in range(random.binomialvariate(1,0.003999)):
    #for i in range(random.binomialvariate(1,)):
        cacto = Cacto()
        all_sprite.add(cacto)
        grupo_obstaculos.add(cacto)
    """if PONTOS % 400 <= 0: 
        cacto = Cacto()
        all_sprite.add(cacto)
        grupo_obstaculos.add(cacto)"""
    if PONTOS % 100 <= 0:
        if colidiu == True:
            Som_pontuação.stop()
        else:
            Som_pontuação.play( )
            velocidade_jogo += 1
        
    tela.blit(texto_pontos, (520,30))
    tela.blit(texto_record, (520,60))
    pygame.display.flip()
