import pygame
import random
import sys
import cv2
import mediapipe as mp

#  Pygame Setup 
pygame.init()
pygame.mixer.init()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game - Hand Gesture Control")
clock = pygame.time.Clock()

# Colors
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
white = (255,255,255)

# Snake settings
snake_block = 20
snake_speed = 12
snake = [[100,100]]
direction = "RIGHT"

# Food
food_x = random.randrange(0, width, snake_block)
food_y = random.randrange(0, height, snake_block)

# Score
score = 0
high_score = 0
score_font = pygame.font.SysFont(None, 30)

def show_score():
    value = score_font.render(f"Score: {score}  High Score: {high_score}", True, white)
    screen.blit(value, [10,10])

# Game State
running = True
game_over = False
font = pygame.font.SysFont(None, 40)

def show_game_over():
    text = font.render("Game Over! Press R to Restart or Q to Quit", True, white)
    screen.blit(text, [40, height//2 - 20])

# ---------- Sound ----------
eat_sound = pygame.mixer.Sound("alarm.wav")

# ---------- OpenCV & MediaPipe Setup ----------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# ---------- Hand gesture smooth movement ----------
prev_x, prev_y = 0, 0
threshold = 0.03  # movement sensitivity

# ---------- Main Game Loop ----------
while running:

    # --- Hand Detection ---
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                x = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                y = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                # Smooth swipe detection
                if prev_x != 0 and prev_y != 0:
                    dx = x - prev_x
                    dy = y - prev_y

                    if abs(dx) > abs(dy):  # horizontal swipe
                        if dx > threshold and direction != "LEFT":
                            direction = "RIGHT"
                        elif dx < -threshold and direction != "RIGHT":
                            direction = "LEFT"
                    else:  # vertical swipe
                        if dy > threshold and direction != "UP":
                            direction = "DOWN"
                        elif dy < -threshold and direction != "DOWN":
                            direction = "UP"

                prev_x, prev_y = x, y

                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    # --- Event Handling (optional keyboard) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"

            if game_over:
                if event.key == pygame.K_r:
                    snake = [[100,100]]
                    direction = "RIGHT"
                    food_x = random.randrange(0, width, snake_block)
                    food_y = random.randrange(0, height, snake_block)
                    score = 0
                    snake_speed = 12
                    prev_x, prev_y = 0,0
                    game_over = False
                elif event.key == pygame.K_q:
                    running = False

    # --- Move Snake ---
    if not game_over:
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

        # --- Food Eat + Score + Speed ---
        if head[0] == food_x and head[1] == food_y:
            food_x = random.randrange(0, width, snake_block)
            food_y = random.randrange(0, height, snake_block)
            score += 10
            eat_sound.play()

            if snake_speed < 25:
                snake_speed += 1
        else:
            snake.pop(0)

        # --- Collision ---
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            if score > high_score:
                high_score = score
            game_over = True

        for block in snake[:-1]:
            if block == head:
                if score > high_score:
                    high_score = score
                game_over = True

    # --- Draw ---
    screen.fill(black)
    show_score()
    pygame.draw.rect(screen, red, [food_x, food_y, snake_block, snake_block])
    for block in snake:
        pygame.draw.rect(screen, green, [block[0], block[1], snake_block, snake_block])

    if game_over:
        show_game_over()

    pygame.display.update()
    clock.tick(snake_speed)

    # --- Show camera (optional) ---
    cv2.imshow("Hand Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False

# ---------- Cleanup ----------
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()