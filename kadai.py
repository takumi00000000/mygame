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
red = (255, 0, 0)

# キャラクターの画像設定
character_image = pygame.image.load('New Piskel-1.png.png')
character_width = 40  # 画像の幅
character_height = 120  # 画像の高さ
character_image = pygame.transform.scale(character_image, (character_width, character_height))

# 障害物の画像設定
obstacle_image = pygame.image.load('/Users/toyotatakumi/Desktop/info2-2023/New Piskel-1.png (1).png')
obstacle_width = 50
obstacle_height = 50
# 画像のスケールが必要な場合は調整する
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))

# アイテム（ハート）の設定
heart_width = 30
heart_height = 30
heart_speed = 5
heart_frequency = 15  # 15秒に1回程度の頻度

# アイテム（グローブ）の設定
glove_width = 30
glove_height = 30
glove_speed = 5
glove_frequency = 20  # 20秒に1回程度の頻度

# 障害物の設定
obstacle_base_speed = 4
obstacle_speed = obstacle_base_speed
num_obstacles = 4  # 同時に降ってくる障害物の数

# ライフの設定
max_life = 3
life = max_life

# フォントの設定
font = pygame.font.SysFont(None, 25)

# 初期位置
character_x = screen_width // 2 - character_width // 2
character_y = screen_height - character_height - 10

obstacles = []
hearts = []
gloves = []

for _ in range(num_obstacles):
    obstacle_x = random.randint(0, screen_width - obstacle_width)
    obstacle_y = random.randint(-screen_height, 0)
    obstacles.append([obstacle_x, obstacle_y])  # 座標をリストに変更

# 時間計測用の変数
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

# 障害物スピードの増加に関連する変数
obstacle_speed_increase_interval = 10  # 10秒ごとにスピードを上げる
last_speed_increase_time = 5

# ハートの生成に関連する変数
last_heart_spawn_time = 0

def draw_character_image(x, y):
    screen.blit(character_image, (x, y))

def draw_obstacle(obstacle_rect):
    screen.blit(obstacle_image, obstacle_rect.topleft)

def draw_heart(x, y):
    pygame.draw.polygon(screen, red, [(x, y + heart_height // 2), (x + heart_width // 2, y),
                                      (x + heart_width, y + heart_height // 2), (x + heart_width // 2, y + heart_height)])

def draw_glove(x, y):
    pygame.draw.polygon(screen, (255, 69, 0), [(x, y), (x + glove_width, y), (x + glove_width, y + glove_height), (x, y + glove_height)])

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

# ゲームループ
while True:
    # 現在の時間を取得
    current_time = pygame.time.get_ticks() / 1000  # ミリ秒を秒に変換

    # 障害物のスピードを時間経過に応じて上げる
    if current_time - last_speed_increase_time > obstacle_speed_increase_interval:
        obstacle_speed += 0.9  # スピードを増加
        last_speed_increase_time = current_time

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # マウスの座標を取得してキャラクターの位置を更新
    character_x, character_y = pygame.mouse.get_pos()
    character_x = max(0, min(character_x, screen_width - character_width))
    character_y = max(0, min(character_y, screen_height - character_height))

    # キャラクターのRectを更新
    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

    # 障害物の移動
    for i, obstacle in enumerate(obstacles):
        obstacle[1] += obstacle_speed
        if obstacle[1] > screen_height:
            obstacle[0] = random.randint(0, screen_width - obstacle_width)
            obstacle[1] = -obstacle_height

    # ハートの移動と衝突判定
    # ...

    # グローブの移動
    # ...

    # 障害物の衝突判定
    for i, obstacle in enumerate(obstacles):
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if character_rect.colliderect(obstacle_rect):
            life -= 1
            obstacles[i] = [random.randint(0, screen_width - obstacle_width), -obstacle_height]
            if life <= 0:
                game_over()

    # 描画処理
    screen.fill(black)
    draw_character_image(character_x, character_y)
    for obstacle in obstacles:
        draw_obstacle(pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height))
    for heart_x, heart_y in hearts:
        draw_heart(heart_x, heart_y)
    for glove_x, glove_y in gloves:
        draw_glove(glove_x, glove_y)
    draw_life(life)
    draw_time(current_time)

    pygame.display.update()
    clock.tick(60)
