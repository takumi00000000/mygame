import pygame
import sys
import random

# 初期化
pygame.init()

# 画面の設定
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Avoidance Game")

# 色の定義
white = (255, 255, 255)
black = (0, 0, 0)

# プレイヤーの設定
player_width = 50
player_height = 50

# 障害物の設定
obstacle_width = 50
obstacle_height = 50
obstacle_base_speed = 8
obstacle_speed = obstacle_base_speed
num_obstacles = 4  # 同時に降ってくる障害物の数

# ライフの設定
life = 3

# フォントの設定
font = pygame.font.SysFont(None, 25)

# 初期位置
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10

obstacles = []

for _ in range(num_obstacles):
    obstacle_x = random.randint(0, screen_width - obstacle_width)
    obstacle_y = random.randint(-screen_height, 0)
    obstacles.append((obstacle_x, obstacle_y))

# 時間計測用の変数
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

def draw_player(x, y):
    pygame.draw.rect(screen, white, [x, y, player_width, player_height])

def draw_obstacle(x, y):
    pygame.draw.rect(screen, white, [x, y, obstacle_width, obstacle_height])

def draw_life(life):
    text = font.render("Life: " + str(life), True, white)
    screen.blit(text, (10, 10))

def game_over():
    font_large = pygame.font.SysFont(None, 50)
    text = font_large.render("Game Over", True, white)
    screen.blit(text, (screen_width // 2 - 100, screen_height // 2 - 25))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# ゲームループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # マウスの座標を取得
    player_x, player_y = pygame.mouse.get_pos()
    player_x -= player_width // 2  # マウス座標を中心に調整

    # 画面外に出ないように制御
    player_x = max(0, min(player_x, screen_width - player_width))

    # 障害物の移動
    for i in range(num_obstacles):
        obstacles[i] = (obstacles[i][0], obstacles[i][1] + obstacle_speed)
        if obstacles[i][1] > screen_height:
            obstacles[i] = (random.randint(0, screen_width - obstacle_width), random.randint(-screen_height, 0))
            obstacle_speed += 0.05  # 避けるほど速度が上がる

    # 衝突判定
    for obstacle_x, obstacle_y in obstacles:
        if (
            player_x < obstacle_x + obstacle_width
            and player_x + player_width > obstacle_x
            and player_y < obstacle_y + obstacle_height
            and player_y + player_height > obstacle_y
        ):
            life -= 1
            obstacles = [(random.randint(0, screen_width - obstacle_width), random.randint(-screen_height, 0)) for _ in range(num_obstacles)]
            obstacle_speed = obstacle_base_speed  # 衝突したら速度をリセット

    # 描画
    screen.fill(black)
    draw_player(player_x, player_y)
    for obstacle_x, obstacle_y in obstacles:
        draw_obstacle(obstacle_x, obstacle_y)
    draw_life(life)

    # ゲームオーバーチェック
    if life <= 0:
        game_over()

    pygame.display.update()
    clock.tick(60)
