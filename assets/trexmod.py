
import pygame
import random
import os



pygame.init()


DINO_IMG = pygame.image.load(os.path.join("assets", "trex_img.png"))
CACTUS_IMG = pygame.image.load(os.path.join("assets", "cactus_img.png"))
WIDTH, HEIGHT = 900, 500
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
ORANGE = (255,165,0)

Xspawn = 40
# TAMANHO DOS OBSTACULOS

MEDIO = (20,50)

GROUND = 480

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trex")
G = 35

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x 
    offset_y = obj2.y - obj1.y 
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class Personagem:
    

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = DINO_IMG
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y - self.img.get_height()))

    def update_position(self, tempo, velPulo, pulo):
        
        if pulo == False:
            self.y = GROUND

        else:
            self.y = self.y - velPulo + G*tempo

     

class Obstaculo:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        

    def draw(self, window):
        window.blit(self.img, (self.x, self.y - self.img.get_height()))

    def move(self, vel_obs):
        self.x -= vel_obs



    

def main(lucas, best_score):
    clock = pygame.time.Clock()
    run = True
    
    contador = 0
    velPulo = 11
    pulo = False 
    velx = 3
    vel_obs = 7
    wave_length = 0
    timer_obs = 0
    k = 0
    tempo_queda = (velPulo/G)*2
    time_list = []
    obstaculos = []
    pontos = 0
    level = 1
    score = 0
    time_game_over = 0
    game = True
    while run:
        clock.tick(60)
        WIN.fill(WHITE)
        lucas.draw(WIN)
        title_font = pygame.font.SysFont("comicsans", 30)
        if pontos % 6 == 0:
            score = pontos/6
        show_score = title_font.render(f"{round(score)}", 1, (BLACK))
        show_best_score = title_font.render(f"HI {round(best_score)}", 1, (BLACK))
        WIN.blit(show_score, (WIDTH - show_score.get_width() - 20, 10))
        WIN.blit(show_best_score, (WIDTH - show_score.get_width() - show_best_score.get_width() - 40, 10))
        
            


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    
        keys = pygame.key.get_pressed()

       
        if keys[pygame.K_UP] and lucas.y == GROUND:
            
            contador = 0
            pulo = True 


        if contador/60 >  tempo_queda:
            pulo = False 

        if keys[pygame.K_RIGHT]:
            lucas.x += velx

        if keys[pygame.K_LEFT]:
            lucas.x -= velx


        for obs in obstaculos:
            obs.draw(WIN)
            if collide(obs, lucas) and game == True:
                lucas.x, lucas.y = Xspawn, GROUND
                if score > best_score:
                    best_score = score
                time_game_over = 1
                game = False
                lucas.x = -1000

        if time_game_over != 0:
            title_game_over = title_font.render("GAME OVER!", 1, (BLACK))
            WIN.blit(title_game_over, (WIDTH/2 - title_game_over.get_width()/2, HEIGHT/2))
            time_game_over += 1
            if time_game_over > 3 * 60:
                run = False


        if time_list == []:
            timer_obs = 0
            if pontos >= 100 * level:
                if vel_obs < 12:
                    vel_obs += 1
                else: 
                    vel_obs = 12
                level += 1
                print("vel",vel_obs)
            wave_length = 6
            min_space = 400 + CACTUS_IMG.get_width()
            max_space = 800 + CACTUS_IMG.get_width()
            min_time = min_space / (60*vel_obs)
            max_time = max_space / (60*vel_obs)
            last_time = 0
            for i in range(wave_length):
                print(i)
                time = random.uniform(min_time, max_time)
                new_time = time + last_time

                time_list.append(new_time)

                last_time = new_time
        
        
        if timer_obs == round(time_list[k]*60):
            obs = Obstaculo(1000, GROUND, CACTUS_IMG)
            obstaculos.append(obs)
            time_list.remove(time_list[k])
            
        for obs in obstaculos:
            obs.move(vel_obs)
            if obs.x < -obs.img.get_width():
                obstaculos.remove(obs)
        pontos += 1
        timer_obs += 1

        
        lucas.update_position(contador/60, velPulo, pulo)
        contador += 1
        
        pygame.display.update()
    return best_score    

def main_menu():

    run = True
    best_score = 0
    new_best_score = 0
    while run:
        lucas = Personagem(Xspawn,GROUND)
        WIN.fill(WHITE)
       
        lucas.draw(WIN)
        title_font = pygame.font.SysFont("comicsans", 30)

        title_label = title_font.render("Aperte espaço para iniciar o jogo!", 1, (BLACK))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2,350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                if new_best_score > best_score:
                    best_score = new_best_score
                    new_best_score = main(lucas, new_best_score)
                    
                else:

                    new_best_score = main(lucas, best_score)
        pygame.display.update()

    pygame.quit()

main_menu()