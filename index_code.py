
import pygame
from time import sleep
import random
import math
from pygame import mixer
pygame.init()
mixer.init()
WIDTH, HEIGHT = 2000, 1400
speed0 = 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chromosomo")
title_font = pygame.font.Font("pixel_1.ttf",  150)
owner_font = pygame.font.SysFont('couriernew' , 30)
button_font = pygame.font.SysFont('couriernew', 40)
text_font = pygame.font.Font("pixel_2.ttf" , 34)
text_font2 = pygame.font.SysFont('impact', 50)
text_font0 = pygame.font.Font("pixel_2.ttf", 60)
text2_font = pygame.font.SysFont('impact', 70)
small_font = pygame.font.SysFont('Arial', 20)
BACKGROUND_COLOR = (20, 20, 40)  
BLUE = (0, 102, 204)
PURPLE = (153, 51, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
YELLOW = (255, 255, 0)  
VERT = (0, 255, 0)
START_MENU = 0
EXPLANATION = 1
GAME_LEVEL_1 = 2
GAME_LEVEL_2 = 3
GAME_LEVEL_3 = 4
WIN_SCREEN = 5
LOSE_SCREEN = 6
current_state = START_MENU
level = 1
player = None
enemies = []
goal = None
key = None
maze = None
key_found = False
def create_level_1():
    maze = [
        "#####################",
        "#          S        #",
        "# #### ## # ##### # #",
        "#    #    #   #     #",
        "## ##### #### # ### #",
        "#      #      #     #",
        "# ####   ######## # #",
        "# #    #          # #",
        "# # ############# # #",
        "# #      #        # #",
        "# ###  ###### ####  #",
        "#         #     G # #",
        "#####################"
    ]
    return maze
def create_level_2():
    maze = [
        "#####################",
        "#  ##G  #         # #",
        "# ## # ## # ####### #",
        "#    #    #   #  ####",
        "## ##### #### # #####",
        "#      #      #    ##",
        "# #### # ######## # #",
        "# #    #          # #",
        "# # ############# # #",
        "# #                 #",
        "# ############### ###",
        "#                S  #",
        "#####################"
    ]
    return maze
def create_level_3():
    maze = [
        "#####################",
        "#         S        ##",
        "# #### ##   ##### ###",
        "#    #   ##   #   K##",
        "## ##### ## # # #####",
        "#      #    #       #",
        "# ####   ######## # #",
        "# #   ##  #       # #",
        "# # ####  ####### # #",
        "# # ##   #   ##     #",
        "########D########## #",
        "#     ##          G #",
        "#####################"
    ]
    return maze

# Classes elements du jeu :
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = button_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Player:
    def __init__(self, x, y, level , image):
        self.x = x
        self.y = y
        self.radius = 5
        self.level = level
        self.speed = speed0
        self.image = None
        if level == 1 :
            original_image = pygame.image.load('chromosome_mono_1.webp').convert_alpha( )
            self.image = pygame.transform.scale(original_image, (50, 50)) 
        elif level == 2 :
            original_image = pygame.image.load('chromosome_bi.webp').convert_alpha( )
            self.image = pygame.transform.scale(original_image, (50, 50))
        elif level == 3 :
            original_image = pygame.image.load('chromosome_mono_2.webp').convert_alpha( )
            self.image = pygame.transform.scale(original_image, (50, 50))             
    def draw(self, surface):
        
        image_rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, image_rect)

    def move(self, dx, dy, maze):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        cell_x = int(((new_x - 265) // 70))
        cell_y = int(((new_y - 245) // 70))
        
        if 0 <= cell_y < len(maze) and 0 <= cell_x < len(maze[0]):
            if maze[cell_y][cell_x] != '#':
                self.x = new_x
                self.y = new_y

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 12
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.change_direction_timer = 0
    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.x, self.y), self.radius)
        text_surf = small_font.render("C", True, WHITE)
        text_rect = text_surf.get_rect(center=(self.x, self.y))
        surface.blit(text_surf, text_rect)
    def move(self, player_x, player_y, maze):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        dx, dy = dx/dist, dy/dist
        self.direction = (dx, dy)
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        cell_x = int(((new_x - 265) // 70))
        cell_y = int(((new_y - 245) // 70))
        
        self.x = new_x
        self.y = new_y

class Goal:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.radius = 20
                                                           
        
    def draw(self, surface):
        pygame.draw.circle(surface, GREEN, (self.x, self.y), self.radius)
        text_surf = button_font.render(self.symbol, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.x, self.y))
        surface.blit(text_surf, text_rect)

class Key:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.collected = False
        
    def draw(self, surface):
        if not self.collected:
            pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.radius)
            text_surf = small_font.render("K", True, BLACK)
            text_rect = text_surf.get_rect(center=(self.x, self.y))
            surface.blit(text_surf, text_rect)


play_button = Button(WIDTH//2 - 150, HEIGHT//2 + 100, 300, 60, "PLAY", BLUE, (144, 15, 15))
credits_button = Button(WIDTH//2 - 150, HEIGHT//2  + 170, 300, 60, "CREDITS", (240, 240, 240), (150, 150, 150))
quit_button = Button(WIDTH//2 - 150, HEIGHT//2 + 240, 300, 60, "QUIT", RED, GREY)
def draw_start_screen():
    dna = pygame.image.load ('dna.png')    
    chs = pygame.image.load('chromosomes.webp')
    image = pygame.image.load("background.jpg")
    screen.blit(image, (0, 0)) 
    screen.blit(image, (700, 0))
    screen.blit(image, (1400, 0))
    title_surf = title_font.render("CHROMOSOMO", True, (224,224,224))
    title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 200))
    screen.blit(title_surf, title_rect)
    owner_surf = owner_font.render('Version 1.0 - Developped By A.B', True, WHITE)
    screen.blit(owner_surf, (WIDTH // 2 + 40, HEIGHT //2 - 300))
    play_button.draw(screen)
    quit_button.draw(screen)
    credits_button.draw(screen)
    screen.blit(dna,(WIDTH // 2 - 185, HEIGHT // 2 - 250))
    screen.blit(dna,(WIDTH // 2 + 20 , HEIGHT // 2 - 250 ))
    screen.blit(chs, (WIDTH // 2 + 600, HEIGHT // 2 - 50))
    screen.blit(chs, (WIDTH // 2 - 800, HEIGHT // 2 + 100))
facile_button = Button(WIDTH//2 - 600, HEIGHT//2 + 120, 300, 60, "Facile", VERT, (120, 120, 120))
normal_button = Button(WIDTH//2 - 350, HEIGHT//2  + 120, 300, 60, "Normal", YELLOW, (150, 150, 150))
difficile_button = Button(WIDTH//2 - 100, HEIGHT//2 + 120, 300, 60, "Difficile", RED, GREY)    
    
def draw_explanation_screen():
    screen.fill((25 , 0 , 51))
    text_y = HEIGHT // 2 - 100
    text_surf1 , text_surf2 , text_surf3 , text_surf4 = text_font.render("Tu joues avec un chromosome dans une labyrinthe ou la Colchicine te chasse .Tu dois atteindre d'abord S=Synthèse pour synthétiser une autre chromatide" , True , WHITE ) , text_font.render ("puis atteindre A = l'Anaphase pour se diviser et à la fin , il faut que tu aies le clé avant que tu iras vers T = Télophase pour completer le cycle cellulaire  " , True, WHITE) , text_font.render("Utilise les flèches directionnelles pour te déplacer. Évite les Colchicines rouges qui te poursuivent. Bonne chance !" , True , WHITE) , text_font.render("(Attention , les Colchicines seront de plus en plus rapide  . . . Choisir La difficulté : ", True , WHITE)
    alarm = text2_font.render('Sois Loin de Colchicine !', True, RED)
    colchicine = pygame.image.load('colchicine_monstre.png')
    colchicine = pygame.transform.scale(colchicine, (300,300))
    screen.blit(colchicine, (WIDTH - WIDTH/6 - 300  , HEIGHT / 2 + 200))
    screen.blit(alarm, (WIDTH/8  , HEIGHT / 2 + 300))
    screen.blit(text_surf1, ((WIDTH/8 - 190 , HEIGHT / 2 - 300)) ) 
    screen.blit(text_surf2, ((WIDTH/8 - 180 + 50 , HEIGHT / 2 - 230)))
    screen.blit(text_surf3, ((WIDTH/8 - 180 + 250 , HEIGHT / 2 + - 160)))
    screen.blit(text_surf4, ((WIDTH/8 - 180 + 500 , HEIGHT / 2 + - 90)))
    facile_button.draw(screen)
    normal_button.draw(screen)
    difficile_button.draw(screen)
    

# dessiner labyrinthe
def draw_maze(maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * 70 + 265 , y * 70 + 245  , 50, 50)    # normal cube size
            if cell == '#':
                pygame.draw.rect(screen, (50, 50, 100), rect)        # walls        
            elif cell == 'G' :
                pygame.draw.rect(screen, (153, 153, 0), rect)
            elif cell == 'S' :
                pygame.draw.rect(screen, (64, 64, 64), rect)
            elif cell == 'K' :
                pygame.draw.rect(screen, (153, 0, 76), rect)                
            else  :
                pygame.draw.rect(screen, BACKGROUND_COLOR, rect)    # ways
            pygame.draw.rect(screen, (70, 70, 120), rect, 4)  # grid lines

def init_level(level_num):
    global player, enemies, goal, key,  maze, key_found
    
    key_found = False
    
    if level_num == 1:
        speed = 2
        maze = create_level_1()
        player_x = player_y = goal_x = goal_y = 0
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 'S':  # S = Start 
                    player_x, player_y =  x * 70 + 265 + 25  ,    y * 70 + 245 + 25  # 25 = half of 50
                elif cell == 'G':  # G = Goal
                    goal_x   ,    goal_y = x * 70 + 265 + 25  ,    y * 70 + 245 + 25  # Center in cell
        player = Player(player_x, player_y, 1 , None)
        goal = Goal(goal_x, goal_y, "S")
        enemies = []
        for _ in range(2) :
           while True:
                enemy_grid_x = random.randint(1,19) 
                enemy_grid_y = random.randint(1 ,7) 
                enemy_x = enemy_grid_x * 70 + 265 + 25  # 25 = half of 50 (cell width)
                enemy_y = enemy_grid_y * 70 + 245 + 25  # Center in cell
                if maze[enemy_grid_y][enemy_grid_x] != '#' and (enemy_x , enemy_y) != (player_x  , player_y ) and (enemy_x , enemy_y) != (goal_x , goal_y):
                   enemies.append(Enemy(enemy_x, enemy_y, 2))
                   break
    elif level_num == 2:
        maze = create_level_2()
        player_x = player_y = goal_x = goal_y = 0
        
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
               if cell == 'S':  # S = Start 
                    player_x, player_y =  x * 70 + 265 + 25  ,    y * 70 + 245 + 25  
               elif cell == 'G':  # G = Goal
                    goal_x   ,    goal_y = x * 70 + 265 + 25  ,    y * 70 + 245 + 25  
        player = Player(player_x, player_y, 2 , None)
        goal = Goal(goal_x, goal_y, "A")
        enemies = []
        for _ in range(3):
            while True:
                enemy_grid_x = random.randint(1,19) 
                enemy_grid_y = random.randint(1 ,7) 
                enemy_x = enemy_grid_x * 70 + 265 + 25  # 25 = half of 50 (cell width)
                enemy_y = enemy_grid_y * 70 + 245 + 25  # Center in cell
                if maze[enemy_grid_y][enemy_grid_x] != '#' and (enemy_x , enemy_y) != (player_x , player_y) and (enemy_x , enemy_y) != (goal_x , goal_y):
                   enemies.append(Enemy(enemy_x, enemy_y, 2.3))
                   break
            
    elif level_num == 3:
        maze = create_level_3()
        player_x = player_y = goal_x = goal_y = key_x = key_y  = 0
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 'S':
                    player_x, player_y = x * 70 + 265 + 25, y * 70 + 245 + 25
                elif cell == 'G':
                    goal_x, goal_y = x * 70 + 265 + 25, y * 70 + 245 + 25
                elif cell == 'K':
                    key_x, key_y = x * 70 + 265 + 25, y * 70 + 245 + 25
        player = Player(player_x, player_y, 3 , None)
        goal = Goal(goal_x, goal_y, "T")
        key = Key(key_x, key_y)
        
        enemies = []
        for _ in range(3):
            while True:
                enemy_x = random.randint(1, len(maze[0])-2) * 40 + 20
                enemy_y = random.randint(1, len(maze)-2) * 40 + 20
                if maze[enemy_y//40][enemy_x//40] != '#':
                    break
            enemies.append(Enemy(enemy_x, enemy_y, 2.5))
def draw_game_screen():
    screen.fill(BACKGROUND_COLOR)
    draw_maze(maze)
    if level == 3 and not key_found :
        key.draw(screen)
    goal.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    player.draw(screen)

def draw_win_screen():
    screen.fill((64,64,64))
    pygame.draw.circle(screen, (100, 100, 200), (WIDTH//3, HEIGHT//2), 150)
    pygame.draw.circle(screen, (80, 80, 180), (WIDTH//3, HEIGHT//2), 130)
    pygame.draw.circle(screen, (150, 150, 220), (WIDTH//3, HEIGHT//2), 60)
    
    pygame.draw.circle(screen, (100, 100, 200), (2*WIDTH//3, HEIGHT//2), 150)
    pygame.draw.circle(screen, (80, 80, 180), (2*WIDTH//3, HEIGHT//2), 130)
    pygame.draw.circle(screen, (150, 150, 220), (2*WIDTH//3, HEIGHT//2), 60)
    congrats_text = title_font.render("Félicitations!", True, GREEN)
    congrats_rect = congrats_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(congrats_text, congrats_rect)
    
    sub_text = text_font2.render("Vous avez complété le cycle cellulaire et obtenu deux cellules filles!", True, WHITE)
    sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 150))
    screen.blit(sub_text, sub_rect)

def draw_lose_screen():
    screen.fill((52,0,0))
    chromosome = pygame.image.load("chromosome_bi.webp")
    chromosome__ = pygame.transform.scale(chromosome  , (20,20))
    screen.blit(chromosome,(WIDTH//2 - 320, HEIGHT//2 - 250))
    pygame.draw.line(screen, RED, (WIDTH//2 - 100, HEIGHT//2 + 150 ), (WIDTH//2 + 100, HEIGHT//2 - 70), 10)
    pygame.draw.line(screen, RED, (WIDTH//2 + 100, HEIGHT//2 + 150 ), (WIDTH//2 - 100, HEIGHT//2 - 70), 10)
    
    lose_text = title_font.render("Chromosome Attrapé!", True, RED)
    lose_rect = lose_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(lose_text, lose_rect)
    
    sub_text = text_font0.render("Le chromosome a été dévoré par la Colchicine. Réessayer( Espace ) ", True, WHITE)
    sub_rect = sub_text.get_rect(center=(WIDTH//2 - 60, HEIGHT//4 + 120))
    screen.blit(sub_text, sub_rect)



# Boucle principale du jeu


clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    click = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_state == WIN_SCREEN or current_state == LOSE_SCREEN:
                    current_state = START_MENU
                    level = 1
                    init_level(1)
                    key_found = False
                    gate_open = False
            elif event.key == pygame.K_ESCAPE:
                if current_state == WIN_SCREEN or current_state == LOSE_SCREEN:
                    running = False
    if current_state == EXPLANATION:
                    facile_button.check_hover(mouse_pos)
                    normal_button.check_hover(mouse_pos)
                    difficile_button.check_hover(mouse_pos)
                    if facile_button.is_clicked(mouse_pos, click):
                        speed0 = 8 
                        init_level(1)
                        print(speed0)
                        current_state = GAME_LEVEL_1
                    if normal_button.is_clicked(mouse_pos, click):
                        speed0 = 5
                        init_level(1)
                        current_state = GAME_LEVEL_1
                    if difficile_button.is_clicked(mouse_pos, click):
                        speed0 = 3
                        init_level(1)
                        current_state = GAME_LEVEL_1
    if current_state == START_MENU:
        play_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        credits_button.check_hover(mouse_pos)
        
        if play_button.is_clicked(mouse_pos, click):
            current_state = EXPLANATION

            
        if quit_button.is_clicked(mouse_pos, click):
            running = False
        if credits_button.is_clicked(mouse_pos, click):
            screen.fill(BLACK)
            text0 = title_font.render("Nothing Here . . . Yet :)", True, WHITE)
            screen.blit(text0, (WIDTH//2 - 800, HEIGHT//2 - 200))
            pygame.display.flip()
            sleep(3)
            current_state = START_MENU

        draw_start_screen()
        
    elif current_state == EXPLANATION:
        draw_explanation_screen()
        
    elif current_state in [GAME_LEVEL_1, GAME_LEVEL_2, GAME_LEVEL_3]:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = +1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = +1
            
        player.move(dx, dy, maze)
        
        for enemy in enemies:
            if not keys[pygame.K_l] :                     # cheat code to disable enemies
               enemy.move(player.x, player.y, maze)
            
            dist = math.sqrt((player.x - enemy.x)**2 + (player.y - enemy.y)**2)
            if dist < player.radius + enemy.radius:
                current_state = LOSE_SCREEN
        
        dist_to_goal = math.sqrt((player.x - goal.x)**2 + (player.y - goal.y)**2)
        if dist_to_goal < player.radius + goal.radius :   
            if level == 1 and dist_to_goal < player.radius + goal.radius :
                current_state = GAME_LEVEL_2
                level = 2
                init_level(2)
            elif level == 2 and dist_to_goal < player.radius + goal.radius :        
                current_state = GAME_LEVEL_3
                level = 3
                init_level(3)
            elif level == 3 and key_found == True  :
                   current_state = WIN_SCREEN
        
        if level == 3 and not key_found == True:
            dist_to_key = math.sqrt((player.x - key.x)**2 + (player.y - key.y)**2)
            if dist_to_key < player.radius + key.radius:
                key_found = True
                key.collected = True
        draw_game_screen()
    elif current_state == WIN_SCREEN:
        draw_win_screen()
    elif current_state == LOSE_SCREEN:
        draw_lose_screen()
        if keys[pygame.K_SPACE] :
            current_state = GAME_LEVEL_1    
            level = 1
            init_level(1)
            key_found = False
            draw_game_screen()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

sys.exit()
