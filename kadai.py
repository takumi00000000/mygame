import pygame
import sys
import random


pygame.init()
pygame.mixer.init()  


screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Avoidance Game")


white = (255, 255, 255)
black = (0, 0, 0)


character_image = pygame.image.load('New Piskel-1.png.png')
character_width = 70 
character_height = 120 
character_image = pygame.transform.scale(character_image, (character_width, character_height))


obstacle_image = pygame.image.load('/Users/toyotatakumi/Desktop/info2-2023/New Piskel-1.png (1).png')
obstacle_width = 50
obstacle_height = 50
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))


heart_image = pygame.image.load('kaihuku.png')  
heart_width = 30
heart_height = 30
heart_image = pygame.transform.scale(heart_image, (heart_width, heart_height))  
heart_speed = 5
heart_frequency = 15 


glove_width = 30
glove_height = 30
glove_speed = 5
glove_frequency = 20  


obstacle_base_speed = 4
obstacle_speed = obstacle_base_speed
num_obstacles = 5  


obstacle_speed_increase_interval = 5 
last_speed_increase_time = 0 


max_life = 3
life = max_life


font = pygame.font.SysFont(None, 25)


character_x = screen_width // 2 - character_width // 2
character_y = screen_height - character_height - 10

obstacles = []
hearts = []
gloves = []

for _ in range(num_obstacles):
    obstacle_x = random.randint(0, screen_width - obstacle_width)
    obstacle_y = random.randint(-screen_height, 0)
    obstacles.append([obstacle_x, obstacle_y]) 


clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()


last_heart_spawn_time = 0


collision_sound = pygame.mixer.Sound('dageki.mp3')

def draw_character_image(x, y):
    screen.blit(character_image, (x, y))

def draw_obstacle(obstacle_rect):
    screen.blit(obstacle_image, obstacle_rect.topleft)

def draw_heart(x, y):
    screen.blit(heart_image, (x, y))  

def draw_glove(x, y):
    orange = (255, 165, 0)
    pygame.draw.polygon(screen, orange, [(x, y), (x + glove_width, y), (x + glove_width, y + glove_height),
    (x, y + glove_height)])

def draw_life(life):
    text = font.render("Life: " + str(life), True, white)
    screen.blit(text, (10, 10))

def draw_time(seconds):
    text = font.render("Time: {:.2f}".format(seconds), True, white)
    screen.blit(text, (10, 30))

def draw_game_over(seconds):
    font_large = pygame.font.SysFont(None, 50)
    text = font_large.render("Game Over", True, white)
    screen.blit(text, (screen_width // 2 - 100, screen_height // 2 - 25))
    text_seconds = font.render("Time: {:.2f}".format(seconds), True, white)
    screen.blit(text_seconds, (screen_width // 2 - 50, screen_height // 2 + 25))

def game_over():
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    draw_game_over(elapsed_seconds)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()


pygame.mixer.music.load('human.mp3') 
pygame.mixer.music.play(-1)


while True:
    current_time = pygame.time.get_ticks() / 1000  

    
    if current_time - last_speed_increase_time > obstacle_speed_increase_interval:
        obstacle_speed += 1 
        last_speed_increase_time = current_time

   
    if current_time - last_heart_spawn_time > heart_frequency:
        heart_x = random.randint(0, screen_width - heart_width)
        heart_y = -heart_height 
        hearts.append([heart_x, heart_y])
        last_heart_spawn_time = current_time

  
    for heart in hearts:
        heart[1] += heart_speed  
        if heart[1] > screen_height:
            hearts.remove(heart) 

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

   
    character_x, character_y = pygame.mouse.get_pos()
    character_x = max(0, min(character_x, screen_width - character_width))
    character_y = max(0, min(character_y, screen_height - character_height))

    
    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

  
    for i, obstacle in enumerate(obstacles):
        obstacle[1] += obstacle_speed
        if obstacle[1] > screen_height:
            obstacle[0] = random.randint(0, screen_width - obstacle_width)
            obstacle[1] = -obstacle_height


    for i, obstacle in enumerate(obstacles):
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if character_rect.colliderect(obstacle_rect):
            if pygame.mouse.get_pressed()[0]:  
                pass
            else:
                collision_sound.play()  
                life -= 1
                if life <= 0:
                    game_over()
            obstacles[i] = [random.randint(0, screen_width - obstacle_width), -obstacle_height]


    for heart in hearts[:]:  
        heart_rect = pygame.Rect(heart[0], heart[1], heart_width, heart_height)
        if character_rect.colliderect(heart_rect):
            life = min(life + 1, max_life) 
            hearts.remove(heart)

   
    screen.fill(black)
    draw_character_image(character_x, character_y)
    for obstacle in obstacles:
        draw_obstacle(pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height))
    for heart in hearts:
        draw_heart(heart[0], heart[1])
    draw_life(life)
    draw_time(current_time)

    pygame.display.update()
    clock.tick(60)

