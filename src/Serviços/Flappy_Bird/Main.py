import pygame
from pygame.locals import *
import os
import random

#VARIAVEIS
LARGURA = 288;ALTURA = 512;PONTOS = 0
#Inicializando
pygame.display.set_caption("FLAPPY BIRD")
pygame.init()
pygame.mixer.init()
#Variaveis
colidiu = False;cano_passou = False;pipe_gap = 100;ultimo_cano = pygame.time.get_ticks()
intervalo_cano = 1500 #milisegundos
x = 0;y = 0;começar = False
#DIRETORIOS
Diretorio_principal = os.path.dirname(__file__)
Diretorio_Audios = os.path.join(Diretorio_principal, "audio")
Diretorio_Imagens = os.path.join(Diretorio_principal, "sprites")
#Sons
som_passar = pygame.mixer.Sound(os.path.join(Diretorio_Audios, "point.ogg"))
som_passar.set_volume(1)
som_voar = pygame.mixer.Sound(os.path.join(Diretorio_Audios, "wing.ogg"))
som_voar.set_volume(1)
som_morte = pygame.mixer.Sound(os.path.join(Diretorio_Audios, "die.ogg"))
som_morte.set_volume(1)
som_hit = pygame.mixer.Sound(os.path.join(Diretorio_Audios, "hit.ogg"))
som_hit.set_volume(1)
#interface
tela = pygame.display.set_mode((LARGURA,ALTURA))
#Carregar imagens de números
numeros = {}
for i in range(10):
    numeros[str(i)] = pygame.image.load(os.path.join(Diretorio_Imagens, f"{i}.png"))
relogio = pygame.time.Clock()
#CLASSES
class Final(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(Diretorio_Imagens, "gameover.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA/2, ALTURA/2)
    def update(self):
        pass
class Inicial(pygame.sprite.Sprite):
    def __init__(self, começar):
        self.init = começar
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(os.path.join(Diretorio_Imagens, "message.png"))
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA/2, ALTURA/2)

    def iniciar(self):
        self.init = True

    def update(self):
        if self.init:
            criar_passaro()
        return self.init
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_bird = []
        self.image_bird.append(pygame.image.load(os.path.join(Diretorio_Imagens, "redbird1.png")))
        self.image_bird.append(pygame.image.load(os.path.join(Diretorio_Imagens, "redbird2.png")))
        self.image_bird.append(pygame.image.load(os.path.join(Diretorio_Imagens, "redbird3.png")))
        self.atual = 1
        self.image = self.image_bird[self.atual]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA/2,300)
        self.velocidade = 0  
        self.gravidade = 1
        self.forca_pulo = -10
        self.angle = 0  
    def jump(self):
        self.velocidade = self.forca_pulo
        som_voar.play()
    def update(self):
        self.velocidade += self.gravidade
        self.rect.y += self.velocidade
        if self.velocidade < 0:
            self.angle = 25  # Ângulo olhando para cima
        else:
            self.angle -= 5
            if self.angle <= -90:
                self.angle = -90
        self.atual += 0.25
        self.image = self.image_bird[int(self.atual)]
        if self.atual >= 2:
            self.atual = 0

        self.image = pygame.transform.rotate(self.image, self.angle)  

       
        if self.rect.y > 380:
            self.rect.y = 380
            self.angle = -90 
        elif self.rect.y < 0:
            self.rect.y = 0
