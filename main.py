import pygame
import random
import time
from PIL import Image

# Load the image
img_path = "C:/Users/gtak2/PycharmProjects/flappy/bird.png"
img = Image.open(img_path)

# Convert the image to RGBA (Red, Green, Blue, Alpha) if it's not already in that mode
img = img.convert("RGBA")

# Get data of the image
data = img.getdata()

# Create a new list to hold the new image data
new_data = []
for item in data:
    # Change all white (also shades of whites)
    # (255, 255, 255) to transparent
    if item[0] in list(range(200, 256)):
        new_data.append((255, 255, 255, 0))  # Adding alpha to make white transparent
    else:
        new_data.append(item)

# Update image data
img.putdata(new_data)

# Save the image
img.save("C:/Users/gtak2/PycharmProjects/flappy/bird_transparent.png", "PNG")

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (1, 50, 32)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)


# Game variables
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_WIDTH = 70
PIPE_HEIGHT = random.randint(150, 450)
PIPE_GAP = 200
BIRD_SIZE = 30
FPS = 60
HIGH_SCORE = 0  # Add this line to initialize the high score variable

# Load images
BIRD_IMG = pygame.image.load("bird_transparent.png").convert_alpha()
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (30, 30))
BACKGROUND_IMG = pygame.image.load("background.png").convert()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize clock
clock = pygame.time.Clock()


def change_bird_color():
    new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    data = img.getdata()
    new_data = []
    for item in data:
        if item[3] != 0:  # Preserve alpha channel
            new_data.append((new_color[0], new_color[1], new_color[2], item[3]))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save("C:/Users/gtak2/PycharmProjects/flappy/bird_transparent.png", "PNG")


# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(SCREEN, DARK_GREEN, pipe['top'])
        pygame.draw.rect(SCREEN, DARK_GREEN, pipe['bottom'])


# Function to check collision
def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.colliderect(pipe['top']) or bird.colliderect(pipe['bottom']):
            return True
    if bird.top <= 0 or bird.bottom >= SCREEN_HEIGHT:
        return True
    return False


# Function to display score
def display_score(score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, BLACK)
    SCREEN.blit(score_text, (10, 10))


# Function to display time
def display_time(start_time):
    elapsed_time = int(time.time() - start_time)
    font = pygame.font.SysFont(None, 36)
    time_text = font.render(f'Time: {elapsed_time}', True, BLACK)
    SCREEN.blit(time_text, (SCREEN_WIDTH - 150, 10))


# Function to draw buttons
def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(SCREEN, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(SCREEN, color, (x, y, w, h))

    font = pygame.font.SysFont(None, 36)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    SCREEN.blit(text_surf, text_rect)
    return False


# Function to display the menu
def menu():
    global HIGH_SCORE
    menu_running = True
    while menu_running:
        SCREEN.blit(BACKGROUND_IMG, (0, 0))

        # Display high score
        font = pygame.font.SysFont(None, 36)
        high_score_text = font.render(f'High Score: {HIGH_SCORE}', True, BLACK)
        SCREEN.blit(high_score_text, (10, 10))

        if draw_button("Play", 150, 200, 100, 50, GREEN, (0, 200, 0)):
            game()
        if draw_button("Exit", 150, 300, 100, 50, RED, (200, 0, 0)):
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(15)


# Function to display "GAME OVER" message
def game_over_screen():
    font = pygame.font.SysFont(None, 36)
    game_over_text = font.render('GAME OVER!!', True, RED)
    SCREEN.blit(game_over_text, (
        SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before returning to the menu


# Main game function
def game():
    global HIGH_SCORE, BIRD_IMG
    bird = pygame.Rect(100, 300, BIRD_SIZE, BIRD_SIZE)
    bird_speed = 0
    pipes = []
    score = 0
    start_time = time.time()

    # Create initial pipes
    for i in range(2):
        pipe_height = random.randint(150, 450)
        pipes.append({
            'top': pygame.Rect(SCREEN_WIDTH + i * (PIPE_WIDTH + 200), 0, PIPE_WIDTH, pipe_height),
            'bottom': pygame.Rect(SCREEN_WIDTH + i * (PIPE_WIDTH + 200), pipe_height + PIPE_GAP, PIPE_WIDTH,
                                  SCREEN_HEIGHT)
        })

    running = True
    while running:
        SCREEN.blit(BACKGROUND_IMG, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_speed = BIRD_JUMP

        # Bird movement
        bird_speed += GRAVITY
        bird.y += int(bird_speed)

        # Pipe movement
        for pipe in pipes:
            pipe['top'].x -= 5
            pipe['bottom'].x -= 5

        # Check if we need to add a new pipe
        if pipes[0]['top'].x < -PIPE_WIDTH:
            pipes.pop(0)
            pipe_height = random.randint(150, 450)
            pipes.append({
                'top': pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height),
                'bottom': pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)
            })
            score += 1
            change_bird_color()  # Change bird color
            BIRD_IMG = pygame.image.load("bird_transparent.png").convert_alpha()
            BIRD_IMG = pygame.transform.scale(BIRD_IMG, (30, 30))

        # Draw everything
        SCREEN.blit(BIRD_IMG, (bird.x, bird.y))
        draw_pipes(pipes)
        display_score(score)
        display_time(start_time)

        # Check for collisions
        if check_collision(bird, pipes):
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    # Update high score
    if score > HIGH_SCORE:
        HIGH_SCORE = score

    game_over_screen()
    menu()


# Run the menu
menu()
