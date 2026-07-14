import pygame
import random
import sys

pygame.init()

# Window
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with Score")

clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Snake settings
snake_block = 20
snake_speed = 12
snake = [[100, 100]]
direction = "RIGHT"

# Food
food_x = random.randrange(0, width, snake_block)
food_y = random.randrange(0, height, snake_block)

# Score
score = 0
score_font = pygame.font.SysFont(None, 35)

def show_score():
    value = score_font.render("Score : " + str(score), True, white)
    screen.blit(value, [10, 10])

# Game state
running = True
game_over = False

font = pygame.font.SysFont(None, 40)

def show_game_over():
    text = font.render("Game Over! Press R to Restart or Q to Quit", True, white)
    screen.blit(text, [40, height // 2 - 20])
    pygame.display.update()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Control snake
            if not game_over:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"

            # Restart / Quit
            if game_over:
                if event.key == pygame.K_r:
                    snake = [[100, 100]]
                    direction = "RIGHT"
                    food_x = random.randrange(0, width, snake_block)
                    food_y = random.randrange(0, height, snake_block)
                    score = 0
                    game_over = False
                elif event.key == pygame.K_q:
                    running = False

    if not game_over:
        # Move snake
        head = snake[-1].copy()
        if direction == "LEFT":
            head[0] -= snake_block
        elif direction == "RIGHT":
            head[0] += snake_block
        elif direction == "UP":
            head[1] -= snake_block
        elif direction == "DOWN":
            head[1] += snake_block

        snake.append(head)

        # Food eat + Score add
        if head[0] == food_x and head[1] == food_y:
            food_x = random.randrange(0, width, snake_block)
            food_y = random.randrange(0, height, snake_block)
            score += 10
            print("Score:", score)
        else:
            snake.pop(0)

        # Wall collision
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            game_over = True

        # Self collision
        for block in snake[:-1]:
            if block == head:
                game_over = True

    # Drawing
    screen.fill(black)
    show_score()

    pygame.draw.rect(screen, red, [food_x, food_y, snake_block, snake_block])

    for block in snake:
        pygame.draw.rect(screen, green, [block[0], block[1], snake_block, snake_block])

    if game_over:
        show_game_over()

    pygame.display.update()
    clock.tick(snake_speed)

pygame.quit()
sys.exit()