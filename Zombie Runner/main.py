
## ZOMBIE RUNNER ##


import pygame
from sys import exit 
from random import randint
from random import choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('Picture/playerrun1.png').convert_alpha()
        player_walk2 = pygame.image.load('Picture/playerrun2.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Picture/playerjump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,400))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('Music/jump.mp3')
        self.jump_sound.set_volume(0.5)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=400:
            self.gravity = -17
            self.jump_sound.play()        
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >=400:
            self.rect.bottom = 400
            
    def animation_state(self):
        if self.rect.bottom < 400:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

           
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'bat':
            bat1 = pygame.image.load('Picture/bat1.png').convert_alpha()
            bat2 = pygame.image.load('Picture/bat2.png').convert_alpha()
            self.frames =  [bat1,bat2]
            y_pos = 280
        else:
            spider = pygame.image.load('Picture/spyder.png').convert_alpha()
            self.frames = [spider] 
            y_pos = 405
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright = (randint(900, 1100),y_pos))
        
    def animation_state(self):
        self.animation_index += 0.09
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 10
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    time = int(pygame.time.get_ticks() / 250) - start_time
    score = font.render(f'Score: {time}',True,(64,64,64))
    score_rect = score.get_rect(center = (400,70))
    screen.blit(score,score_rect)
    return time
    
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        col.play(loops = 0)      
        return False
    else: return True
    
def int_animation():
    global int_surf, player_index
    player_index += 0.08
    if player_index >= len(player_int): player_index = 0
    int_surf = player_int[int(player_index)]
    screen.blit(int_surf,int_rect)

   
pygame.init()
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption("Zombie Runner")
icon = pygame.image.load('Picture/logo.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font('Font/font.ttf', 50)
font2 = pygame.font.Font('Font/font.ttf', 35)
credit = pygame.font.Font('Font/credit.ttf', 20)
game_active = False
start_time = 0 
score = 0
bg_music = pygame.mixer.Sound('Music/bg_music.mp3')
bg_music.play(loops = -1)
bg_music.set_volume(0.5)
col = pygame.mixer.Sound('Music/coll.mp3')

#Gropus
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group() 

#Surface
sky = pygame.image.load('Picture/sky.png').convert()
land = pygame.image.load('Picture/land.jpg').convert()

obstacle_rect_list = [] 

#Intro
player1 = pygame.image.load('Picture/player1.png').convert_alpha()
player2 = pygame.image.load('Picture/player2.png').convert_alpha()
playerr1 = pygame.transform.rotozoom(player1,0,2)
playerr2 = pygame.transform.rotozoom(player2,0,2)
player_index = 0
player_int = [playerr1,playerr2]
int_surf = player_int[player_index]
int_rect = int_surf.get_rect(center = (400,250))
int_animation()

game_name = font.render('Zombie  Runner',True,'#000066')
game_name_rect = game_name.get_rect(center = (400,50))

game_message = font.render('Press  SPACE  to  Start',True,'#000066')
game_message_rect = game_message.get_rect(center = (400,450))

credit = credit.render('Made by: Gyanjyoti',True,'#3333ff')
credit_rect = credit.get_rect(bottomleft = (10,490))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

bat_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bat_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:
            player_gravity = -20
                    
        else:  
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                
                start_time = int(pygame.time.get_ticks() / 250)
                        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['spider','spider','bat','spider'])))
                    
    if game_active:            
        screen.blit(sky,(0,0))                         #blit : block image transfer
        screen.blit(land,(0,400))

        score = display_score()
           
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
              
        #Collision
        game_active = collision_sprite()
            
    else:
        screen.fill('#99ffff')
        int_animation()
        obstacle_rect_list.clear()
        player_gravity = 0
        
        score_message = font.render(f'Your  Score: {score}',True,'#000066')
        score_message_rect = score_message.get_rect(center = (400,430))

        start_again = font2.render(f'Press SPACE to start again', True, '#8F24E3')
        start_again_rect = start_again.get_rect(center = (400,480))
        
        screen.blit(game_name,game_name_rect)
        
        if score == 0:
            screen.blit(game_message,game_message_rect)
            screen.blit(credit,credit_rect)
        else:
            screen.blit(score_message,score_message_rect)
            screen.blit(start_again,start_again_rect)
            screen.blit(credit,credit_rect)
        
        
    pygame.display.update()
    clock.tick(60)