class Chao(pygame.sprite.Sprite):
    def __init__(self,pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(Diretorio_Imagens, "base.png"))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = 400
        self.rect.x = pos_x * LARGURA
        
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= 5
class Cano(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        pygame.sprite.Sprite.__init__(self)
        #CANO NORMAL APONTADO PARA CIMA
        if pos == 1:
            self.image = pygame.image.load(os.path.join(Diretorio_Imagens, "pipe-green.png"))
            self.rect = self.image.get_rect()
            self.rect.topleft = [x,y + int(pipe_gap/2)]
        #VIRA O CANO APONTADO PARA BAIXO
        if pos == -1:
            self.image = pygame.image.load(os.path.join(Diretorio_Imagens, "pipe-green.png"))
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = [x,y - int(pipe_gap/2)]         
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        if self.rect.topright[0] < 0:
            self.kill()
            self.rect.x = LARGURA
        self.rect.x -= 5
#Declarar Grupos
inicio = Inicial(começar)
bird = Bird()
bird_sprite = pygame.sprite.Group()
bg = pygame.sprite.Group()
canos = pygame.sprite.Group()
chao_sprite = pygame.sprite.Group()
grupo_colisao = pygame.sprite.Group()
#Adicionar aos grupos
bg.add(inicio)
for i in range(3):
    chao = Chao(i)
    chao_sprite.add(chao)
grupo_colisao.add(chao)
Go = pygame.sprite.Group() #Game Over
game_over = Final()
#defs
def criar_passaro():
    global bird_sprite
    bird_sprite.add(bird)
def desenhar_pontuacao(tela, pontos):
    str_pontos = str(min(pontos, 999))  # Limitar a pontuação a 999
    largura_total = sum(numeros[d].get_width() for d in str_pontos)
    
    # Posição inicial
    x_inicial = (LARGURA - largura_total) // 2
    y_inicial = 20  # distancia
    
    for digito in str_pontos:
        tela.blit(numeros[digito], (x_inicial, y_inicial))
        x_inicial += numeros[digito].get_width()
def main(começar,colidiu,PONTOS,ultimo_cano,cano_passou):
    while True:
        relogio.tick(30)
        tela.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            #interação
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if not começar:
                        bg.remove(inicio)
                        inicio.iniciar()  
                        começar = inicio.update() 
                    elif colidiu == False:
                        bird.jump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not começar:
                        bg.remove(inicio)
                        inicio.iniciar()  
                        começar = inicio.update() 
                    elif colidiu == False:
                        bird.jump()
        #sistema de colisão
        colisoes = pygame.sprite.spritecollide(bird, grupo_colisao, False, pygame.sprite.collide_mask)
        #Condiçoes
        if começar == True:
            if colisoes and colidiu == False:
                som_hit.play()
                som_morte.play()
                colidiu = True
        if colidiu == True:
            Go.add(game_over)
        else:
            if começar:
                time_now = pygame.time.get_ticks()
                if time_now - ultimo_cano > intervalo_cano:
                    altura_cano = random.randrange(-100,90) 
                    cano_baixo = Cano(LARGURA,int(512/2) + altura_cano,-1)
                    cano_cima = Cano(LARGURA,int(512/2) + altura_cano,1)
                    canos.add(cano_baixo)
                    canos.add(cano_cima)
                    grupo_colisao.add(cano_baixo,cano_cima)
                    ultimo_cano = time_now
            bg.update()
            canos.update()
            chao_sprite.update()
        if len(canos) == 2:
            if bird_sprite.sprites()[0].rect.left > canos.sprites()[0].rect.left\
                and bird_sprite.sprites()[0].rect.right < canos.sprites()[0].rect.right\
                and cano_passou == False:
                cano_passou = True
            if cano_passou == True:
                if bird_sprite.sprites()[0].rect.right > canos.sprites()[0].rect.right:
                    PONTOS += 1
                    som_passar.play()
                    cano_passou = False         
        #sistema de muda de dia para noite
        if PONTOS >= 100 :
            Background = pygame.image.load(os.path.join(Diretorio_Imagens, "background-night.png"))
        else:
            Background = pygame.image.load(os.path.join(Diretorio_Imagens, "background-day.png"))
        #Desenhar a imagem na tela
        tela.blit(Background,(0,0))
        bg.draw(tela)
        canos.draw(tela)
        chao_sprite.draw(tela)
        
        bird_sprite.update()
        bird_sprite.draw(tela)
        desenhar_pontuacao(tela, PONTOS)
        Go.draw(tela)
        Go.update()
        pygame.display.update()
main(começar,colidiu,PONTOS,ultimo_cano,cano_passou)