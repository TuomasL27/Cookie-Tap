import pygame as pg
from pygame import mixer
import os
import time

WIDTH = 1920
HEIGHT = 1080
FPS = 60
COOKIE_BASE_SIZE = (400, 400)
COOKIE_ON_CLICK_SIZE = (300, 300)
COOKIE_POSITION = (120, 450)

WHITE = (255, 255, 255)
FONT_SIZE = 80
FONT_COLOR = (0, 0, 0)

pg.init()
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Cookie Clicker")

font = pg.font.Font(os.path.join("fonts", "Grand9K.ttf"), FONT_SIZE)
coin_img = pg.image.load(os.path.join("assets", "coin.png"))
coin_img = pg.transform.scale(coin_img, (100, 100))

mixer.init()
mixer.music.load(os.path.join("sound", "Game_Theme.mp3"))
mixer.music.set_volume(0.7)
mixer.music.play()


def load_asset(filename, size=(100, 100), folder="assets"):
    asset = pg.image.load(os.path.join(folder, filename))
    return pg.transform.scale(asset, size)


BG = load_asset("BQB.png", size=(WIDTH, HEIGHT))
JAR = load_asset("Jar.png", size=(639,100))


def draw(cookie_img, cookie_count):
    win.fill(WHITE)
    win.blit(BG, (0, 0))
    x = COOKIE_POSITION[0] + (COOKIE_BASE_SIZE[0] - cookie_img.get_width()) // 2
    y = COOKIE_POSITION[1] + (COOKIE_BASE_SIZE[1] - cookie_img.get_height()) // 2

    text_surface = font.render(f"{cookie_count} moneys", True, FONT_COLOR)
    text_rect = text_surface.get_rect(
        x=COOKIE_POSITION[0] + COOKIE_BASE_SIZE[0] // 2 - 0 - text_surface.get_width() // 2, y=-20
    )

    last_letter_x = text_rect.x + text_rect.width
    last_letter_y = text_rect.y
    coin_coords = (last_letter_x + 3, last_letter_y + 23)
    win.blit(text_surface, text_rect)
    win.blit(coin_img, coin_coords)
    win.blit(cookie_img, (x, y))
    win.blit(JAR, (WIDTH-642,390))
    win.blit(JAR, (WIDTH - 642, 490))
    win.blit(JAR, (WIDTH - 642, 590))
    win.blit(JAR, (WIDTH - 642, 690))
    win.blit(JAR, (WIDTH - 642, 790))
    win.blit(JAR, (WIDTH - 642, 890))
    win.blit(JAR, (WIDTH - 642, 990))
    pg.display.update()


def scale_cookie(cookie_img, target_size, duration_sec, cookie_count):
    original_size = cookie_img.get_size()
    current_size = original_size

    if duration_sec == 0:
        duration_sec = 1

    delta_width_down = (original_size[0] - target_size[0]) / max(1, int(duration_sec * FPS) // 2)
    delta_height_down = (original_size[1] - target_size[1]) / max(1, int(duration_sec * FPS) // 2)

    delta_width_up = (original_size[0] - target_size[0]) / max(1, int(duration_sec * FPS) * 4)
    delta_height_up = (original_size[1] - target_size[1]) / max(1, int(duration_sec * FPS) * 4)

    for _ in range(int(duration_sec * FPS) // 2):
        current_size = (current_size[0] - delta_width_down, current_size[1] - delta_height_down)
        scaled_cookie = pg.transform.scale(cookie_img, (int(current_size[0]), int(current_size[1])))
        draw(scaled_cookie, cookie_count)
        pg.time.wait(int(1000 / FPS))

    pg.time.wait(int(1000 / FPS))

    for _ in range(int(duration_sec * FPS) * 4):
        current_size = (current_size[0] + delta_width_up, current_size[1] + delta_height_up)
        scaled_cookie = pg.transform.scale(cookie_img, (int(current_size[0]), int(current_size[1])))
        draw(scaled_cookie, cookie_count)
        pg.time.wait(int(1000 / FPS))

    final_cookie = pg.transform.scale(cookie_img, original_size)
    draw(final_cookie, cookie_count)

def main():
    clock = pg.time.Clock()
    run = True
    FRAMES = 0
    CLICK_ANIMATION_COOLDOWN_FRAME_COUNT = 0
    CLICK_ANIMATION_COOLDOWN = 0.02  # Adjust the cooldown value here
    clicked = False
    animation_playing = False  # Flag variable to track animation state
    COOKIE_1 = load_asset("Cookie_1.png", size=COOKIE_BASE_SIZE)

    cookie_count = 0
    start_time = time.time()
    fun_time = "NON"
    cookie_rect = COOKIE_1.get_rect()
    cookie_rect.topleft = COOKIE_POSITION

    cookie_per_click = 1

    while run:
        clock.tick(FPS)
        FRAMES += 1
        if time.time() - start_time > 600:
            mixer.stop()
            mixer.music.load(os.path.join("sound", "funtime.mp3"))
            mixer.music.set_volume(1)
            mixer.music.play()
            start_time = time.time()
            fun_time = time.time()
        if fun_time != "NON":
            if time.time() - fun_time > 18:
                mixer.stop()
                mixer.music.load(os.path.join("sound", "Game_Theme.mp3"))
                mixer.music.set_volume(0.7)
                mixer.music.play()
                fun_time = "NON"

        for event in pg.event.get():
            pos = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN and not animation_playing:
                # Check if the left mouse button is pressed and the position is within the cookie's area
                if event.button == 1 and (
                        COOKIE_POSITION[0] <= pos[0] <= COOKIE_POSITION[0] + COOKIE_BASE_SIZE[0] and
                        COOKIE_POSITION[1] <= pos[1] <= COOKIE_POSITION[1] + COOKIE_BASE_SIZE[1]
                ):
                    cookie_count += cookie_per_click
                    clicked = True
                    animation_playing = True
                    CLICK_ANIMATION_COOLDOWN_FRAME_COUNT = FRAMES

        if clicked and FRAMES - CLICK_ANIMATION_COOLDOWN_FRAME_COUNT >= CLICK_ANIMATION_COOLDOWN * FPS and animation_playing:
            clicked = False
            COOKIE_1 = load_asset("Cookie_1.png", size=COOKIE_BASE_SIZE)
            scale_cookie(COOKIE_1, COOKIE_ON_CLICK_SIZE, CLICK_ANIMATION_COOLDOWN, cookie_count)
            animation_playing = False

        draw(COOKIE_1, cookie_count)

    pg.quit()

if __name__ == "__main__":
    main()
