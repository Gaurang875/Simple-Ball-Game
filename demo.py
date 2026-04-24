import pygame
import random
pygame.init()
pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 700, 700
FPS = 90
VEL = 5
BSPEED = 0.5
ISPEED = 5
COLOR = (0, 0, 0)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brawling Ball")
BACKGROUND = pygame.transform.scale(pygame.image.load('background.jpg'), (WIDTH, HEIGHT))
BUCKET = pygame.transform.scale(pygame.image.load('bucket.png'), (100, 100))
BALL = pygame.transform.scale(pygame.image.load('ball.png'), (40, 40))
title_music = 'Wii Music.mp3'
game_music = ['zelda.mp3', 'super mario.mp3', 'pokemon scary.mp3', 'donkey kong.mp3',
              'tetris theme.mp3', 'sonic.mp3', 'pokemon.mp3', 'mario world.mp3']
game_over_music = 'super mario end.mp3'
def play_music(track):
    try:
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print(f"Failed to load: {track}")
def menu():
    run = True
    font1 = pygame.font.Font(None, 80)
    font2 = pygame.font.Font(None, 40)
    play_music(title_music)
    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        title = font1.render("BRAWLING BALL", True, (0, 0, 255))
        start_text = font2.render("Press ENTER to start", True, (0, 0, 0))
        quit_text = font2.render("Press ESC to quit", True, (0, 0, 0))
        WINDOW.blit(title, (WIDTH / 2 - title.get_width() / 2, 100))
        WINDOW.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 2))
        WINDOW.blit(quit_text, (WIDTH / 2 - quit_text.get_width() / 2, HEIGHT / 2 + 50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
def draw_window(bucket_rect, ball_rect, score, high_score):
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(BUCKET, (bucket_rect.x, bucket_rect.y))
    WINDOW.blit(BALL, (ball_rect.x, ball_rect.y))
    font = pygame.font.Font(None, 40)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 255))
    WINDOW.blit(score_text, (10, HEIGHT - 40))
    WINDOW.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))
    pygame.display.update()
def move_bucket(bucket_rect, keys):
    if keys[pygame.K_LEFT] and bucket_rect.x > 0:
        bucket_rect.x -= VEL
    if keys[pygame.K_RIGHT] and bucket_rect.x < WIDTH - 100:
        bucket_rect.x += VEL
def main():
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    current_song = 0
    play_music(game_music[current_song])
    bucket_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 120, 100, 100)
    ball_rect = pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40)
    run = True
    clock = pygame.time.Clock()
    score = 0
    high_score = 0
    ball_speed = ISPEED
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.USEREVENT:
                current_song = (current_song + 1) % len(game_music)
                play_music(game_music[current_song])
        keys = pygame.key.get_pressed()
        move_bucket(bucket_rect, keys)
        ball_rect.y += ball_speed
        if ball_rect.y > HEIGHT:
            if score > high_score:
                high_score = score
            pygame.mixer.music.stop()
            play_music(game_over_music)
            font = pygame.font.Font(None, 100)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            restart_font = pygame.font.Font(None, 40)
            restart_text = restart_font.render("Press ENTER to restart", True, (0, 0, 0))
            WINDOW.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 4))
            WINDOW.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 2 + 20))
            pygame.display.update()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            score = 0
                            ball_rect.y = -30
                            ball_rect.x = random.randint(0, WIDTH - 40)
                            ball_speed = ISPEED
                            waiting = False
                            pygame.mixer.music.stop()
                            play_music(game_music[0]) 
        if bucket_rect.colliderect(ball_rect):
            score += 1
            ball_rect.y = -30
            ball_rect.x = random.randint(0, WIDTH - 40)
            if score % 10 == 0:
                ball_speed += BSPEED
        draw_window(bucket_rect, ball_rect, score, high_score)
    pygame.quit()
if menu():
    main()
